"""Roda todos os testes, um de cada vez (nunca em paralelo). Antes: python3 empacotar.py
Uso: python3 testes/rodar.py   (de dentro de fontes/)  Para na primeira falha."""
import subprocess,sys,os,glob
aqui=os.path.dirname(os.path.abspath(__file__))
ordem=['teste_identificar.py','teste_ajustes.py','teste_telas.py']
resto=sorted(f for f in map(os.path.basename,glob.glob(aqui+'/teste_*.py')) if f not in ordem)
for f in ordem+resto:
    print('\n=== '+f+' ===',flush=True)
    r=subprocess.run([sys.executable,'-c',
      "import sys,os,runpy;sys.path.insert(0,%r)\nfrom playwright.sync_api import sync_playwright\nimport _nav\nfrom playwright.sync_api import BrowserType\n_o=BrowserType.launch\ndef _l(self,*a,**k):\n  try:return _o(self,*a,**k)\n  except Exception:\n    k.setdefault('executable_path','/usr/bin/google-chrome');k.setdefault('args',['--no-sandbox']);return _o(self,*a,**k)\nBrowserType.launch=_l\nrunpy.run_path(%r,run_name='__main__')"%(aqui,os.path.join(aqui,f))])
    if r.returncode!=0:
        print('FALHOU:',f);sys.exit(1)
print('\nTudo passou.')
