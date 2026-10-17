"""Setas dos mecanismos por pico, desenhadas sobre a estrutura de partida (RDKit).
Especificação: ARW[(ex,pico)] = dict(v=[(rótulo, mark, [setas])], n=nota)
 mark: átomo onde fica o radical +· (ou None)
 seta: (tipo, origem, destino) tipo 'h' (anzol, 1 elétron) ou 'f' (cheia, 1 par)
 ponto: ('A',i) átomo | ('B',i,j) meio da ligação | ('B',i,'H') meio da ligação i–H | ('R',i) elétron sozinho em i | ('H',i) H que sai de i
"""
import math, re
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D

T_ALFA=['O elétron sozinho forma a ligação dupla (anzol 1).','Um elétron da ligação vai com o grupo que sai, que vira radical (anzol 2).']
T_H=['O elétron sozinho forma a ligação dupla com o carbono (anzol 1).','Um elétron da C–H vai com o H, que sai como radical (anzol 2).']
T_MCL=['O elétron sozinho do O pega o H do carbono γ (anzol 1).','A ligação Cα–Cβ se desloca e forma a dupla Cβ=Cγ (anzol 2).','O elétron da ligação C=O forma a dupla C=Cα, e o alqueno sai neutro (anzol 3).']
T_ACIL=['Seta cheia: o par de elétrons da ligação vai com o CO, que sai como molécula neutra. A carga + fica no outro pedaço.']
T_SIMP=['Anzol: um elétron da ligação vai com o pedaço que sai (radical). O outro elétron fica no íon.']
E_ALFA=['ANTES (íon M+·): Y tem 1 e⁻ sozinho (ele ficou assim quando o par livre, 2 e⁻, perdeu 1 e⁻ na ionização). Ligação Y–C: 2 e⁻. Ligação C–R: 2 e⁻.','MOVIMENTO: 1 e⁻ do Y (anzol 1) + 1 e⁻ da ligação C–R (anzol 2 vai para R). Cada anzol move 1 e⁻.','DEPOIS, íon que fica: Y=C passa a ter 4 e⁻ (2 da ligação que já existia + 1 do Y + 1 da C–R). Todos os e⁻ do Y estão pareados, octeto completo. Estável (carga + com octeto).','DEPOIS, o que sai: R leva 1 e⁻ sozinho (radical neutro, 1 e⁻, não aparece no espectro).','CONTA: nenhum e⁻ some na quebra. O e⁻ perdido da molécula (−1 e⁻) foi na ionização.']
E_H=['ANTES (íon M+·): Y tem 1 e⁻ sozinho. Ligação Y–C: 2 e⁻. Ligação C–H: 2 e⁻.','MOVIMENTO: 1 e⁻ do Y (anzol 1) e 1 e⁻ da C–H vai com o H (anzol 2).','DEPOIS, íon que fica: Y=C com 4 e⁻, tudo pareado, carga + no Y (octeto completo). Estável.','DEPOIS, o que sai: H· com 1 e⁻ sozinho (radical neutro). Por isso a massa cai 1 (M − 1).','CONTA: nenhum e⁻ some na quebra.']
E_MCL=['ANTES (íon M+·): O tem 1 e⁻ sozinho. C=O: 4 e⁻. Cγ–H: 2 e⁻. Cα–Cβ: 2 e⁻. Cβ–Cγ: 2 e⁻.','PASSO 1 (anzol 1): o e⁻ sozinho do O + 1 e⁻ da Cγ–H formam a ligação O–H (2 e⁻). O Cγ fica com 1 e⁻ sozinho.','PASSO 2 (anzol 2): 1 e⁻ da Cα–Cβ + o e⁻ sozinho do Cγ formam a 2ª ligação Cβ=Cγ (agora 4 e⁻). O Cα fica com 1 e⁻ sozinho.','PASSO 3 (anzol 3): 1 e⁻ da C=O (4 e⁻ vira 2 e⁻) + o e⁻ sozinho do Cα formam a ligação C=Cα (4 e⁻). A ligação Cα–Cβ se desfaz.','DEPOIS, o que sai: alqueno Cβ=Cγ neutro (4 e⁻ na dupla, tudo pareado, nenhum e⁻ sozinho).','DEPOIS, íon que fica (enol): continua com carga + e 1 e⁻ sozinho (·+). A carga e o e⁻ sozinho trocaram de lugar, mas continuam no íon.']
E_ACIL=['ANTES (acílio R–C≡O⁺): ligação R–C: 2 e⁻. Ligação C≡O: 6 e⁻ (3 pares). Nenhum e⁻ sozinho. O C tem 8 e⁻ em volta (octeto completo).','MOVIMENTO (seta cheia): os 2 e⁻ da ligação R–C vão juntos para o C (par de e⁻).','DEPOIS, o que sai: CO neutro, 10 e⁻ de valência: 6 e⁻ na tripla + 2 e⁻ de par livre no C + 2 e⁻ de par livre no O. Tudo pareado.','DEPOIS, íon que fica: R⁺ perdeu os 2 e⁻ da ligação e ficou com 6 e⁻ em volta do C (sexteto). É menos estável que o acílio, por isso só acontece com R⁺ razoavelmente estável (fenila, terc-butila…).']
E_SIMP=['ANTES: a ligação que quebra tem 2 e⁻.','MOVIMENTO (anzol): 1 e⁻ vai com o pedaço que sai, e 1 e⁻ fica no íon.','DEPOIS, o que sai: leva 1 e⁻ sozinho (radical neutro).','DEPOIS, o íon: ficou com 1 e⁻ do lado dele. Esse e⁻ ou pareia com outro (forma ligação) ou é o e⁻ sozinho do íon. A carga + continua.','CONTA: nenhum e⁻ some na quebra.']
def ALFA(Y,C,R):   return dict(a=[('h',('R',Y),('B',Y,C)),('h',('B',C,R),('A',R))],t=T_ALFA,e=E_ALFA)
def HLOSS(Y,C):    return dict(a=[('h',('R',Y),('B',Y,C)),('h',('B',C,'H'),('H',C))],t=T_H,e=E_H)
def MCL(O,Cc,Ca,Cb,Cg): return dict(a=[('h',('B',Cg,'H'),('A',O)),('h',('B',Ca,Cb),('B',Cb,Cg)),('h',('B',Cc,O),('B',Ca,Cc))],t=T_MCL,e=E_MCL,lay=(O,Cc,Ca,Cb,Cg))
def ACIL(a,c):     return dict(a=[('f',('B',a,c),('A',c))],t=T_ACIL,e=E_ACIL)
def SIMP(a,b):     return dict(a=[('h',('B',a,b),('A',b))],t=T_SIMP,e=E_SIMP)

