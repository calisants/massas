"""Recalcula só os overtones (último item do bloco r[17]) de analor_bd.json com compostos.overtones, sem precisar do DBF.
Uso: python3 analor_ot_refaz.py   (precisa de RDKit)"""
import json
from rdkit import Chem
import compostos
d = json.load(open('analor_bd.json', encoding='utf-8'))
mud = 0
for r in d['r']:
    if not r[17]: continue
    m = Chem.MolFromSmiles(r[12])
    novo = compostos.overtones(m)
    if json.loads(json.dumps(novo)) != r[17][-1]:
        r[17][-1] = novo; mud += 1
json.dump(d, open('analor_bd.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(mud, 'compostos com overtones alterados')
