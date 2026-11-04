"""Ajuda dos testes: abre o Chrome do sistema quando o Chromium do Playwright não está instalado."""
import os
def abrir(p, **kw):
    try:
        return p.chromium.launch(**kw)
    except Exception:
        for c in ('/usr/bin/google-chrome','/usr/bin/chromium','/usr/bin/chromium-browser'):
            if os.path.exists(c):
                return p.chromium.launch(executable_path=c,args=['--no-sandbox'],**kw)
        raise