NOTA_ANEL="Sem setas: a perda envolve abertura ou rearranjo do anel em várias etapas, e eu não consigo desenhar isso com certeza."
NOTA_H="Sem setas: não sei de qual C–H sai o hidrogênio, e não vou chutar."
NOTA_DUV="Sem setas: este mecanismo está na lista de perguntas para o professor."

ARW = {
 (1,91): dict(v=[('',2,ALFA(2,1,0))]),
 (1,77): dict(v=[('',2,SIMP(2,1))]),
 (1,65): dict(n=NOTA_ANEL), (1,51): dict(n=NOTA_ANEL),
 (2,40): dict(n=NOTA_ANEL), (2,39): dict(n=NOTA_ANEL), (2,29): dict(n=NOTA_ANEL),
 (3,103): dict(n=NOTA_H), (3,78): dict(n=NOTA_ANEL), (3,77): dict(v=[('',2,SIMP(2,1))]),
 (3,52): dict(n=NOTA_ANEL), (3,51): dict(n=NOTA_ANEL),
 (4,105): dict(v=[('',0,ALFA(0,1,8))]),
 (4,77): dict(v=[('',None,ACIL(1,2))]), (4,51): dict(n=NOTA_ANEL),
 (5,57): dict(v=[('',3,ALFA(3,2,4))]),
 (5,29): dict(v=[('',None,ACIL(1,2))]),
 (5,27): dict(n="Sem setas: é uma perda de H2 do cátion, sem mecanismo simples para desenhar."),
 (6,59): dict(v=[('Como na lousa (H do O–H)',3,dict(a=[('h',('B',3,'H'),('H',3))],t=['Anzol: um elétron da O–H vai com o H, que sai como radical.'],e=E_SIMP)),
                 ('Como na literatura (H do carbono ligado ao OH)',3,HLOSS(3,2))]),
 (6,42): dict(n="Sem setas desenhadas por mim. O mecanismo do professor está na folha, acima (o H do CH₃ vai para o O e sai água)."),
 (6,31): dict(v=[('',3,ALFA(3,2,1))]),
 (7,58): dict(v=[('1ª etapa: o anel abre (depois sai CH2=O)',2,ALFA(2,1,0))]),
 (7,28): dict(n=NOTA_ANEL),
 (8,78): dict(n=NOTA_H), (8,52): dict(n=NOTA_ANEL), (8,51): dict(n=NOTA_H), (8,50): dict(n=NOTA_DUV),
 (9,73): dict(n="Sem setas desenhadas por mim. O mecanismo do professor está na folha, acima (o O fecha um anel de 4 membros quando sai CH₃)."),
 (9,71): dict(v=[('',4,ALFA(4,3,5))]),
 (9,60): dict(v=[('',4,MCL(4,3,2,1,0))]),
 (9,43): dict(v=[('',None,ACIL(2,3))]),
 (10,72): dict(v=[('',2,HLOSS(2,1))]),
 (10,58): dict(v=[('Como na lousa (sai o CH3 ligado ao N)',2,SIMP(2,3)),
                  ('Pela clivagem α (sai o CH3 do etila)',2,ALFA(2,1,0))]),
 (10,44): dict(v=[('Como na lousa',2,SIMP(2,1))]),
 (11,87): dict(n="Sem setas desenhadas por mim. O mecanismo do professor está na folha, acima (H do carbono α passa para o O e sai ·CH₂CH₃)."),
 (11,85): dict(v=[('',5,ALFA(5,4,6))]),
 (11,74): dict(v=[('',5,MCL(5,4,3,2,1))]),
 (11,57): dict(v=[('',None,ACIL(3,4))]),
 (11,29): dict(n="Sem setas: o cátion butila solta eteno com um deslocamento de H, em mais de uma etapa."),
 (12,85): dict(v=[('',5,HLOSS(5,4))]),
 (12,58): dict(n=NOTA_DUV),
 (12,57): dict(v=[('',None,ACIL(3,4))]),
 (12,44): dict(v=[('',5,MCL(5,4,3,2,1))]),
 (12,29): dict(v=[('',5,ALFA(5,4,3))]),
}

