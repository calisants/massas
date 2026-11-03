# Gera os temas de cor com fundo (CSS + lista PALS) e grava em template.html entre marcadores.
import colorsys,re,urllib.parse
def hsl(h,s,l):
    r,g,b=colorsys.hls_to_rgb(h/360,l/100,s/100);return '#%02X%02X%02X'%(round(r*255),round(g*255),round(b*255))
def lum(c):
    v=[int(c[i:i+2],16)/255 for i in (1,3,5)];v=[x/12.92 if x<=.03928 else ((x+.055)/1.055)**2.4 for x in v];return .2126*v[0]+.7152*v[1]+.0722*v[2]
def cr(a,b):
    x,y=sorted([lum(a),lum(b)],reverse=True);return (x+.05)/(y+.05)
# motivos (cada um desenhado ao redor de 0,0)
M={
'flask':"<path d='M-5-13h10M-3-13v9l-9 17a3 3 0 0 0 3 4h18a3 3 0 0 0 3-4l-9-17v-9M-9 8h18'/>",
'tube':"<path d='M-4-14v22a4 4 0 0 0 8 0v-22M-5-14h10M-4 2h8'/>",
'bub':"<circle r='3'/><circle cx='9' cy='-8' r='2'/><circle cx='-8' cy='-9' r='1.5'/>",
'hex':"<path d='M0-12l10.4 6v12L0 12l-10.4-6v-12z'/><path d='M0-7l6 3.5v7L0 7l-6-3.5v-7z'/>",
'hexc':"<path d='M0-12l10.4 6v12L0 12l-10.4-6v-12z'/><circle r='5'/>",
'chain':"<path d='M-16 6l8-5 8 5 8-5 8 5M-8 1v-9M8 1v-9'/><circle cx='-8' cy='-11' r='2.5'/><circle cx='8' cy='-11' r='2.5'/>",
'atom':"<ellipse rx='14' ry='5'/><ellipse rx='14' ry='5' transform='rotate(60)'/><ellipse rx='14' ry='5' transform='rotate(120)'/><circle r='2'/>",
'wave':"<path d='M-18 0q4.5-10 9 0t9 0 9 0 9 0'/>",
'cell':"<circle r='12'/><circle cx='-3' cy='-2' r='4'/><circle cx='6' cy='5' r='1.5'/><circle cx='4' cy='-6' r='1'/>",
'helix':"<path d='M-8-14c16 7-16 21 0 28M8-14c-16 7 16 21 0 28M-5-8h10M-6 0h12M-5 8h10'/>",
'leaf':"<path d='M-10 10C-12-8 2-14 12-12 14-2 6 12-10 10zM-10 10L4-4'/>",
'axes':"<path d='M-14 12h28M-10 14v-28M-10 8q8-2 12-10t10-6'/>",
'tri':"<path d='M-12 10h24L0-10zM0-10v20'/><path d='M-12 10a6 6 0 0 1 4-5' />",
'plus':"<path d='M-6 0h12M0-6v12'/><path d='M12-8h8M12 8h8M16 5v6'/>",
'pend':"<path d='M0-14v16'/><circle cy='9' r='6'/><path d='M-8-14h16'/>",
'spring':"<path d='M-14 0h5l2-6 4 12 4-12 4 12 2-6h5'/>",
'cont':"<path d='M-16 2c2-12 22-14 30-4s-4 18-16 16-16-4-14-12z'/><path d='M-9 1c2-7 14-8 19-2s-3 11-10 10-11-2-9-8z'/><path d='M-3 1c2-3 8-3 9 0s-3 5-6 4-4-2-3-4z'/>",
'mount':"<path d='M-16 10l9-16 5 8 4-6 10 14zM-7-6l3 5'/>",
'strata':"<path d='M-16-8q8 4 16 0t16 0M-16 0q8 4 16 0t16 0M-16 8q8 4 16 0t16 0'/>",
'star':"<path d='M0-9q1 8 9 9-8 1-9 9-1-8-9-9 8-1 9-9z'/>",
'planet':"<circle r='7'/><ellipse rx='15' ry='4' transform='rotate(-20)'/>",
'dots':"<circle cx='-6' cy='-4' r='1'/><circle cx='5' cy='3' r='1'/><circle cx='-2' cy='8' r='1'/>",
'drop':"<path d='M0-12C7-3 9 2 0 10-9 2-7-3 0-12z'/>",
}
# id,nome,hue,keep claro,motivos (6 posições na malha 120x120)
T=[
('quimica','Química',188,'#0A6F7A',['flask','bub','tube','hex','bub','flask']),
('organica','Orgânica',100,'#4A7020',['hexc','chain','hex','chain','hexc','hex']),
('biologia','Biologia',325,'#A63474',['cell','helix','leaf','cell','helix','leaf']),
('fisica','Física',232,'#3445B8',['atom','wave','pend','spring','atom','wave']),
('exatas','Exatas',205,'#2C6A8E',['axes','tri','plus','axes','tri','plus']),
('terra','Ciências da Terra',28,'#8A5427',['cont','mount','strata','cont','mount','strata']),
('astro','Astronomia',262,'#5B3FB0',['planet','star','dots','star','planet','star']),
]
POS=[(22,24),(82,18),(52,52),(104,62),(20,86),(74,100)]
def tile(motifs,col,op):
    body=''
    for (x,y),m in zip(POS,motifs):
        rot=(x*7+y*3)%40-20
        body+="<g transform='translate(%d %d) rotate(%d)'>%s</g>"%(x,y,rot,M[m])
    svg="<svg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 120 120'><g fill='none' stroke='%s' stroke-opacity='%s' stroke-width='1.4' stroke-linecap='round' stroke-linejoin='round'>%s</g></svg>"%(col,op,body)
    return 'url("data:image/svg+xml,'+urllib.parse.quote(svg,safe="/:=' ")+'")'
