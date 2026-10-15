import math
def esc(s): return s.replace('&','&amp;').replace('<','&lt;')
class S:
    def __init__(s,w=340,h=150): s.w,s.h,s.o=w,h,[]
    def text(s,x,y,t,size=15,anchor='middle',cls='',fill='currentColor',weight=400):
        s.o.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-weight="{weight}" font-family="IBM Plex Mono,ui-monospace,monospace">{t}</text>')
    def line(s,x1,y1,x2,y2,dash=False,w=1.8):
        s.o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="currentColor" stroke-width="{w}" stroke-linecap="round"'+(' stroke-dasharray="3 4"' if dash else '')+'/>')
    def dbl(s,x1,y1,x2,y2,off=3):
        dx,dy=x2-x1,y2-y1;L=math.hypot(dx,dy);nx,ny=-dy/L*off,dx/L*off
        s.line(x1+nx,y1+ny,x2+nx,y2+ny);s.line(x1-nx,y1-ny,x2-nx,y2-ny)
    def dot(s,x,y,r=2.4,fill='currentColor'):
        s.o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>')
    def arrow(s,p0,c,p1,full=False,n=None):
        col='var(--arrow)'
        s.o.append(f'<path d="M{p0[0]} {p0[1]} Q{c[0]} {c[1]} {p1[0]} {p1[1]}" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round"/>')
        tx,ty=p1[0]-c[0],p1[1]-c[1];L=math.hypot(tx,ty);tx,ty=tx/L,ty/L
        def rot(a):
            ca,sa=math.cos(a),math.sin(a);return (tx*ca-ty*sa,tx*sa+ty*ca)
        b1=rot(math.radians(155));b2=rot(math.radians(-155));k=9
        if full:
            s.o.append(f'<path d="M{p1[0]} {p1[1]} L{p1[0]+b1[0]*k:.1f} {p1[1]+b1[1]*k:.1f} L{p1[0]+b2[0]*k:.1f} {p1[1]+b2[1]*k:.1f}Z" fill="{col}"/>')
        else:
            s.o.append(f'<path d="M{p1[0]} {p1[1]} L{p1[0]+b1[0]*k:.1f} {p1[1]+b1[1]*k:.1f}" stroke="{col}" stroke-width="2" stroke-linecap="round" fill="none"/>')
        if n: s.text(c[0],c[1]-4 if c[1]<p0[1]+20 else c[1]+14,str(n),12,fill='var(--arrow)',weight=600)
    def big(s,x,y,t='→'): s.text(x,y,t,22,fill='var(--muted)')
    def svg(s,label):
        return (f'<svg viewBox="0 0 {s.w} {s.h}" role="img" aria-label="{esc(label)}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;max-width:520px">'+''.join(s.o)+'</svg>')

def m_ioniz():
    s=S(340,110)
    s.text(30,62,'R',16);s.line(40,58,62,58);s.text(74,62,'O',16);s.line(86,58,108,58);s.text(120,62,"R'",16)
    s.dot(68,40);s.dot(80,40)
    s.text(74,26,'par livre',11,fill='var(--muted)')
    s.big(165,64);s.text(165,86,'−e⁻',12,fill='var(--muted)')
    s.text(215,62,'R',16);s.line(225,58,247,58);s.text(259,62,'O',16);s.line(271,58,293,58);s.text(305,62,"R'",16)
    s.dot(259,40);s.text(272,42,'+',13)
    s.text(259,92,'1 elétron sozinho',11,fill='var(--muted)')
    return s.svg('Ionização: o par livre do oxigênio perde 1 elétron e fica com um elétron sozinho e carga mais')