W,Hh=330,230
def _arrow(p0,p1,cen,full,n=None):
    dx,dy=p1[0]-p0[0],p1[1]-p0[1];L=math.hypot(dx,dy) or 1
    nx,ny=-dy/L,dx/L
    mx,my=(p0[0]+p1[0])/2,(p0[1]+p1[1])/2
    if (mx+nx-cen[0])**2+(my+ny-cen[1])**2 < (mx-nx-cen[0])**2+(my-ny-cen[1])**2: nx,ny=-nx,-ny
    off=max(14,min(34,L*0.55));c=(mx+nx*off,my+ny*off)
    col='var(--arrow)';o=[f'<path d="M{p0[0]:.1f} {p0[1]:.1f} Q{c[0]:.1f} {c[1]:.1f} {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="{col}" stroke-width="2.2" stroke-linecap="round"/>']
    tx,ty=p1[0]-c[0],p1[1]-c[1];Lt=math.hypot(tx,ty) or 1;tx,ty=tx/Lt,ty/Lt
    def rot(a):
        ca,sa=math.cos(a),math.sin(a);return (tx*ca-ty*sa,tx*sa+ty*ca)
    b1=rot(math.radians(155));b2=rot(math.radians(-155));k=10
    if full: o.append(f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{p1[0]+b1[0]*k:.1f} {p1[1]+b1[1]*k:.1f} L{p1[0]+b2[0]*k:.1f} {p1[1]+b2[1]*k:.1f}Z" fill="{col}"/>')
    else: o.append(f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{p1[0]+b1[0]*k:.1f} {p1[1]+b1[1]*k:.1f}" stroke="{col}" stroke-width="2.2" stroke-linecap="round" fill="none"/>')
    if n is not None:
        qx,qy=(mx+nx*(off*0.5+9)+nx*off*0.0, my+ny*(off*0.5+9));o.append(f'<text x="{(c[0]+nx*7):.1f}" y="{(c[1]+ny*7+4):.1f}" font-size="12" font-weight="700" text-anchor="middle" fill="{col}" font-family="IBM Plex Mono,ui-monospace,monospace">{n}</text>')
    return o

def build(smi, mark, rec):
    arrows=rec['a'];lay=rec.get('lay')
    m=Chem.RWMol(Chem.MolFromSmiles(smi))
    need=[]
    for t,a,b in arrows:
        for p in (a,b):
            if p[0]=='H' or (p[0]=='B' and p[2]=='H'):
                if p[1] not in need: need.append(p[1])
    hidx={}
    for i in need:
        h=m.AddAtom(Chem.Atom(1));m.AddBond(i,h,Chem.BondType.SINGLE);hidx[i]=h
    m=m.GetMol();Chem.SanitizeMol(m)
    from rdkit.Chem import rdDepictor
    from rdkit.Geometry import Point2D
    rdDepictor.SetPreferCoordGen(False)
    if lay:
        O,Cc,Ca,Cb,Cg=lay
        ang={O:150,hidx[Cg]:90,Cg:30,Cb:-30,Ca:-90,Cc:-150}
        cm={k:Point2D(1.5*math.cos(math.radians(v)),1.5*math.sin(math.radians(v))) for k,v in ang.items()}
        rdDepictor.Compute2DCoords(m,coordMap=cm)
    else:
        rdDepictor.Compute2DCoords(m)
    d=rdMolDraw2D.MolDraw2DSVG(W,Hh);op=d.drawOptions()
    op.clearBackground=False;op.fixedBondLength=44;op.padding=0.18;op.bondLineWidth=2;op.useBWAtomPalette();op.addAtomIndices=False
    d.DrawMolecule(m);d.FinishDrawing()
    s=d.GetDrawingText()
    pos={i:(d.GetDrawCoords(i).x,d.GetDrawCoords(i).y) for i in range(m.GetNumAtoms())}
    cen=(sum(p[0] for p in pos.values())/len(pos),sum(p[1] for p in pos.values())/len(pos))
    def away(i,k):
        x,y=pos[i];nb=[pos[a.GetIdx()] for a in m.GetAtomWithIdx(i).GetNeighbors()]
        bx,by=(sum(p[0] for p in nb)/len(nb),sum(p[1] for p in nb)/len(nb)) if nb else cen
        dx,dy=x-bx,y-by;L=math.hypot(dx,dy)
        if L<1e-3: dx,dy,L=0,-1,1
        return (x+dx/L*k,y+dy/L*k)
    def lab(i): return m.GetAtomWithIdx(i).GetSymbol()!='C'
    def pt(p,toward=None):
        t=p[0]
        if t=='A' or t=='H':
            i=p[1] if t=='A' else hidx[p[1]]
            x,y=pos[i]
            if toward is not None:
                dx,dy=toward[0]-x,toward[1]-y;L=math.hypot(dx,dy) or 1;k=10 if lab(i) else 5
                return (x+dx/L*k,y+dy/L*k)
            return (x,y)
        if t=='B':
            a=p[1];b=hidx[p[1]] if p[2]=='H' else p[2]
            return ((pos[a][0]+pos[b][0])/2,(pos[a][1]+pos[b][1])/2)
        if t=='R': return away(p[1],15)
    extra=[]
    if mark is not None:
        x,y=away(mark,15);extra.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.8" fill="currentColor"/>')
        x2,y2=away(mark,27);extra.append(f'<text x="{x2:.1f}" y="{y2+4:.1f}" font-size="14" text-anchor="middle" fill="currentColor" font-family="IBM Plex Mono,ui-monospace,monospace">+</text>')
    for k,(t,a,b) in enumerate(arrows):
        p0=pt(a);p1=pt(b,toward=p0)
        extra+=_arrow(p0,p1,cen,t=='f',k+1 if len(arrows)>1 else None)
    if lay:
        (x0,y0),(x1,y1)=pos[lay[0]],pos[hidx[lay[4]]];extra.insert(0,f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="currentColor" stroke-width="1.6" stroke-dasharray="3 4" opacity=".6"/>')
    s=s.replace('#000000','currentColor')
    s=re.sub(r"<svg[^>]*>",f'<svg viewBox="0 0 {W} {Hh}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Estrutura com setas do mecanismo" style="width:100%;height:auto;max-width:400px">',s,count=1)
    s=re.sub(r'<!--.*?-->','',s);s=re.sub(r'\s+',' ',s).strip()
    return s.replace('</svg>',''.join(extra)+'</svg>')