css=['/* BEGIN temas */']
pals=[];bad=[]
for id,nm,h,k,mo in T:
    L=dict(bg=hsl(h,32,96),surface='#FFFFFF',ink=hsl(h,35,12),muted=hsl(h,14,38),line=hsl(h,24,85),keep=k,soft=hsl(h,48,91))
    kd=hsl(h,62,68)
    D=dict(bg=hsl(h,28,7),surface=hsl(h,24,11),ink=hsl(h,30,91),muted=hsl(h,16,67),line=hsl(h,20,21),keep=kd,soft=hsl(h,42,19))
    for n,c in (('claro',L),('escuro',D)):
        for a,b,t in (('keep','surface',4.5),('muted','bg',4.5),('ink','bg',7),('keep','soft',4.0),('muted','surface',4.5)):
            r=cr(c[a],c[b])
            if r<t:bad.append((id,n,a,b,round(r,2)))
    def v(c):return '--bg:%s;--surface:%s;--ink:%s;--muted:%s;--line:%s;--keep:%s;--focus:%s;--keep-soft:%s'%(c['bg'],c['surface'],c['ink'],c['muted'],c['line'],c['keep'],c['keep'],c['soft'])
    pl=tile(mo,k,'.16');pd=tile(mo,kd,'.2')
    css.append(':root[data-pal="%s"]{%s;--pat:%s}'%(id,v(L),pl))
    dk=v(D)+';--pat:%s'%pd
    css.append('@media (prefers-color-scheme:dark){:root:not([data-theme="light"])[data-pal="%s"]{%s}}'%(id,dk))
    css.append(':root[data-theme="dark"][data-pal="%s"]{%s}'%(id,dk))
    pals.append("['%s','%s','%s','%s','%s']"%(id,nm,k,L['soft'],L['bg']))
css.append('body{background-image:var(--pat,none);background-size:120px 120px;background-attachment:fixed}')
css.append('/* END temas */')
print('contrastes abaixo do alvo:',bad)
s=open('template.html').read()
s=re.sub(r'/\* BEGIN temas \*/.*?/\* END temas \*/\n?','',s,flags=re.S)
i=s.index('</style>');s=s[:i]+'\n'.join(css)+'\n'+s[i:]
# PALS
m=re.search(r"const PALS=\[(.*?)\];\nfunction setPal",s,flags=re.S)
base=["['azul','Azul','#1F5FA8','#DDE9F6','#F3F6FA']","['grafite','Grafite','#3F5A66','#E1E9EC','#F4F4F3']","['roxo','Roxo','#6B3FA0','#E9E0F5','#F6F4FA']","['verde','Verde (o antigo)','#0F6E56','#DCEFE8','#F2F6F5']"]
s=s[:m.start()]+'const PALS=['+','.join(base+pals)+'];\nfunction setPal'+s[m.end():]
open('template.html','w').write(s)
