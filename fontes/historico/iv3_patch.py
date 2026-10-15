p='template.html'; s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    assert a in s,a[:70]; s=s.replace(a,b,1)
rep('''    <div>Exercícios da lista (carregam M e os picos). Nos seus PDFs a numeração vai de 10 direto para 12.</div>''','''    <div id="an-in">
    <div>Exercícios da lista (carregam M e os picos). Nos seus PDFs a numeração vai de 10 direto para 12.</div>''')
rep('''    <div id="nrule" class="mhint"></div>
    <div id="exinfo"></div>''','''    <div id="nrule" class="mhint"></div>
    </div>
    <div id="an-res" hidden>
    <button class="back" type="button" id="an-back">← Mudar exercício ou picos</button>
    <div id="exinfo"></div>''')
rep('''    <div id="pairs"></div>''','''    <div id="pairs"></div>
    </div>''')
rep("b.onclick=()=>{curEx=e.n;pkSel=null;$('#inM').value=e.M;$('#inP').value=e.peaks.filter(p=>p!==e.M).join(', ');buildChips();analyze();};","b.onclick=()=>{curEx=e.n;pkSel=null;$('#inM').value=e.M;$('#inP').value=e.peaks.filter(p=>p!==e.M).join(', ');buildChips();analyze();anStage(true);};")
rep("$('#go').onclick=()=>{curEx=null;pkSel=null;buildChips();analyze();};","$('#go').onclick=()=>{curEx=null;pkSel=null;buildChips();analyze();anStage(true);};\n$('#an-back').onclick=()=>anStage(false);\nfunction anStage(r){$('#an-in').hidden=r;$('#an-res').hidden=!r;window.scrollTo(0,0);}")
open(p,'w',encoding='utf-8').write(s); print('ok')
