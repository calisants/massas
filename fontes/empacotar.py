"""Gera tudo com um comando, rodando dentro de fontes/:   python3 empacotar.py
1) roda build3.py (estruturas em SVG com RDKit + dados) -> saida.html (fragmento, serve para o artefato)
2) sobe o número de versão (sw.js e o texto 'Versão' dentro do app)
3) embrulha em documento completo -> ../index.html
Precisa de: python3 com rdkit (pip install rdkit)."""
import os, re, subprocess, sys, datetime
aqui=os.path.dirname(os.path.abspath(__file__)); os.chdir(aqui)
env=dict(os.environ,SAIDA='saida.html')
subprocess.run([sys.executable,'build3.py'],check=True,env=env)
sw=open('../sw.js',encoding='utf-8').read()
n=int(re.search(r'massas-v(\d+)',sw).group(1))+1
open('../sw.js','w',encoding='utf-8').write(re.sub(r'massas-v\d+',f'massas-v{n}',sw))
hoje=datetime.date.today().strftime('%d/%m/%Y')
s=open('saida.html',encoding='utf-8').read()
s=re.sub(r"const VERSAO='[^']*';",f"const VERSAO='v{n} · {hoje}';",s)
open('saida.html','w',encoding='utf-8').write(s)
i=s.index('</style>')+len('</style>'); head,body=s[:i],s[i:]
head=('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
 '<meta name="theme-color" content="#1F5FA8">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-title" content="Massas">\n'
 '<link rel="manifest" href="manifest.webmanifest">\n<link rel="icon" href="icon-192.png">\n<link rel="apple-touch-icon" href="icon-192.png">\n')+head+'\n</head>\n<body>'
body=body.rstrip()+'\n<script>\nif("serviceWorker" in navigator&&location.protocol.indexOf("http")===0){\n  window.addEventListener("load",function(){navigator.serviceWorker.register("sw.js").catch(function(){});});\n}\n</script>\n</body>\n</html>\n'
open('../index.html','w',encoding='utf-8').write(head+body)
print(f'pronto: versão v{n}, ../index.html e saida.html (para o artefato)')
