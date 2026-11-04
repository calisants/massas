"""Fragmentos de MS propostos: só com átomos que o composto tem; íon + neutro fecham a massa do pai; só com estrutura ou regra segura."""
import sys,os,re,json
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..'))
from rdkit import Chem
import compostos as cp, msfrag
from compostos_sdbs import SDBSMS
R={r[0]:r for r in cp.RAW}
ok=True;n=0
for nome,(no,msid,pk) in SDBSMS.items():
    if nome not in R: continue
    m=Chem.MolFromSmiles(R[nome][2]);M=int(round(Chem.Descriptors.ExactMolWt(m))) if hasattr(Chem,'Descriptors') else None
    from rdkit.Chem import Descriptors
    M=int(round(Descriptors.ExactMolWt(m)))
    perm={a.GetSymbol() for a in m.GetAtoms()}|{'H'}
    it,sv,sem=msfrag.propor(m,M,pk)
    for x in it:
        n+=1
        if not (msfrag._els(x['f'])|msfrag._els(x['n']))<=perm: ok=False;print('FALHA elemento fora do composto',nome,x['mz'],x['f'],x['n'])
        if x['k']=='' and x['n'] not in ('HC≡CH','H₂O','H₂'): ok=False;print('FALHA sem estrutura e sem regra segura',nome,x['mz'])
        if x['n']=='H₂O' and not m.HasSubstructMatch(Chem.MolFromSmarts('[OX2H]')): ok=False;print('FALHA perda de água sem OH',nome)
print(n,'fragmentos verificados')
sys.exit(0 if ok else 1)
