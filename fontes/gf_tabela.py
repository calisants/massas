"""Tabela de grupos funcionais da Orgânica Básica: exemplo desenhado, com o grupo funcional em destaque."""
import re
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D

# (grupo, estrutura geral, exemplo, SMILES do exemplo, SMARTS do grupo em destaque, sufixo ou prefixo do nome)
GF = [
 ("Alcano", "C–C", "propano", "CCC", "[CX4][CX4]", "-ano"),
 ("Alceno", "C=C", "eteno", "C=C", "C=C", "-eno"),
 ("Alcino", "C≡C", "etino", "C#C", "C#C", "-ino"),
 ("Haleto de alquila", "R–X", "clorometano", "CCl", "[CX4][Cl,Br,I,F]", "cloro-, bromo-"),
 ("Álcool", "R–OH", "etanol", "CCO", "[CX4][OX2H]", "-ol"),
 ("Fenol", "Ar–OH", "fenol", "Oc1ccccc1", "c[OX2H]", "fenol"),
 ("Éter", "R–O–R", "éter dimetílico", "COC", "[CX4][OX2][CX4]", "éter / -óxi-"),
 ("Aldeído", "R–CHO", "etanal", "CC=O", "[CX3H1](=O)", "-al"),
 ("Cetona", "R–CO–R", "propanona", "CC(C)=O", "[CX3](=O)([#6])[#6]", "-ona"),
 ("Ácido carboxílico", "R–COOH", "ácido etanoico", "CC(=O)O", "[CX3](=O)[OX2H]", "ácido -óico"),
 ("Éster", "R–COO–R", "etanoato de etila", "CC(=O)OCC", "[CX3](=O)[OX2][#6]", "-oato de -ila"),
 ("Amida", "R–CONH₂", "etanamida", "CC(N)=O", "[CX3](=O)[NX3]", "-amida"),
 ("Amina", "R–NH₂", "etilamina", "CCN", "[CX4][NX3H2]", "-amina"),
 ("Nitrila", "R–C≡N", "etanonitrila", "CC#N", "C#N", "-nitrila"),
 ("Nitro", "R–NO₂", "nitrobenzeno", "O=[N+]([O-])c1ccccc1", "[N+](=O)[O-]", "nitro-"),
]

def _svg(smi, patt, w=150, h=84):
    m = Chem.MolFromSmiles(smi)
    q = Chem.MolFromSmarts(patt)
    hit = set(); hb = set()
    mt = m.GetSubstructMatch(q)
    hit = set(mt)
    for b in m.GetBonds():
        if b.GetBeginAtomIdx() in hit and b.GetEndAtomIdx() in hit: hb.add(b.GetIdx())
    d = rdMolDraw2D.MolDraw2DSVG(w, h); o = d.drawOptions()
    o.clearBackground = False; o.fixedBondLength = 26; o.padding = 0.1; o.bondLineWidth = 2
    o.setHighlightColour((0.99, 0.82, 0.40, 0.9)); o.highlightBondWidthMultiplier = 9
    d.DrawMolecule(m, highlightAtoms=list(hit), highlightBonds=list(hb))
    d.FinishDrawing()
    t = d.GetDrawingText()
    t = re.sub(r'<\?xml.*?\?>', '', t)
    t = re.sub(r"<rect[^>]*?style='opacity:1\.0;fill:#FFFFFF[^>]*?/>", '', t)
    t = t.replace('#000000', 'currentColor').replace('#FF0000', 'var(--lost)').replace('#0000FF', 'var(--blue)')
    t = re.sub(r"<svg[^>]*>", f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img">', t, count=1)
    t = re.sub(r'<!--.*?-->', '', t); t = re.sub(r'\s+', ' ', t)
    return t.strip()

def tabela():
    linhas = []
    for g, est, nome, smi, patt, suf in GF:
        assert Chem.MolFromSmiles(smi) and Chem.MolFromSmarts(patt) and Chem.MolFromSmiles(smi).HasSubstructMatch(Chem.MolFromSmarts(patt)), g
        linhas.append(f'<tr><td class="gfn"><b>{g}</b><div class="mut sm">{est}</div></td><td class="gfs">{_svg(smi, patt)}<div class="mut sm">{nome}</div></td><td>{suf}</td></tr>')
    return ('<div class="tbl"><table class="obt nostk"><thead><tr><th>Grupo</th><th>Exemplo (grupo em destaque)</th><th>Nome</th></tr></thead><tbody>'
            + ''.join(linhas) + '</tbody></table></div>')