def m_alfa():
    s=S(340,170)
    s.text(40,98,'Y',17);s.text(53,86,'+',12);s.dot(40,72);s.line(52,95,86,95);s.text(104,99,'CH₂',15);s.line(124,95,160,95);s.text(176,99,'R',17)
    s.arrow((40,70),(48,40),(80,84),n=1)
    s.arrow((141,93),(158,62),(172,80),n=2)
    s.big(212,98)
    s.text(256,90,'Y',17);s.text(269,78,'+',12)
    s.dbl(268,92,286,92);s.text(306,96,'CH₂',15)
    s.text(256,140,'+',16);s.dot(284,138);s.text(302,142,'R',17)
    s.text(170,160,'R· sai (radical, neutro)',11,fill='var(--muted)')
    return s.svg('Clivagem alfa: o elétron sozinho do heteroátomo forma a ligação dupla e o grupo R sai como radical')
def m_mcl():
    s=S(340,185)
    O=(60,52);H=(106,28);Cg=(152,52);Cb=(152,102);Ca=(106,126);C=(60,102)
    s.text(*(O[0],O[1]+5),'O',16);s.text(O[0]+12,O[1]-6,'+',11);s.dot(O[0]-14,O[1]-10)
    s.text(*(C[0],C[1]+5),'C',15);s.dbl(O[0],O[1]+10,C[0],C[1]-10,3)
    s.text(Ca[0],Ca[1]+16,'Cα',13);s.text(Cb[0]+16,Cb[1]+5,'Cβ',13);s.text(Cg[0]+16,Cg[1]+5,'Cγ',13);s.text(H[0],H[1]-6,'H',14)
    s.line(C[0]+8,C[1]+8,Ca[0]-8,Ca[1]-8);s.line(Ca[0]+8,Ca[1]-6,Cb[0]-8,Cb[1]+6)
    s.line(Cb[0],Cb[1]-12,Cg[0],Cg[1]+12);s.line(Cg[0]-8,Cg[1]-8,H[0]+6,H[1]+2)
    s.line(O[0]+12,O[1]-10,H[0]-6,H[1]+0,dash=True)
    s.arrow((128,36),(92,22),(76,40),n=1)
    s.arrow((130,118),(168,92),(160,76),n=2)
    s.arrow((54,76),(40,94),(68,114),n=3)
    s.big(222,95)
    s.text(282,70,'HO–C=Cα',13);s.text(282,86,'enol⁺·',12,fill='var(--muted)')
    s.text(282,120,'+  Cβ=Cγ',13);s.text(282,136,'alqueno neutro',12,fill='var(--muted)')
    return s.svg('McLafferty: o oxigênio puxa o hidrogênio do carbono gama por um anel de seis átomos, e sai um alqueno neutro')
def m_hetero():
    s=S(340,130)
    s.text(40,70,'R',17);s.line(52,66,100,66);s.text(112,70,'C',16);s.line(124,64,152,64);s.line(124,68,152,68);s.line(124,60,152,60)
    s.text(164,70,'O',16);s.text(178,58,'+',12)
    s.arrow((76,64),(104,26),(112,54),full=True,n='par')
    s.big(212,72)
    s.text(262,50,'R',17);s.text(275,38,'+',12)
    s.text(256,100,'+',15);s.dot(278,92);s.dot(278,100);s.text(304,104,'C≡O',16)
    return s.svg('Cisão heterolítica: o cátion acílio solta CO levando o par de elétrons da ligação')
def m_h():
    s=S(340,170)
    s.text(40,98,'Y',17);s.text(53,86,'+',12);s.dot(40,72);s.line(52,95,86,95);s.text(104,99,'C',16);s.line(104,86,104,52);s.text(104,42,'H',16)
    s.arrow((40,70),(54,42),(84,84),n=1)
    s.arrow((108,70),(130,46),(116,44),n=2)
    s.big(200,98)
    s.text(246,98,'Y',17);s.text(259,86,'+',12);s.dbl(258,95,288,95);s.text(304,99,'C',16)
    s.text(256,146,'+',16);s.dot(284,144);s.text(302,148,'H',16)
    return s.svg('Perda de H: o heteroátomo forma a ligação dupla com o carbono e o H sai como radical')
MODELS={'ioniz':m_ioniz(),'alfa':m_alfa(),'mcl':m_mcl(),'hetero':m_hetero(),'h':m_h()}
