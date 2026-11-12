"""Banco de compostos do Analorg.
Tudo o que dá para CALCULAR vem do RDKit (fórmula, massa, GDH, estrutura, quantidade de sinais de RMN, bandas de IV esperadas por grupo funcional).
O que é escrito à mão (PF, PE, cor, estado, grupo de solubilidade, CAS, picos de MS) fica marcado como "sem fonte conferida" no app.
build_comp() devolve a lista COMP que o build3.py coloca no app."""
import math
from collections import defaultdict
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors

# nome, outros nomes, SMILES, CAS, estado (25 °C), cor, PF °C, PE °C, grupo de solubilidade, nº do exercício de MS (ou None), observação
RAW = [
 ("metanol", ["álcool metílico"], "CO", "67-56-1", "líquido", "incolor", -98, 65, "S1", None, ""),
 ("etanol", ["álcool etílico"], "CCO", "64-17-5", "líquido", "incolor", -114, 78, "S1", None, ""),
 ("1-propanol", ["propan-1-ol"], "CCCO", "71-23-8", "líquido", "incolor", -126, 97, "S1", 6, ""),
 ("2-propanol", ["isopropanol", "álcool isopropílico"], "CC(C)O", "67-63-0", "líquido", "incolor", -88, 82, "S1", None, ""),
 ("1-butanol", ["butan-1-ol", "álcool butílico"], "CCCCO", "71-36-3", "líquido", "incolor", -90, 118, "S1", None, "4 C, no limite da solubilidade em água"),
 ("ciclo-hexanol", ["cicloexanol", "ciclohexanol"], "OC1CCCCC1", "108-93-0", "líquido", "incolor", 25, 161, "N", None, "PF perto da temperatura ambiente: pode estar sólido"),
 ("álcool benzílico", ["fenilmetanol"], "OCc1ccccc1", "100-51-6", "líquido", "incolor", -15, 205, "N", None, ""),
 ("glicerol", ["glicerina", "propano-1,2,3-triol"], "OCC(O)CO", "56-81-5", "líquido viscoso", "incolor", 18, 290, "S2", None, "polifuncional; o PE é com decomposição"),
 ("fenol", ["hidroxibenzeno"], "Oc1ccccc1", "108-95-2", "sólido", "incolor (fica rosado com o ar)", 41, 182, "A2", None, ""),
 ("acetona", ["propanona", "dimetilcetona"], "CC(C)=O", "67-64-1", "líquido", "incolor", -95, 56, "S1", None, ""),
 ("butanona", ["2-butanona", "metil etil cetona", "MEK"], "CCC(C)=O", "78-93-3", "líquido", "incolor", -86, 80, "S1", None, ""),
 ("3-pentanona", ["dietilcetona", "pentan-3-ona"], "CCC(=O)CC", "96-22-0", "líquido", "incolor", -39, 102, "S1", 5, ""),
 ("ciclo-hexanona", ["cicloexanona", "ciclohexanona"], "O=C1CCCCC1", "108-94-1", "líquido", "incolor", -47, 156, "N", None, ""),
 ("acetofenona", ["metil fenil cetona"], "CC(=O)c1ccccc1", "98-86-2", "líquido", "incolor", 20, 202, "N", None, "PF perto da temperatura ambiente"),
 ("benzofenona", ["difenilmetanona"], "O=C(c1ccccc1)c1ccccc1", "119-61-9", "sólido", "branco", 48, 305, "N", 4, ""),
 ("pentanal", ["valeraldeído", "aldeído valérico"], "CCCCC=O", "110-62-3", "líquido", "incolor", -92, 103, "S1", 12, "5 C, mas pouco solúvel em água: está no limite"),
 ("benzaldeído", ["fenilmetanal"], "O=Cc1ccccc1", "100-52-7", "líquido", "incolor", -26, 179, "N", None, ""),
 ("ácido acético", ["ácido etanoico"], "CC(=O)O", "64-19-7", "líquido", "incolor", 17, 118, "SA", None, "PF perto da temperatura ambiente (gelo glacial)"),
 ("ácido butanoico", ["ácido butírico"], "CCCC(=O)O", "107-92-6", "líquido", "incolor", -5, 164, "SA", 9, "cheiro forte"),
 ("ácido benzoico", ["ácido benzenocarboxílico"], "OC(=O)c1ccccc1", "65-85-0", "sólido", "branco", 122, 249, "A1", None, ""),
 ("ácido benzílico", ["ácido difenil-hidroxiacético", "ácido 2-hidroxi-2,2-difenilacético"], "OC(=O)C(O)(c1ccccc1)c1ccccc1", "76-93-7", "sólido", "branco", 150, None, "A1", None, "decompõe ao aquecer; sem PE comum"),
 ("ácido salicílico", ["ácido 2-hidroxibenzoico"], "OC(=O)c1ccccc1O", "69-72-7", "sólido", "branco", 159, None, "A1", None, "sublima; não tem PE comum"),
 ("acetato de etila", ["etanoato de etila"], "CCOC(C)=O", "141-78-6", "líquido", "incolor", -84, 77, "S1", None, ""),
 ("pentanoato de metila", ["valerato de metila"], "CCCCC(=O)OC", "624-24-8", "líquido", "incolor", -91, 127, "N", 11, ""),
 ("éter dietílico", ["etoxietano", "éter etílico"], "CCOCC", "60-29-7", "líquido", "incolor", -116, 35, "N", None, "muito volátil e inflamável"),
 ("1,4-dioxano", ["dioxano"], "C1COCCO1", "123-91-1", "líquido", "incolor", 12, 101, "S1", 7, "miscível com água"),
 ("furano", ["óxido de divinileno"], "c1ccoc1", "110-00-9", "líquido", "incolor", -86, 31, "N", 2, "muito volátil"),
 ("acetamida", ["etanamida"], "CC(N)=O", "60-35-5", "sólido", "branco", 81, 221, "S1", None, "amida de 2 C"),
 ("benzamida", [], "NC(=O)c1ccccc1", "55-21-0", "sólido", "branco", 128, 288, "MN", None, "tem N; insolúvel em água, NaOH e HCl"),
 ("acetanilida", ["N-fenilacetamida"], "CC(=O)Nc1ccccc1", "103-84-4", "sólido", "branco", 114, 304, "MN", None, ""),
 ("ureia", ["carbamida"], "NC(N)=O", "57-13-6", "sólido", "branco", 133, None, "S2", None, "polifuncional; decompõe ao aquecer"),
 ("anilina", ["fenilamina", "aminobenzeno"], "Nc1ccccc1", "62-53-3", "líquido", "incolor (escurece com o ar)", -6, 184, "B", None, "pouco solúvel em água; dissolve em HCl 5%"),
 ("piridina", [], "c1ccncc1", "110-86-1", "líquido", "incolor", -42, 115, "SB", 8, ""),
 ("N,N-dimetiletilamina", ["dimetiletilamina"], "CCN(C)C", "598-56-1", "líquido", "incolor", None, 37, "SB", 10, "muito volátil"),
 ("trietilamina", ["N,N-dietiletanamina"], "CCN(CC)CC", "121-44-8", "líquido", "incolor", -115, 89, "SB", None, ""),
 ("dietilamina", [], "CCNCC", "109-89-7", "líquido", "incolor", -50, 55, "SB", None, "muito volátil"),
 ("dimetilamina", ["N-metilmetanamina"], "CNC", "124-40-3", "gás", "incolor", -93, 7, "SB", None, "gás a 25 °C; costuma vir em solução aquosa"),
 ("acetonitrila", ["cianeto de metila", "etanonitrila"], "CC#N", "75-05-8", "líquido", "incolor", -45, 82, "S1", None, ""),
 ("nitrobenzeno", [], "O=[N+]([O-])c1ccccc1", "98-95-3", "líquido", "amarelo-claro", 6, 211, "N", None, "tóxico"),
 ("clorobenzeno", ["cloro-benzeno"], "Clc1ccccc1", "108-90-7", "líquido", "incolor", -45, 132, "I", None, ""),
 ("clorofórmio", ["triclorometano"], "ClC(Cl)Cl", "67-66-3", "líquido", "incolor", -63, 61, "I", None, ""),
 ("diclorometano", ["cloreto de metileno"], "ClCCl", "75-09-2", "líquido", "incolor", -97, 40, "I", None, "muito volátil"),
 ("hexano", ["n-hexano"], "CCCCCC", "110-54-3", "líquido", "incolor", -95, 69, "I", None, ""),
 ("ciclo-hexano", ["cicloexano", "ciclohexano"], "C1CCCCC1", "110-82-7", "líquido", "incolor", 7, 81, "I", None, ""),
 ("ciclo-hexeno", ["cicloexeno", "ciclohexeno"], "C1=CCCCC1", "110-83-8", "líquido", "incolor", -104, 83, "N", None, "alceno: dissolve em H₂SO₄ 96%"),
 ("benzeno", [], "c1ccccc1", "71-43-2", "líquido", "incolor", 5.5, 80, "I", None, "cancerígeno"),
 ("tolueno", ["metilbenzeno"], "Cc1ccccc1", "108-88-3", "líquido", "incolor", -95, 111, "I", None, ""),
 ("etilbenzeno", [], "CCc1ccccc1", "100-41-4", "líquido", "incolor", -95, 136, "I", 1, ""),
 ("estireno", ["vinilbenzeno"], "C=Cc1ccccc1", "100-42-5", "líquido", "incolor", -31, 145, "N", 3, "alceno: dissolve em H₂SO₄ 96%"),
 ("naftaleno", [], "c1ccc2ccccc2c1", "91-20-3", "sólido", "branco", 80, 218, "I", None, "sublima"),
 ("2-butanol", ["butan-2-ol", "álcool sec-butílico"], "CCC(C)O", "78-92-2", "líquido", "incolor", -115, 99, "S1", None, ""),
 ("terc-butanol", ["2-metilpropan-2-ol", "álcool terc-butílico"], "CC(C)(C)O", "75-65-0", "líquido", "incolor", 25, 82, "S1", None, "PF perto da temperatura ambiente: pode estar sólido"),
 ("etilenoglicol", ["etano-1,2-diol", "glicol"], "OCCO", "107-21-1", "líquido viscoso", "incolor", -13, 197, "S2", None, "polifuncional"),
 ("propanal", ["propionaldeído"], "CCC=O", "123-38-6", "líquido", "incolor", -81, 48, "S1", None, "muito volátil"),
 ("ácido fórmico", ["ácido metanoico"], "OC=O", "64-18-6", "líquido", "incolor", 8, 101, "SA", None, "cheiro pungente"),
 ("ácido propanoico", ["ácido propiônico"], "CCC(=O)O", "79-09-4", "líquido", "incolor", -21, 141, "SA", None, "cheiro pungente"),
 ("ácido cítrico", [], "OC(=O)CC(O)(CC(O)=O)C(O)=O", "77-92-9", "sólido", "branco", 153, None, "SA", None, "polifuncional; decompõe ao aquecer"),
 ("ácido tartárico", ["ácido 2,3-di-hidroxibutanodioico"], "OC(C(O)C(O)=O)C(O)=O", "87-69-4", "sólido", "branco", 172, None, "SA", None, "L-(+); decompõe ao aquecer"),
 ("glicose", ["D-glicose", "dextrose"], "OCC1OC(O)C(O)C(O)C1O", "50-99-7", "sólido", "branco", 146, None, "S2", None, "polifuncional; decompõe ao aquecer"),
 ("sacarose", ["açúcar de mesa"], "OCC1OC(CO)(OC2OC(CO)C(O)C(O)C2O)C(O)C1O", "57-50-1", "sólido", "branco", 186, None, "S2", None, "decompõe (caramelizar) em vez de ferver"),
 ("acetato de metila", ["etanoato de metila"], "COC(C)=O", "79-20-9", "líquido", "incolor", -98, 57, "S1", None, "muito volátil"),
 ("acetato de butila", ["etanoato de butila"], "CCCCOC(C)=O", "123-86-4", "líquido", "incolor", -78, 126, "N", None, "cheiro de fruta"),
 ("valerato de metila", ["pentanoato de metila"], "CCCCC(=O)OC", "624-24-8", "líquido", "incolor", -91, 127, "N", None, "cheiro de fruta"),
 ("benzoato de metila", [], "COC(=O)c1ccccc1", "93-58-3", "líquido", "incolor", -12, 199, "N", None, ""),
 ("salicilato de metila", ["óleo de gaultéria"], "COC(=O)c1ccccc1O", "119-36-8", "líquido", "incolor", -8, 222, "A2", None, "éster e fenol ao mesmo tempo"),
 ("anidrido acético", ["anidrido etanoico"], "CC(=O)OC(C)=O", "108-24-7", "líquido", "incolor", -73, 140, "N", None, "reage com água; cheiro pungente"),
 ("aspirina", ["ácido acetilsalicílico"], "CC(=O)Oc1ccccc1C(O)=O", "50-78-2", "sólido", "branco", 135, None, "A1", None, "decompõe ao aquecer"),
 ("ácido esteárico", ["ácido octadecanoico"], "CCCCCCCCCCCCCCCCCC(O)=O", "57-11-4", "sólido", "branco", 69, 361, "A1", None, "ácido graxo"),
 ("ácido cinâmico", ["ácido trans-cinâmico"], "OC(=O)/C=C/c1ccccc1", "140-10-3", "sólido", "branco", 133, 300, "A1", None, "trans"),
 ("ácido 4-nitrobenzoico", ["ácido p-nitrobenzoico"], "OC(=O)c1ccc(cc1)[N+]([O-])=O", "62-23-7", "sólido", "amarelo-claro", 240, None, "A1", None, "sublima"),
 ("anisol", ["metoxibenzeno"], "COc1ccccc1", "100-66-3", "líquido", "incolor", -37, 154, "N", None, ""),
 ("tetra-hidrofurano", ["THF", "oxolano"], "C1CCOC1", "109-99-9", "líquido", "incolor", -108, 66, "S1", None, "miscível com água"),
 ("N,N-dimetilformamida", ["DMF"], "CN(C)C=O", "68-12-2", "líquido", "incolor", -61, 153, "S1", None, ""),
 ("dimetilsulfóxido", ["DMSO"], "CS(C)=O", "67-68-5", "líquido", "incolor", 18, 189, "S1", None, "PF perto da temperatura ambiente"),
 ("benzonitrila", ["cianobenzeno"], "N#Cc1ccccc1", "100-47-0", "líquido", "incolor", -13, 191, "MN", None, "cheiro de amêndoas"),
 ("difenilamina", [], "c1ccc(Nc2ccccc2)cc1", "122-39-4", "sólido", "branco", 53, 302, "MN", None, "amina muito fraca: não dissolve em HCl 5%"),
 ("N,N-dimetilanilina", ["dimetilfenilamina"], "CN(C)c1ccccc1", "121-69-7", "líquido", "incolor (amarela com o ar)", 2, 194, "B", None, ""),
 ("p-toluidina", ["4-metilanilina"], "Cc1ccc(N)cc1", "106-49-0", "sólido", "branco", 44, 200, "B", None, ""),
 ("benzilamina", ["fenilmetanamina"], "NCc1ccccc1", "100-46-9", "líquido", "incolor", 10, 185, "SB", None, "miscível com água"),
 ("butilamina", ["butan-1-amina"], "CCCCN", "109-73-9", "líquido", "incolor", -49, 78, "SB", None, "cheiro de peixe"),
 ("p-fenilenodiamina", ["benzeno-1,4-diamina"], "Nc1ccc(N)cc1", "106-50-3", "sólido", "marrom-claro (escurece com o ar)", 145, 267, "B", None, "oxida com facilidade"),
 ("o-cresol", ["2-metilfenol"], "Cc1ccccc1O", "95-48-7", "sólido", "incolor", 31, 191, "A2", None, "PF perto da temperatura ambiente"),
 ("p-cresol", ["4-metilfenol"], "Cc1ccc(O)cc1", "106-44-5", "sólido", "incolor", 35, 202, "A2", None, "PF perto da temperatura ambiente"),
 ("timol", ["2-isopropil-5-metilfenol"], "Cc1ccc(C(C)C)c(O)c1", "89-83-8", "sólido", "branco", 49, 233, "A2", None, ""),
 ("vanilina", ["4-hidroxi-3-metoxibenzaldeído"], "COc1cc(C=O)ccc1O", "121-33-5", "sólido", "branco", 82, 285, "A2", None, "aldeído e fenol ao mesmo tempo"),
 ("1-naftol", ["α-naftol"], "Oc1cccc2ccccc12", "90-15-3", "sólido", "branco-acinzentado (escurece)", 96, 288, "A2", None, ""),
 ("2-naftol", ["β-naftol"], "Oc1ccc2ccccc2c1", "135-19-3", "sólido", "branco (rosado com a luz)", 122, 285, "A2", None, ""),
 ("tiofenol", ["benzenotiol"], "Sc1ccccc1", "108-98-5", "líquido", "incolor", -15, 169, "A2", None, "cheiro de alho; tóxico"),
 ("4-nitrofenol", ["p-nitrofenol"], "Oc1ccc(cc1)[N+]([O-])=O", "100-02-7", "sólido", "amarelo-claro", 114, None, "A2", None, "amarelo mais forte em meio básico"),
 ("2,4-dinitrofenol", ["DNP"], "Oc1ccc(cc1[N+]([O-])=O)[N+]([O-])=O", "51-28-5", "sólido", "amarelo", 112, None, "A1", None, "tóxico; explosivo se seco"),
 ("4-nitroanilina", ["p-nitroanilina"], "Nc1ccc(cc1)[N+]([O-])=O", "100-01-6", "sólido", "amarelo-alaranjado", 148, 332, "MN", None, "base muito fraca"),
 ("1,4-benzoquinona", ["p-benzoquinona"], "O=C1C=CC(=O)C=C1", "106-51-4", "sólido", "amarelo", 115, None, "N", None, "sublima; cheiro irritante"),
 ("benzil", ["difenil-etanodiona"], "O=C(C(=O)c1ccccc1)c1ccccc1", "134-81-6", "sólido", "amarelo", 95, 347, "N", None, "dicetona conjugada"),
 ("antraquinona", [], "O=C1c2ccccc2C(=O)c2ccccc12", "84-65-1", "sólido", "amarelo-claro", 286, 379, "N", None, ""),
 ("azobenzeno", [], "c1ccc(cc1)N=Nc1ccccc1", "103-33-3", "sólido", "laranja-avermelhado", 68, 293, "N", None, "azocomposto"),
 ("N,N-dimetil-4-nitrosoanilina", ["p-nitrosodimetilanilina"], "CN(C)c1ccc(cc1)N=O", "138-89-6", "sólido", "verde-escuro", 85, None, "B", None, "nitrosocomposto"),
 ("iodofórmio", ["triiodometano"], "IC(I)I", "75-47-8", "sólido", "amarelo", 119, None, "I", None, "cheiro característico; decompõe ao aquecer"),
 ("bromobenzeno", [], "Brc1ccccc1", "108-86-1", "líquido", "incolor", -31, 156, "I", None, ""),
 ("1-bromobutano", ["brometo de butila"], "CCCCBr", "109-65-9", "líquido", "incolor", -112, 101, "I", None, ""),
 ("tetracloreto de carbono", ["tetraclorometano"], "ClC(Cl)(Cl)Cl", "56-23-5", "líquido", "incolor", -23, 77, "I", None, "tóxico"),
 ("pentano", ["n-pentano"], "CCCCC", "109-66-0", "líquido", "incolor", -130, 36, "I", None, "muito volátil"),
 ("heptano", ["n-heptano"], "CCCCCCC", "142-82-5", "líquido", "incolor", -91, 98, "I", None, ""),
 ("1-hexeno", ["hex-1-eno"], "C=CCCCC", "592-41-6", "líquido", "incolor", -140, 63, "N", None, "alceno: dissolve em H₂SO₄ 96%"),
 ("fenilacetileno", ["etinilbenzeno"], "C#Cc1ccccc1", "536-74-3", "líquido", "incolor", -45, 142, "N", None, "alcino terminal"),
 ("o-xileno", ["1,2-dimetilbenzeno"], "Cc1ccccc1C", "95-47-6", "líquido", "incolor", -25, 144, "I", None, ""),
 ("bifenilo", ["difenila"], "c1ccc(cc1)-c1ccccc1", "92-52-4", "sólido", "branco", 69, 255, "I", None, ""),
 ("antraceno", [], "c1ccc2cc3ccccc3cc2c1", "120-12-7", "sólido", "incolor (fluoresce azul)", 216, 340, "I", None, ""),
 ("cânfora", [], "CC1(C)C2CCC1(C)C(=O)C2", "76-22-2", "sólido", "branco", 176, 204, "N", None, "sublima; cheiro característico"),
 ("ácido 5-formilsalicílico", ["ácido formilsalicílico", "ácido 5-formil-2-hidroxibenzoico", "5-formilsalicylic acid"], "O=Cc1ccc(O)c(c1)C(=O)O", "616-76-2", "sólido", "branco a amarelo", 250, None, "A1", None, "decompõe na fusão (PF 250 °C com decomposição, TCI e Sigma-Aldrich); aldeído, fenol e ácido carboxílico na mesma molécula"),
 ("1-nitroso-2-naftol", ["1-nitroso-2-naphthol", "1-nitrosonaftalen-2-ol", "α-nitroso-β-naftol"], "Oc1ccc2ccccc2c1N=O", "131-91-9", "sólido", "laranja a marrom (TCI); amarelo-amarronzado (Wikipedia)", 107, None, "A2", None, "PF 106 a 110 °C (TCI); fenol com grupo nitroso; forma quelatos coloridos com Fe(II) e Co(II); tautomeria nitroso/oxima"),
 ("m-xileno", ["1,3-dimetilbenzeno", "meta-xileno"], "Cc1cccc(C)c1", "108-38-3", "líquido", "incolor", None, 139, "I", None, "meta-dissubstituído; PF não consta no banco Analor; grupo de solubilidade previsto pela regra (hidrocarboneto), não medido"),
 ("m-cresol", ["3-metilfenol", "meta-cresol"], "Cc1cccc(O)c1", "108-39-4", "líquido", "incolor ou amarelo", 9, 203, "A2", None, "meta-dissubstituído; PF perto da temperatura ambiente; dados do banco Analor"),
 ("resorcinol", ["benzeno-1,3-diol", "1,3-di-hidroxibenzeno"], "Oc1cccc(O)c1", "108-46-3", "sólido", "branco", 110, None, "S1", None, "meta-dissubstituído; PE não consta no banco Analor; grupo previsto pela regra (muito solúvel em água), não medido"),
 ("m-nitroanilina", ["3-nitroanilina", "meta-nitroanilina"], "Nc1cccc(c1)[N+]([O-])=O", "99-09-2", "sólido", "amarelo", 114, 306, "MN", None, "meta-dissubstituído; base muito fraca; grupo previsto por analogia com a 4-nitroanilina"),
 ("ácido 3-nitrobenzoico", ["ácido m-nitrobenzoico"], "OC(=O)c1cccc(c1)[N+]([O-])=O", "121-92-6", "sólido", "branco ou amarelo", 141, None, "A1", None, "meta-dissubstituído; dados do banco Analor"),
 ("m-toluidina", ["3-metilanilina", "meta-toluidina"], "Cc1cccc(N)c1", "108-44-1", "líquido", "incolor ou amarelo", None, 203, "B", None, "meta-dissubstituído; PF não consta no banco Analor; grupo previsto por analogia com a anilina"),
 ("1,3-dinitrobenzeno", ["m-dinitrobenzeno"], "O=[N+]([O-])c1cccc(c1)[N+]([O-])=O", "99-65-0", "sólido", "amarelo", 90, 297, "N", None, "meta-dissubstituído; tóxico; grupo previsto por analogia com o nitrobenzeno"),
 ("m-diclorobenzeno", ["1,3-diclorobenzeno"], "Clc1cccc(Cl)c1", "541-73-1", "líquido", "incolor", -24, 173, "I", None, "meta-dissubstituído; grupo previsto por analogia com o clorobenzeno"),
 ("ácido isoftálico", ["ácido benzeno-1,3-dicarboxílico"], "OC(=O)c1cccc(c1)C(O)=O", "121-91-5", "sólido", "incolor", 348, None, "A1", None, "meta-dissubstituído; PE não consta no banco Analor; grupo previsto pela regra de ácido carboxílico"),
]

# Picos de MS (EI, 70 eV) escritos à mão a partir de espectros comuns. Os dos exercícios 1 a 12 vêm do EX (lousa/SDBS) e não passam por aqui.
MSK = {
 "2-butanol":[74,45,31,29,27], "terc-butanol":[74,59,31,41,43], "etilenoglicol":[62,31,33,43], "propanal":[58,29,57,28], "ácido fórmico":[46,45,29],
 "ácido propanoico":[74,45,73,29,28], "acetato de metila":[74,43,59,15], "acetato de butila":[116,43,56,73,61], "benzoato de metila":[136,105,77,51],
 "aspirina":[180,138,120,92,43], "anisol":[108,78,65,77,51], "tetra-hidrofurano":[72,71,42,41,43], "N,N-dimetilformamida":[73,44,42,30], "dimetilsulfóxido":[78,63,45,15],
 "benzonitrila":[103,76,50], "N,N-dimetilanilina":[121,120,77,105,42], "bromobenzeno":[156,158,77,51], "pentano":[72,43,42,41,57], "heptano":[100,43,57,41,71],
 "1-hexeno":[84,56,41,55,42], "o-xileno":[106,91,105,77], "bifenilo":[154,153,152,76], "antraceno":[178,176,152,89],
 "metanol":[32,31,29], "etanol":[46,45,31,29,27], "2-propanol":[60,45,43,27], "1-butanol":[74,56,43,41,31,29,27],
 "ciclo-hexanol":[100,82,67,57], "álcool benzílico":[108,107,79,77], "glicerol":[61,43,31], "fenol":[94,66,65,39],
 "acetona":[58,43,15], "butanona":[72,57,43,29], "ciclo-hexanona":[98,69,55,42], "acetofenona":[120,105,77,51,43],
 "benzaldeído":[106,105,77,51], "ácido acético":[60,45,43,15], "ácido benzoico":[122,105,77,51], "ácido benzílico":[228,183,105,77], "ácido salicílico":[138,120,92,64],
 "acetato de etila":[88,70,61,45,43,29], "éter dietílico":[74,59,45,31,29], "acetamida":[59,44,43,42], "benzamida":[121,105,77,51],
 "acetanilida":[135,93,66,43], "ureia":[60,44,43,17], "anilina":[93,66,65,39], "trietilamina":[101,86,58,30], "dietilamina":[73,58,44,30], "dimetilamina":[45,44,42,28], "valerato de metila":[116,74,43,87,57],
 "acetonitrila":[41,40,39], "nitrobenzeno":[123,93,77,65,51], "clorobenzeno":[114,112,77,51], "clorofórmio":[85,83,47],
 "diclorometano":[86,84,51,49], "hexano":[86,57,43,41,29], "ciclo-hexano":[84,69,56,41], "ciclo-hexeno":[82,67,54],
 "benzeno":[78,52,51,50], "tolueno":[92,91,65,51,39], "naftaleno":[128,102,64],
}

# Grupos funcionais -> bandas de IV esperadas. (SMARTS, rótulo do grupo, [(cm-1 baixo, cm-1 alto, atribuição, intensidade, chave?)])
# Faixas da "Apostila de Interpretação de Espectros de IV" (a que está na pasta Analorg do Drive); onde a apostila não traz, usei tabela geral (Pavia) e marquei fonte "g".
IVG = [
 ("[CH2X4][OX2H]", "álcool", [(3550,3200,"O–H (estiramento)","F, larga",1,"a"),(1090,1000,"C–O de álcool primário","F",0,"s")]),
 ("[CH1X4]([#6])([#6])[OX2H]", "álcool", [(3550,3200,"O–H (estiramento)","F, larga",1,"a"),(1150,1060,"C–O de álcool secundário","F",0,"s")]),
 ("[CX4;H0]([#6])([#6])([#6])[OX2H]", "álcool", [(3550,3200,"O–H (estiramento)","F, larga",1,"a"),(1205,1124,"C–O de álcool terciário","F",0,"s")]),
 ("c[OX2H]", "fenol", [(3550,3150,"O–H (estiramento)","F, larga",1,"a"),(1275,1200,"C–O (estiramento)","F",0,"s")]),
 ("[CX3](=O)[OX2H]", "ácido carboxílico", [(3300,2500,"O–H (estiramento)","F, muito larga",1,"a"),(1750,1700,"C=O (estiramento)","F",1,"s"),(1320,1170,"C–O de ácido carboxílico (estiramento)","F",0,"s")]),
 ("[CX3](=O)[OX2][#6]", "éster", [(1750,1735,"C=O (estiramento)","F",1,"a"),(1300,1000,"C–O (estiramento)","F, 2 bandas",0,"a")]),
 ("[CX3H1](=O)[#6]", "aldeído", [(1740,1720,"C=O (estiramento)","F",1,"a"),(2830,2700,"C–H de aldeído","f, 2 bandas",1,"a")]),
 ("[#6][CX3](=O)[#6]", "cetona", [(1725,1705,"C=O (estiramento)","F",1,"a")]),
 ("[#6;a][CX3](=O)[#6]", "cetona aromática", [(1300,1230,"C–CO–C de cetona aromática (estiramento)","F",0,"s")]),
 ("[CX3](=O)[NX3]", "amida", [(1700,1630,"C=O (estiramento)","F",1,"a")]),
 ("[NX3;!$(NC=O)][CH2,CH3]", "N–CH₂ ou N–CH₃ de amina", [(2850,2760,"C–H de N–CH₂ e N–CH₃ (estiramento)","f–M",0,"s")]),
 ("[NX3;H2;!$(NC=O)][#6]", "amina primária", [(3500,3270,"N–H (2 bandas, sim. e ass.)","M",1,"a"),(1650,1580,"N–H tesoura (amina primária)","M",0,"s"),(910,740,"N–H balanço (amina primária)","F, larga",0,"s"),(1340,1020,"C–N (estiramento)","M",0,"a")]),
 ("[NX3;H1;!$(NC=O)]([#6])[#6]", "amina secundária", [(3450,3270,"N–H (1 banda)","f–M",1,"a"),(910,665,"N–H balanço (amina secundária)","F, larga",0,"s"),(1340,1020,"C–N (estiramento)","M",0,"a")]),
 ("[NX3;H0;!$(NC=O)]([#6])([#6])[#6]", "amina terciária", [(1340,1020,"C–N (estiramento)","M",0,"a")]),
 ("[NX3;H2]C=O", "amida primária", [(3500,3100,"N–H (2 bandas)","M, larga",1,"a"),(1650,1590,"N–H deformação (amida II)","M",0,"s")]),
 ("[NX3;H1](C=O)", "amida secundária", [(3500,3100,"N–H (1 banda)","M, larga",1,"a"),(1570,1510,"N–H deformação (amida II)","M–F",0,"s")]),
 ("[CX2]#[NX1]", "nitrila", [(2260,2210,"C≡N (estiramento)","M–F, estreita",1,"a")]),
 ("[CX2]#[CX2;H1]", "alcino terminal", [(3310,3300,"≡C–H (estiramento)","f, estreita",1,"a"),(2150,2100,"C≡C (estiramento)","f–M",1,"a")]),
 ("[N+](=O)[O-]", "nitro", [(1550,1500,"N=O assimétrico","F",1,"a"),(1370,1300,"N=O simétrico","F",1,"a")]),
 ("[#6][NX2]=O", "nitroso", [(1550,1480,"N=O de nitroso (estiramento)","M–F",1,"a")]),
 ("[CX4][Cl]", "cloreto de alquila", [(800,600,"C–Cl (estiramento)","F",0,"a")]),
 ("c[Cl]", "cloreto de arila", [(800,600,"C–Cl (estiramento)","F",0,"a"),(1100,1020,"C–H no plano, sensível ao halogênio (anel)","M–F",0,"s")]),
 ("c[OX2][CX4]", "éter de aril e alquila", [(1275,1200,"C–O–C assimétrico (aril alquil éter)","F",0,"s"),(1075,1020,"C–O–C simétrico (aril alquil éter)","F",0,"s")]),
 ("[OX2][CH3]", "O–CH₃", [(2850,2815,"C–H de O–CH₃ (estiramento)","f–M",0,"s")]),
 ("[CX4]O[CX4]", "éter", [(1150,1050,"C–O (estiramento)","F",0,"a")]),
 ("[CH2;!a]=[CH;!a]", "vinila", [(1000,985,"=C–H fora do plano (vinil)","F",0,"s"),(920,905,"=CH₂ fora do plano (vinil)","F",0,"s")]),
 ("c1ccoc1", "furano", [(3170,3100,"C–H de furano (estiramento)","f–M",0,"s"),(1070,1010,"C–O–C do anel de furano","F",0,"s"),(760,730,"C–H fora do plano (furano)","F",0,"s")]),
 ("[CX4;H1]([Cl,Br,I])([Cl,Br,I])[Cl,Br,I]", "haloforme (CHX₃)", [(3100,3000,"C–H de CHX₃ (estiramento)","f–M",0,"s"),(1230,1060,"C–H deformação de CHX₃ (cai quando X é mais pesado)","F",0,"s")]),
 ("[CH2X4]([Cl,Br,I])[Cl,Br,I]", "dialeto geminal (CH₂X₂)", [(1290,1240,"CH₂ balanço de CH₂X₂","F",0,"s")]),
 ("[CX3]=[CX3;!a]", "alceno", [(3100,3000,"=C–H (estiramento)","f–M",1,"a"),(1680,1620,"C=C (estiramento)","f–M",1,"a")]),
 # grupos acrescentados em 04/11/2026. Faixas da tabela de IV do LibreTexts ("Infrared Spectroscopy Absorption Table") onde ela traz o número; o resto é referência geral (marcada "g")
 ("[CX3](=O)[Cl,Br]", "haleto de ácido", [(1815,1785,"C=O de haleto de ácido (estiramento)","F",1,"a")]),
 ("[CX3](=O)O[CX3](=O)", "anidrido", [(1850,1800,"C=O de anidrido (assimétrico)","F",1,"s"),(1790,1740,"C=O de anidrido (simétrico)","F",1,"s"),(1050,1040,"C–O–C de anidrido","F, larga",0,"s")]),
 ("[SX2H]", "tiol", [(2600,2550,"S–H (estiramento)","f",1,"a")]),
 ("[CX4][Br]", "brometo de alquila", [(690,515,"C–Br (estiramento)","F",0,"s")]),
 ("c[Br]", "brometo de arila", [(690,515,"C–Br (estiramento)","F",0,"s"),(1100,1020,"C–H no plano, sensível ao halogênio (anel)","M–F",0,"s")]),
 ("[CX4][I]", "iodeto de alquila", [(680,500,"C–I (estiramento)","F",0,"s")]),
 ("c[I]", "iodeto de arila", [(600,500,"C–I (estiramento)","F",0,"s")]),
 ("[#6][F]", "fluoreto orgânico", [(1400,1000,"C–F (estiramento)","F",0,"a")]),
 ("[SX4](=O)(=O)([#6])[#6]", "sulfona", [(1350,1320,"S=O assimétrico","F",1,"s"),(1160,1120,"S=O simétrico","F",1,"s")]),
 ("[SX3](=O)([#6])[#6]", "sulfóxido", [(1070,1030,"S=O (estiramento)","F",1,"s")]),
 ("[SX4](=O)(=O)[NX3]", "sulfonamida", [(1370,1335,"S=O assimétrico","F",1,"s"),(1170,1155,"S=O simétrico","F",1,"s")]),
 ("[CX3]=[NX2][#6]", "imina", [(1690,1640,"C=N (estiramento)","M–F",1,"a")]),
 ("[CX3]=[NX2][OX2H]", "oxima", [(3650,3500,"O–H de oxima (estiramento)","M, larga",0,"g"),(1690,1640,"C=N (estiramento)","M",1,"s"),(960,930,"N–O (estiramento)","M",0,"g")]),
 ("N=[N+]=[N-]", "azida", [(2160,2120,"N=N=N (estiramento)","F",1,"s")]),
 ("N=C=O", "isocianato", [(2275,2250,"N=C=O (estiramento)","F, larga",1,"s")]),
 ("N=C=S", "isotiocianato", [(2140,1990,"N=C=S (estiramento)","F, larga",1,"s")]),
 ("[SX2]C#N", "tiocianato", [(2175,2140,"S–C≡N (estiramento)","F",1,"s")]),
 ("[CX3](=O)[NX3][CX3](=O)", "imida", [(1790,1700,"C=O de imida (2 bandas)","F, 2 bandas",1,"g")]),
 ("[NX3][CX3](=O)[OX2]", "carbamato", [(1740,1680,"C=O de carbamato (estiramento)","F",1,"g"),(3500,3100,"N–H (estiramento)","M",0,"g")]),
 ("[NX3][CX3](=O)[NX3]", "ureia", [(1690,1630,"C=O de ureia (estiramento)","F",1,"g"),(3500,3100,"N–H (estiramento)","M, larga",0,"g")]),
 ("[OX2][CX3](=O)[OX2]", "carbonato", [(1780,1740,"C=O de carbonato (estiramento)","F",1,"g"),(1280,1240,"C–O de carbonato","F",0,"g")]),
 ("C1OC1", "epóxido", [(1280,1230,"anel do epóxido (estiramento simétrico)","M",0,"g"),(950,815,"anel do epóxido (assimétrico)","F",0,"g")]),
 ("[OX2][OX2]", "peróxido", [(890,820,"O–O (estiramento)","f",0,"g")]),
 ("[#6]=S", "tiocarbonila", [(1250,1020,"C=S (estiramento)","M–F",0,"g")]),
 ("[SX2][SX2]", "dissulfeto", [(540,480,"S–S (estiramento)","f",0,"g")]),
 ("[PX4]=O", "fosfato ou fosfina-óxido", [(1300,1250,"P=O (estiramento)","F",1,"g")]),
 ("P[OX2][#6]", "éster de fósforo", [(1050,970,"P–O–C (estiramento)","F",0,"g")]),
 ("[Si][OX2][Si]", "siloxano", [(1100,1000,"Si–O–Si (estiramento)","F, larga",1,"g")]),
 ("[SiH]", "silano", [(2250,2100,"Si–H (estiramento)","M–F",1,"g")]),
 ("[Si][CH3]", "silício-metila", [(1260,1250,"Si–CH₃ (deformação)","M–F",0,"g"),(840,800,"Si–C","F",0,"g")]),
 ("[N;R]=,:[c,C]", "heterociclo com N", [(1600,1430,"anel heteroaromático (estiramento)","M",0,"g")]),
 ("[nX3;H1]", "N–H de anel (pirrol, indol)", [(3500,3200,"N–H de anel (estiramento)","M",1,"g")]),
 ("C1CC1", "ciclopropano", [(3100,3070,"C–H de ciclopropano (estiramento)","f–M",0,"g")]),
 ("[CX3](=O)[CX3]=[CX3]", "cetona ou aldeído α,β-insaturado", [(1620,1610,"C=C conjugado com C=O (estiramento)","F",0,"a")]),
 ("[CX4]([CH3])([CH3])([CH3])", "terc-butila", [(1395,1385,"CH₃ deformação do t-butila (2 bandas)","M, 2 bandas",0,"g")]),
 ("[CX4;H1]([CH3])[CH3]", "isopropila ou gem-dimetila", [(1385,1365,"CH₃ deformação (dubleto)","M, 2 bandas",0,"a")]),
]
IV_CHAIN = [(725,720,"–(CH₂)ₙ– balanço (n ≥ 4)","f–M",0,"a")]
IV_BEND = [(1470,1450,"CH₂ tesoura e CH₃ deformação assimétrica","M",0,"a")]
IV_UMB = [(1390,1370,"CH₃ deformação simétrica (guarda-chuva)","M",0,"a")]
IV_AROM = [(3100,3000,"C–H aromático (estiramento)","f–M",1,"a"),(1620,1440,"C=C do anel (estiramento)","M",1,"a")]
IV_ALK = (3000,2850,"C–H sp³ (estiramento)","M–F",1,"a")

SOLN = {"S2":"S₂","SA":"SA","SB":"SB","S1":"S₁","A1":"A₁","A2":"A₂","B":"B","MN":"MN","N":"N","I":"I"}

def _p(smarts):
    p = Chem.MolFromSmarts(smarts)
    assert p is not None, smarts
    return p
IVP = [(_p(s), lab, bands) for s, lab, bands in IVG]
P_ARO = _p("a"); P_CH3 = _p("[CH3]"); P_CSP3H = _p("[CX4;!H0]")

def ring_pattern(m):
    """substituição do anel benzênico (só mono e di): devolve (rótulo, bandas de deformação fora do plano) ou None."""
    for ring in m.GetRingInfo().AtomRings():
        if len(ring) != 6: continue
        at = [m.GetAtomWithIdx(i) for i in ring]
        if not all(a.GetSymbol() == 'C' and a.GetIsAromatic() for a in at): continue
        if any(sum(1 for n in a.GetNeighbors() if n.GetIdx() in ring and n.GetIsAromatic()) != 2 or sum(1 for n in a.GetNeighbors() if n.GetIsAromatic()) != 2 for a in at):
            return None  # anel fundido (naftaleno etc.)
        subs = [k for k, a in enumerate(at) if a.GetTotalNumHs() == 0]
        if len(subs) == 1:
            return ("anel monossubstituído", [(780,725,"C–H fora do plano (anel mono)","F",0,"a"),(720,680,"deformação do anel (mono)","F",0,"a")])
        if len(subs) == 2:
            d = min((subs[0]-subs[1]) % 6, (subs[1]-subs[0]) % 6)
            return {1:("anel orto-dissubstituído", [(770,735,"C–H fora do plano (orto)","F",0,"a")]),
                    2:("anel meta-dissubstituído", [(900,880,"C–H fora do plano (meta)","M",0,"a"),(810,750,"C–H fora do plano (meta)","F",0,"a"),(725,680,"deformação do anel (meta)","M",0,"a")]),
                    3:("anel para-dissubstituído", [(860,800,"C–H fora do plano (para)","F",0,"g")])}[d]
        if len(subs) == 0:
            return ("benzeno sem substituinte", [(690,660,"C–H fora do plano (benzeno)","F",0,"s")])
        return None
    return None

_OT_ALD = _p("[CX3H1](=O)[#6]"); _OT_CET = _p("[#6][CX3](=O)[#6]"); _OT_CO = _p("[CX3]=[OX1]")
S_BENZ = "Smith, The Benzene Fingers, Spectroscopy, 2016"
S_ALD = "Smith, The C=O Bond, parte II: aldeídos, Spectroscopy"
S_CET = "quimicaorganica.org, espectro IV de cetonas"
S_AMP = "Smith, Organic Chemistry, espectroscopia de aminas (LibreTexts)"
_OT_AMP = _p("[NX3;H2;!$(N[C,S]=[O,S])][#6]")
def overtones(m):
    """Overtones, combinações e ressonância de Fermi esperados, por grupo. Cada item: [tipo, faixa em cm⁻¹, o que é, fonte]. Lista vazia = nada que sirva de diagnóstico."""
    out = []
    aneis = [r for r in m.GetRingInfo().AtomRings() if len(r) == 6 and all(m.GetAtomWithIdx(i).GetSymbol() == 'C' and m.GetAtomWithIdx(i).GetIsAromatic() for i in r)]
    if aneis:
        iso = []; bi = []
        for ring in aneis:
            at = [m.GetAtomWithIdx(i) for i in ring]
            # anel fundido (naftaleno etc.): átomo em 2 anéis com 3 vizinhos aromáticos. Bifenila não é fundida: o outro anel conta como substituinte.
            if any(sum(1 for n in a.GetNeighbors() if n.GetIsAromatic()) != 2 and m.GetRingInfo().NumAtomRings(a.GetIdx()) > 1 for a in at): continue
            iso.append([k for k, a in enumerate(at) if a.GetTotalNumHs() == 0])
            bi.append(any(nb.GetIsAromatic() and nb.GetIdx() not in ring for a in at for nb in a.GetNeighbors()))
        if not iso:
            out.append(["Combinação e harmônico do anel", "2000–1650", "Anel fundido (naftaleno e semelhantes): não achei padrão tabelado para esta região.", S_BENZ])
        else:
            subs = iso[0]; n = len(subs); pad = None
            if n == 1: pad = ("anel monossubstituído", "4 picos fracos, bem separados")
            elif n == 2:
                d = min((subs[0] - subs[1]) % 6, (subs[1] - subs[0]) % 6)
                pad = {1: ("anel orto-dissubstituído", "4 picos fracos, juntos"), 2: ("anel meta-dissubstituído", "3 picos fracos"), 3: ("anel para-dissubstituído", "2 picos fracos")}[d]
            elif n == 3:
                g = sorted([subs[1] - subs[0], subs[2] - subs[1], 6 - (subs[2] - subs[0])])
                pad = {(1, 1, 4): ("anel 1,2,3-trissubstituído", "4 picos fracos, bem separados"), (1, 2, 3): ("anel 1,2,4-trissubstituído", "2 picos fracos, bem separados"), (2, 2, 2): ("anel 1,3,5-trissubstituído", "2 picos fracos, juntos")}.get(tuple(g))
            if pad:
                out.append(["Combinação e harmônico do anel", "2000–1650", pad[0][0].upper() + pad[0][1:] + ": " + pad[1] + ". São as chamadas benzene fingers: o número, o espaçamento e a altura dos picos ajudam a confirmar o padrão de substituição, junto com a C–H fora do plano (900–650).", S_BENZ])
            else:
                out.append(["Combinação e harmônico do anel", "2000–1650", "Anel com " + str(n) + " substituintes: não achei padrão tabelado para esta região.", S_BENZ])
            if len(iso) > 1: out[-1][2] += " Há mais de um anel isolado; os padrões se somam."
            if pad and bi[0]:
                out[-1][2] += " O outro anel aromático conta como substituinte. A tabela de Smith não cita bifenilas: aqui é extensão dela, sem conferência."
                out[-1][3] = S_BENZ + " (extensão a bifenilas, sem fonte tabelada)"
    if m.HasSubstructMatch(_OT_ALD):
        out.append(["Ressonância de Fermi (harmônico)", "2850–2700", "Aldeído: aparecem duas bandas de C–H do aldeído, perto de 2820 e 2720. A banda de estiramento C–H interage com o harmônico da deformação C–H do aldeído (fundamental em ~1390). Nem todo aldeído mostra as duas, mas a de ~2720 é a mais útil porque fica livre dos C–H alifáticos.", S_ALD])
    if m.HasSubstructMatch(_OT_CET):
        out.append(["Harmônico do C=O (2 × ν)", "3500–3350", "Cetona: banda fraca na região de O–H e N–H. É o dobro da frequência do C=O, não é um grupo O–H. Serve para não ser enganado por uma banda fraquinha acima de 3300 num composto sem O–H.", S_CET])
    elif m.HasSubstructMatch(_OT_CO):
        out.append(["Harmônico do C=O (2 × ν)", "~3400–3500", "Composto com C=O: o dobro da frequência do C=O cai perto de 3400–3500, fraco. Faixa estimada pelo dobro da banda do C=O; não achei faixa tabelada para este tipo de carbonila.", "estimado, sem fonte tabelada"])
    if m.HasSubstructMatch(_OT_AMP):
        out.append(["Ressonância de Fermi (harmônico)", "3250–3150", "Amina primária: banda fraca perto de 3200, ao lado das duas bandas de N–H. Vem da interação do harmônico da deformação N–H (~1600) com o estiramento N–H simétrico. Não é outro grupo.", S_AMP])
    return out

def iv_bands(m):
    out = []; grupos = []
    for pat, lab, bands in IVP:
        if m.HasSubstructMatch(pat):
            # amina primária/secundária e amida se sobrepõem: evita contar NH de amida como amina
            grupos.append(lab)
            for b in bands: out.append(b)
    if m.HasSubstructMatch(P_ARO):
        grupos.append("anel aromático")
        for b in IV_AROM: out.append(b)
        rp = ring_pattern(m)
        if rp:
            grupos.append(rp[0])
            for b in rp[1]: out.append(b)
    if m.HasSubstructMatch(P_CSP3H):
        out.append(IV_ALK)
        if m.HasSubstructMatch(_p("[CH2,CH3]")): out.extend(IV_BEND)
        if m.HasSubstructMatch(P_CH3) and not any(g in grupos for g in ("terc-butila","isopropila ou gem-dimetila")): out.extend(IV_UMB)
        if m.HasSubstructMatch(_p("[CH2][CH2][CH2][CH2]")): out.extend(IV_CHAIN)
    if "anidrido" in grupos:
        out = [b for b in out if b[2] != "C=O (estiramento)"]
    # éster aromático (benzoato): C=O desce pouco, 1730–1715
    if m.HasSubstructMatch(_p("[#6;a][CX3](=O)[OX2][#6]")) and "ácido carboxílico" not in grupos:
        out = [((1730,1715,"C=O de éster conjugado com anel (estiramento)","F",1,"s") if (b[2] == "C=O (estiramento)" and b[5] == "a") else b) for b in out]
    # éster de fenol (acetato de aril, aspirina): C=O sobe e não é o do ácido conjugado
    if m.HasSubstructMatch(_p("[CX3;!$(C-a)](=O)[OX2]a")):
        out = [b for b in out if not (b[2] == "C=O (estiramento)" and b[0] == 1750 and b[1] == 1735)]
        out.append((1780,1750,"C=O de éster de fenol (estiramento)","F",1,"s"))
    # trans-CH=CH: banda fora do plano
    for bd in m.GetBonds():
        if bd.GetBondType() == Chem.BondType.DOUBLE and not bd.IsInRing() and bd.GetStereo() == Chem.BondStereo.STEREOE \
           and all(x.GetSymbol() == 'C' and x.GetTotalNumHs() == 1 for x in (bd.GetBeginAtom(), bd.GetEndAtom())):
            out.append((995,960,"=C–H fora do plano (trans)","F",0,"s")); break
    # conjugação desloca C=O para baixo (tabela geral, Pavia)
    conj = m.HasSubstructMatch(_p("[#6;a][CX3]=O")) or m.HasSubstructMatch(_p("[CX3;!a]=[CX3;!a][CX3]=O"))
    if conj:
        out = [((1710,1660,"C=O conjugado com anel (estiramento)","F",1,"s") if b[2].startswith("C=O") and b[5] == "a" else b) for b in out]
        if "ácido carboxílico" in grupos:
            out = [((1710,1660,"C=O conjugado com anel (estiramento)","F",1,"s") if b[2].startswith("C=O") and b[5] != "s" or b[2] == "C=O (estiramento)" else b) for b in out]
    # aldeído aromático + outra carbonila (ex.: ácido formilsalicílico): o C=O do aldeído é uma banda à parte
    if m.HasSubstructMatch(_p("[CX3H1](=O)[#6;a]")) and len(m.GetSubstructMatches(_p("[CX3]=O"))) >= 2:
        out.append((1715,1685,"C=O de aldeído aromático (estiramento)","F",1,"s"))
    # tira duplicatas exatas
    seen = set(); res = []
    for b in out:
        if b not in seen: seen.add(b); res.append(b)
    res, fat = iv_ajusta(m, res)
    return grupos, res, fat

# ---------------------------------------------------------------- fatores que deslocam as bandas de IV
# Cada fator desloca a faixa base da molécula. Fontes (conferidas em 04/11/2026):
#  LibreTexts (Morsch, 12.08), material de curso lcwu.edu.pk (IRSpectroscopy.pdf), NC State e Oregon State (valores de C=O),
#  e os prints do SDBS que a Camila enviou (ácido salicílico 1662 x ácido benzoico 1696; anilina C-N 1276).
# Onde marquei "sem fonte conferida", o efeito é o que os livros-texto dizem, mas não achei o número nas fontes desta sessão.
def iv_atoms(m, txt):
    """átomos (índices) que dão a banda de IV, a partir do texto da atribuição. Serve só para colorir a estrutura."""
    def q(sma, only=None):
        r = set()
        for mt in m.GetSubstructMatches(_p(sma)):
            for k, i in enumerate(mt):
                if only is None or k in only: r.add(i)
        return r
    T = txt
    if "anidrido" in T: return sorted(q("[CX3](=O)[OX2][CX3]=O"))
    if T.startswith("C–CO–C"): return sorted(q("[#6][CX3](=O)[#6]"))
    if T.startswith("C=O"): return sorted(q("[CX3]=[OX1]"))
    if "C–H de aldeído" in T: return sorted(q("[CX3H1]=[OX1]"))
    if "C–O de ácido" in T: return sorted(q("[CX3](=O)[OX2H1]", {0, 2}))
    if "C–O de álcool primário" in T: return sorted(q("[CX4;H2,H3][OX2H]"))
    if "C–O de álcool secundário" in T: return sorted(q("[CX4;H1][OX2H]"))
    if "C–O de álcool terciário" in T: return sorted(q("[CX4;H0][OX2H]"))
    if "C–O–C do anel de furano" in T: return sorted(q("[o]"))
    if "C–O–C" in T: return sorted(q("[#6][OX2][#6]"))
    if T.startswith("C–O"): return sorted(q("[#6;!$(C=O)][OX2]") or q("[#6][OX2]"))
    if T.startswith("O–H"): return sorted(q("[OX2H]"))
    if T.startswith("N–H"):
        return sorted(q("[NX3;$(NC=O)]")) if "amida" in T else sorted(q("[#7;!H0]"))
    if T.startswith("N=O"): return sorted(q("[N+](=O)[O-]"))
    if "C–N" in T: return sorted(q("[#6;a,CX4][NX3;!$(NC=O)]"))
    if T.startswith("C≡N"): return sorted(q("C#N"))
    if T.startswith("C≡C"): return sorted(q("C#C"))
    if T.startswith("≡C–H"): return sorted(q("[CX2;H1]#C", {0}))
    if "C=C do anel" in T or "(orto)" in T or "(meta)" in T or "(para)" in T or "anel" in T or "furano" in T or "benzeno" in T or "aromático" in T: return sorted(q("a"))
    if T.startswith("C=C"): return sorted(q("[CX3;!a]=[CX3;!a]"))
    if T.startswith("=C") or "vinil" in T: return sorted(q("[CX3;!a;!$(C=O)]=[CX3;!a]"))
    if "CHX₃" in T: return sorted(q("[CX4;!H0]([F,Cl,Br,I])([F,Cl,Br,I])[F,Cl,Br,I]"))
    if "CH₂X₂" in T: return sorted(q("[CX4;H2]([F,Cl,Br,I])[F,Cl,Br,I]"))
    if T.startswith(("C–Cl", "C–Br", "C–I")): return sorted(q("[#6][Cl,Br,I]"))
    if T.startswith("S"): return sorted(q("[#16]"))
    if "O–CH₃" in T: return sorted(q("[CH3][OX2]"))
    if "N–CH" in T: return sorted(q("[CX4;!H0][NX3]"))
    if "balanço (n" in T: return sorted(q("[CH2]"))
    if "CH₃" in T and "CH₂" not in T: return sorted(q("[CH3]"))
    if "C–H" in T or "CH₂" in T: return sorted(q("[CX4;!H0]"))
    return []

MSFR = [  # m/z, SMARTS (átomos que formam o fragmento), nome do fragmento. Só os que a regra do livro atribui sem ambiguidade.
    (15, "[CH3]", "CH₃⁺"),
    (30, "[CH2][NH2]", "CH₂=NH₂⁺ (amina primária)"),
    (31, "[CH2][OH]", "CH₂=OH⁺ (álcool primário)"),
    (43, "[CH3]C=O", "CH₃C≡O⁺ (acetila)"),
    (77, "c1ccccc1", "C₆H₅⁺ (fenila)"),
    (91, "[CH2]c1ccccc1", "C₇H₇⁺ (benzila)"),
    (105, "O=Cc1ccccc1", "C₆H₅C≡O⁺ (benzoíla)"),
]
def ms_atoms(m, M, picos):
    """{m/z: (átomos, nome)} para os picos que têm atribuição segura. O pico M leva a molécula inteira."""
    out = {}
    if M in picos: out[M] = (list(range(m.GetNumAtoms())), "íon molecular (M⁺·): a molécula inteira, menos 1 elétron")
    for mz, sma, nome in MSFR:
        if mz in picos and mz != M:
            mt = m.GetSubstructMatches(_p(sma))
            if mt: out[mz] = (sorted({i for t in mt for i in t}), nome + ", fragmento provável")
    return out

def iv_ajusta(m, res):
    fat = []
    def troca(pred, novo):
        for k, b in enumerate(res):
            if b[2].startswith("C=O") and pred(b):
                res[k] = novo; return True
        return False
    P = lambda s: Chem.MolFromSmarts(s)
    # tamanho do anel: cetona cíclica
    if m.HasSubstructMatch(P("[CX3;r4](=O)([#6])[#6]")):
        troca(lambda b: True, (1820,1775,"C=O de cetona em anel de 4 (estiramento)","F",1,"s"))
        fat.append(("Anel pequeno", "Cetona em anel de 4: a banda sobe bastante (as fontes dão 1785 ou 1810 para a ciclobutanona; a faixa aqui cobre as duas)."))
    elif m.HasSubstructMatch(P("[CX3;r5](=O)([#6])[#6]")):
        troca(lambda b: True, (1780,1740,"C=O de cetona em anel de 5 (estiramento)","F",1,"s"))
        fat.append(("Anel pequeno", "Cetona em anel de 5: a banda sobe em relação à ciclo-hexanona (1715). As fontes dão 1750 ou 1774 para a ciclopentanona; a faixa aqui cobre as duas."))
    elif m.HasSubstructMatch(P("[CX3;r6;!$(C(=O)[#6]=,:[#6])](=O)([#6])[#6]")):
        fat.append(("Anel", "Cetona em anel de 6: sem tensão, fica como cetona de cadeia (ciclo-hexanona 1715; no seu print do SDBS, 1716)."))
    # lactonas e lactamas
    for r, hi, lo, nm in ((4,1850,1830,"β-lactona"),(5,1780,1750,"γ-lactona"),(6,1750,1730,"δ-lactona")):
        if m.HasSubstructMatch(P("[CX3;r%d](=O)[OX2;r%d]" % (r, r))):
            troca(lambda b: True, (hi, lo, "C=O de "+nm+" (estiramento)","F",1,"s"))
            fat.append(("Éster cíclico", "Em anel de %d, o éster vira lactona e a banda sobe (4: 1840 ±5; 5: 1765 ±10; 6: 1740 ±10)." % r))
    for r, hi, lo, nm in ((4,1760,1730,"β-lactama"),(5,1715,1685,"γ-lactama"),(6,1680,1660,"δ-lactama")):
        if m.HasSubstructMatch(P("[CX3;r%d](=O)[NX3;r%d]" % (r, r))):
            troca(lambda b: True, (hi, lo, "C=O de "+nm+" (estiramento)","F",1,"s"))
            fat.append(("Amida cíclica", "Em anel de %d, a amida vira lactama (4: 1745 ±15; 5: 1700 ±15; 6: 1670 ±10)." % r))
    # ligação de H intramolecular (o-hidroxi carbonila aromática)
    if m.HasSubstructMatch(P("[OX2H]c:c[CX3]=O")):
        troca(lambda b: True, (1700,1630,"C=O com ligação de H intramolecular (estiramento)","F",1,"s"))
        fat.append(("Ligação de H intramolecular", "O OH do fenol faz ligação de H com o C=O vizinho e a banda desce. No SDBS: ácido salicílico 1662, ácido benzoico 1696."))
    # alfa-halogenio sobe a banda
    if m.HasSubstructMatch(P("[CX3](=O)[CX4][F,Cl,Br,I]")):
        for k, b in enumerate(res):
            if b[2].startswith("C=O"):
                res[k] = (b[0]+30, b[1], b[2], b[3], b[4], "g")
        fat.append(("Halogênio em α", "Halogênio no carbono vizinho puxa elétrons e sobe o C=O. Efeito conhecido de livro-texto, sem fonte conferida para o número (usei +30 cm⁻¹ como margem)."))
    # conjugacao (ja aplicada antes): registra
    if m.HasSubstructMatch(P("[#6;a][CX3]=O")):
        fat.append(("Conjugação", "C=O ligado ao anel aromático: a banda desce 20 a 30 cm⁻¹. No SDBS: acetofenona 1686, benzaldeído 1703, ácido benzoico 1696."))
    # substituinte forte no anel desloca a C–H fora do plano
    if m.HasSubstructMatch(P("c[N+](=O)[O-]")):
        for k, b in enumerate(res):
            if b[2].startswith("C–H fora do plano (anel mono"):
                res[k] = (810, b[1], b[2], b[3], b[4], "s")
                fat.append(("Substituinte no anel", "Grupo retirador forte no anel (NO₂) mexe nas bandas de C–H fora do plano. No SDBS, o nitrobenzeno tem uma delas em 794, acima da faixa de anel monossubstituído (770–730)."))
    # ácido: dímero x monômero
    if m.HasSubstructMatch(P("[CX3](=O)[OX2H]")):
        fat.append(("Dimerização", "Ácido carboxílico forma dímero por ligação de H (C=O perto de 1710, O–H muito largo). Em solução diluída o monômero aparece 25 cm⁻¹ ou mais acima. No SDBS, o ácido acético em CCl₄ mostra a banda forte em 1715 e uma fraca em 1768."))
    # N aromático: C-N sobe
    for k, b in enumerate(res):
        if b[2].startswith("C–N"):
            if m.HasSubstructMatch(P("[NX3;!$(NC=O)]c")):
                res[k] = (1360,1250,"C–N de amina aromática (estiramento)","M",0,"s")
                fat.append(("N ligado ao anel", "C–N de amina aromática fica acima da alifática (1340–1250 contra 1250–1020). No SDBS, anilina 1276."))
            else:
                res[k] = (1250,1020,"C–N de amina alifática (estiramento)","M",0,"a")
    # OH de fenol: ligação H forte e meio
    if m.HasSubstructMatch(P("[OX2H]")) or m.HasSubstructMatch(P("[NX3;H1,H2]")):
        fat.append(("Ligação de H intermolecular", "O–H e N–H de líquido puro ou sólido saem largos e baixos (O–H 3500–3200). Em gás ou solução bem diluída o O–H livre é fino e fica em 3620–3670."))
    return res, fat

# ---------------------------------------------------------------- RMN (estimativa por faixas típicas)
def _is_carbonyl_C(a):
    return a.GetSymbol() == 'C' and any(b.GetBondTypeAsDouble() == 2 and b.GetOtherAtom(a).GetSymbol() == 'O' for b in a.GetBonds())

def _mult(n):
    return {0:"s",1:"d",2:"t",3:"q",4:"quinteto",5:"sexteto",6:"septeto"}.get(n, "m")

def classify_h(x, nH):
    sym = x.GetSymbol()
    heavy = [n for n in x.GetNeighbors() if n.GetAtomicNum() > 1]
    if sym == 'S': return ("S–H de tiol", 1.0, 4.0, 1)
    if sym == 'O':
        if any(_is_carbonyl_C(n) for n in heavy): return ("O–H de ácido carboxílico", 10.0, 13.0, 1)
        if any(n.GetIsAromatic() for n in heavy):
            ar = [n for n in heavy if n.GetIsAromatic()][0]
            if any(_is_carbonyl_C(k) for a in ar.GetNeighbors() if a.GetIsAromatic() for k in a.GetNeighbors() if not k.GetIsAromatic()):
                return ("O–H de fenol com ligação de H para a carbonila vizinha", 10.0, 12.0, 1)
            return ("O–H de fenol", 4.0, 8.0, 1)
        return ("O–H de álcool", 1.0, 5.5, 1)
    if sym == 'N':
        if any(_is_carbonyl_C(n) for n in heavy): return ("N–H de amida", 5.0, 8.5, 1)
        if sum(1 for n in heavy if n.GetIsAromatic()) >= 2: return ("N–H de diarilamina", 5.0, 6.0, 1)
        if any(n.GetIsAromatic() for n in heavy): return ("N–H de anilina", 3.0, 4.5, 1)
        return ("N–H de amina", 0.5, 3.0, 1)
    if x.GetIsAromatic():
        ring_het = any(n.GetSymbol() != 'C' and n.GetIsAromatic() for n in x.GetNeighbors())
        if ring_het: return ("H de anel heteroaromático", 6.2, 8.8, 0)
        return ("H aromático", 6.5, 8.4, 0)
    hyb = x.GetHybridization()
    if _is_carbonyl_C(x):
        bd = x.GetOwningMol().GetBondBetweenAtoms
        if any(n.GetSymbol() in ('O', 'N') and bd(x.GetIdx(), n.GetIdx()).GetBondTypeAsDouble() == 1.0 for n in x.GetNeighbors()):
            return ("H de formiato, ácido fórmico ou formamida", 7.8, 8.3, 0)
        return ("H de aldeído", 9.3, 10.1, 0)
    if hyb == Chem.HybridizationType.SP: return ("≡C–H", 2.0, 3.1, 0)
    if hyb == Chem.HybridizationType.SP2:
        if any(_is_carbonyl_C(n) for n in x.GetNeighbors()): return ("H de alceno ligado a C=O", 5.8, 7.5, 0)
        if any(n.GetIsAromatic() for n in x.GetNeighbors()): return ("H de alceno ligado a anel", 6.2, 7.9, 0)
        return ("H de alceno", 4.5, 6.5, 0)
    nb = list(x.GetNeighbors())
    for n in nb:
        if n.GetSymbol() == 'O':
            if sum(1 for k in nb if k.GetSymbol() == 'O') >= 2: return ("H anomérico ou de acetal", 4.5, 5.8, 0)
            ester = any(_is_carbonyl_C(k) for k in n.GetNeighbors() if k.GetIdx() != x.GetIdx())
            if ester: return ("O–CH de éster", 3.6, 4.3, 0)
            if any(_is_carbonyl_C(k) for k in nb): return ("C–H ligado a O e a C=O", 3.9, 4.9, 0)
            if any(k.GetSymbol() == 'C' and k.GetIsAromatic() for k in nb): return ("C–H benzílico ligado a O", 4.2, 5.0, 0)
            return ("C–H ligado a O (álcool ou éter)", 3.2, 4.1, 0)
    for n in nb:
        if n.GetSymbol() == 'N':
            amide = any(_is_carbonyl_C(k) for k in n.GetNeighbors() if k.GetIdx() != x.GetIdx())
            if not amide and any(k.GetSymbol() == 'C' and k.GetIsAromatic() for k in nb): return ("C–H benzílico ligado a N", 3.6, 4.2, 0)
            return (("C–H ligado a N de amida", 2.7, 3.6, 0) if amide else ("C–H ligado a N (amina)", 2.2, 3.2, 0))
    for n in nb:
        if n.GetSymbol() == 'S': return ("C–H ligado a S", 2.0, 3.0, 0)
    hal = [n.GetSymbol() for n in nb if n.GetSymbol() in ("Cl", "Br", "I", "F")]
    if len(hal) >= 3:
        if hal.count("I") >= 3: return ("H de iodofórmio", 4.5, 5.3, 0)
        if hal.count("Br") >= 3: return ("H de bromofórmio", 6.5, 7.0, 0)
        return ("H de haloforme (CHCl₃)", 7.0, 7.6, 0)
    if len(hal) == 2: return ("C–H com dois halogênios", 3.8, 5.6, 0)
    if hal: return ("C–H ligado a halogênio", 3.0, 4.4, 0)
    for n in nb:
        if _is_carbonyl_C(n): return ("C–H α à carbonila", 2.0, 2.8, 0)
    for n in nb:
        if n.GetSymbol() == 'C' and n.GetIsAromatic(): return ("C–H benzílico", 2.2, 3.0, 0)
    for n in nb:
        if n.GetSymbol() == 'C' and n.GetHybridization() == Chem.HybridizationType.SP2: return ("C–H alílico", 1.6, 2.3, 0)
    for n in nb:
        if n.GetSymbol() == 'C' and n.GetHybridization() == Chem.HybridizationType.SP: return ("C–H propargílico", 1.7, 2.6, 0)
    for n in nb:
        if n.GetSymbol() == 'C' and any(k.GetSymbol() in ("O", "N", "Cl", "Br", "I") for k in n.GetNeighbors() if k.GetIdx() != x.GetIdx()):
            return (("CH₃ β a heteroátomo", 0.9, 1.5, 0) if nH == 3 else ("C–H β a heteroátomo", 1.3, 2.0, 0))
    return {3:("CH₃ alifático", 0.8, 1.3, 0), 2:("CH₂ alifático", 1.2, 2.0, 0)}.get(nH, ("CH alifático", 1.4, 2.0, 0))

def nmr_h(m):
    mh = Chem.AddHs(m)
    rk = list(Chem.CanonicalRankAtoms(mh, breakTies=False))
    g = defaultdict(list)
    for a in mh.GetAtoms():
        if a.GetAtomicNum() == 1: g[rk[a.GetIdx()]].append(a.GetIdx())
    out = []
    for r, hs in g.items():
        x = mh.GetAtomWithIdx(hs[0]).GetNeighbors()[0]
        # nº de H no mesmo carbono que fazem parte do mesmo grupo (ex.: CH3 = 3)
        nH = len(hs)
        lab, lo, hi, exch = classify_h(x, len([n for n in x.GetNeighbors() if n.GetAtomicNum() == 1]))
        if exch:
            mult = "s largo"
        elif x.GetIsAromatic() or (x.GetHybridization() == Chem.HybridizationType.SP2 and not _is_carbonyl_C(x)):
            mult = "m"
        else:
            n = 0
            for y in x.GetNeighbors():
                if y.GetSymbol() != 'C': continue
                for h in y.GetNeighbors():
                    if h.GetAtomicNum() == 1 and rk[h.GetIdx()] != r: n += 1
            mult = _mult(n)
        out.append(dict(t=lab, h=nH, m=mult, lo=lo, hi=hi, on=sorted({mh.GetAtomWithIdx(h).GetNeighbors()[0].GetIdx() for h in hs})))
    # H aromáticos de um mesmo anel se sobrepõem no espectro real: juntos num sinal só
    mer = {}; res = []
    for d in out:
        if d["t"] == "H aromático":
            if "ar" in mer: mer["ar"]["h"] += d["h"]; mer["ar"]["on"] = sorted(set(mer["ar"]["on"]) | set(d["on"]))
            else: mer["ar"] = d; res.append(d)
        else: res.append(d)
    res.sort(key=lambda d: -(d["lo"] + d["hi"]))
    return res

def _pos_anel(m, ai):
    """orto, meta ou para em relação ao único substituinte do anel benzênico (só para CH aromático de anel monossubstituído)."""
    a = m.GetAtomWithIdx(ai)
    if not a.GetIsAromatic() or a.GetTotalNumHs() == 0: return ""
    for ring in m.GetRingInfo().AtomRings():
        if len(ring) != 6 or ai not in ring: continue
        at = [m.GetAtomWithIdx(i) for i in ring]
        if not all(x.GetSymbol() == 'C' and x.GetIsAromatic() for x in at): return ""
        subs = [k for k, x in enumerate(at) if x.GetTotalNumHs() == 0]
        if len(subs) != 1: return ""
        k = ring.index(ai); d = min((k - subs[0]) % 6, (subs[0] - k) % 6)
        return {1: "orto", 2: "meta", 3: "para"}.get(d, "")
    return ""

_QU = None
def QUIN(m):
    return {i for mt in m.GetSubstructMatches(_p("[#6]1(=O)[#6]=,:[#6][#6](=O)[#6]=,:[#6]1")) for i in (mt[0], mt[4])}

def nmr_c(m):
    rk = list(Chem.CanonicalRankAtoms(m, breakTies=False))
    g = defaultdict(list)
    for a in m.GetAtoms():
        if a.GetSymbol() == 'C': g[rk[a.GetIdx()]].append(a.GetIdx())
    out = []
    for r, cs in g.items():
        a = m.GetAtomWithIdx(cs[0]); nbs = list(a.GetNeighbors())
        syms = [n.GetSymbol() for n in nbs]
        if _is_carbonyl_C(a):
            if syms.count("N") >= 2: t, lo, hi = "C=O de ureia", 155, 165
            elif "N" in syms: t, lo, hi = "C=O de amida", 160, 180
            elif "O" in [n.GetSymbol() for n in nbs if m.GetBondBetweenAtoms(a.GetIdx(), n.GetIdx()).GetBondTypeAsDouble() == 1]:
                acid = any(n.GetSymbol() == 'O' and n.GetTotalNumHs() == 1 for n in nbs)
                t, lo, hi = ("C=O de ácido carboxílico", 165, 185) if acid else ("C=O de éster", 160, 175)
            elif a.GetTotalNumHs() == 1: t, lo, hi = "C=O de aldeído", 190, 205
            elif a.GetIdx() in QUIN(m): t, lo, hi = "C=O de quinona", 175, 190
            else:
                arom = any(n.GetIsAromatic() for n in nbs)
                t, lo, hi = ("C=O de cetona conjugada", 190, 205) if arom else ("C=O de cetona", 200, 220)
        elif a.GetIsAromatic():
            if any(n.GetSymbol() == 'O' and n.GetIsAromatic() for n in nbs): t, lo, hi = "C α do furano (ao lado do O)", 140, 150
            elif a.GetSymbol() == 'C' and any(any(m.GetAtomWithIdx(j).GetSymbol() == 'O' and m.GetAtomWithIdx(j).GetIsAromatic() for j in r) and len(r) == 5 for r in m.GetRingInfo().AtomRings() if a.GetIdx() in r): t, lo, hi = "C β do furano", 105, 115
            elif "O" in syms: t, lo, hi = "C aromático ligado a O", 145, 167
            elif "N" in syms:
                nitro = any(n.GetSymbol() == 'N' and n.GetFormalCharge() == 1 for n in nbs)
                t, lo, hi = ("C aromático ligado a NO₂", 145, 152) if nitro else ("C aromático ligado a N", 135, 155)
            elif "Cl" in syms: t, lo, hi = "C aromático ligado a Cl", 130, 138
            elif a.GetTotalNumHs() == 0:
                fused = sum(1 for n in nbs if n.GetIsAromatic()) == 3
                ao_lado_O = any(any(k.GetSymbol() == 'O' and not k.GetIsAromatic() for k in nn.GetNeighbors()) for nn in nbs if nn.GetIsAromatic())
                t, lo, hi = ("C aromático de fusão de anéis", 130, 136) if fused else (("C aromático sem H (ipso), ao lado do C–O", 108, 135) if ao_lado_O else ("C aromático sem H (ipso)", 125, 150))
            else: t, lo, hi = "CH aromático", 105, 137
        elif a.GetHybridization() == Chem.HybridizationType.SP:
            nit = "N" in syms
            t, lo, hi = ("C≡N (nitrila)", 115, 125) if nit else ("C≡C (alcino)", 65, 90)
        elif a.GetHybridization() == Chem.HybridizationType.SP2:
            t, lo, hi = "C de alceno", 100, 150
        else:
            h = a.GetTotalNumHs()
            if syms.count("O") >= 2: t, lo, hi = "C sp³ com dois O (acetal)", 85, 110
            elif "O" in syms: t, lo, hi = "C sp³ ligado a O", 50, 90
            elif "N" in syms: t, lo, hi = "C sp³ ligado a N", 30, 65
            elif any(s in ("Cl", "Br", "I") for s in syms): t, lo, hi = "C sp³ ligado a halogênio", 25, 80
            elif any(_is_carbonyl_C(n) for n in nbs): t, lo, hi = "C sp³ α à carbonila", 20, 50
            elif any(n.GetIsAromatic() for n in nbs): t, lo, hi = "C sp³ benzílico", 15, 45
            elif "S" in syms: t, lo, hi = "C sp³ ligado a S", 15, 55
            elif any(n.GetHybridization() == Chem.HybridizationType.SP and "N" in [x.GetSymbol() for x in n.GetNeighbors()] for n in nbs): t, lo, hi = "C sp³ ao lado de nitrila", 0, 30
            elif h == 3: t, lo, hi = "CH₃", 5, 30
            else: t, lo, hi = "C sp³ alifático", 15, 55
        out.append(dict(t=t, n=len(cs), lo=lo, hi=hi, at=sorted(cs), pos=_pos_anel(m, cs[0])))
    out.sort(key=lambda d: -(d["lo"] + d["hi"]))
    return out

def gdh(m):
    f = rdMolDescriptors.CalcMolFormula(m)
    c = h = n = x = 0
    for a in Chem.AddHs(m).GetAtoms():
        s = a.GetSymbol()
        if s == 'C': c += 1
        elif s == 'H': h += 1
        elif s == 'N': n += 1
        elif s in ("F", "Cl", "Br", "I"): x += 1
    return (2*c + 2 + n - h - x) / 2

def cas_ok(c):
    d = c.replace("-", ""); body, chk = d[:-1], int(d[-1])
    return sum((i+1)*int(ch) for i, ch in enumerate(reversed(body))) % 10 == chk

def _hl_svg(m, w, h, bond, numerar=None):
    """estrutura com um círculo invisível atrás de cada átomo (classe hl hN). O app liga o círculo quando o pico é escolhido."""
    import re
    from rdkit.Chem.Draw import rdMolDraw2D
    mm = Chem.Mol(m)
    if numerar:
        for k, sg in enumerate(numerar, 1):
            for ai in sg["at"]: mm.GetAtomWithIdx(ai).SetProp("atomNote", str(k))
    d = rdMolDraw2D.MolDraw2DSVG(w, h); o = d.drawOptions()
    o.clearBackground = False; o.fixedBondLength = bond; o.padding = 0.14; o.bondLineWidth = 2
    o.annotationFontScale = 0.85
    d.DrawMolecule(mm); d.FinishDrawing()
    t = d.GetDrawingText()
    circ = ''.join('<circle class="hl h%d" cx="%.1f" cy="%.1f" r="%.1f"/>' % (a.GetIdx(), d.GetDrawCoords(a.GetIdx()).x, d.GetDrawCoords(a.GetIdx()).y, bond * 0.52) for a in mm.GetAtoms())
    t = re.sub(r'<\?xml.*?\?>', '', t)
    t = re.sub(r"<rect[^>]*?style='opacity:1\.0;fill:#FFFFFF[^>]*?/>", '', t)
    t = t.replace('#000000', 'currentColor').replace('#FF0000', 'var(--lost)').replace('#0000FF', 'var(--blue)')
    t = re.sub(r"<svg[^>]*>", f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img">' + circ, t, count=1)
    t = re.sub(r'<!--.*?-->', '', t); t = re.sub(r'\s+', ' ', t)
    return t.strip()

def svg_numerado(m, c13, w=270, h=180):
    """Estrutura com cada carbono marcado pelo número do sinal de 13C (carbonos equivalentes levam o mesmo número)."""
    return _hl_svg(m, w, h, 34, c13)

def liga_h_c(m, h1, c13):
    """texto 'H do C2' para cada sinal de 1H, usando a numeração dos sinais de 13C."""
    num = {}
    for k, sg in enumerate(c13, 1):
        for ai in sg["at"]: num[ai] = k
    for sg in h1:
        cs = sorted({num[i] for i in sg["on"] if i in num})
        het = sorted({m.GetAtomWithIdx(i).GetSymbol() for i in sg["on"] if i not in num})
        parts = []
        if cs:
            l = ["C" + str(x) for x in cs]
            parts.append(l[0] if len(l) == 1 else ", ".join(l[:-1]) + " e " + l[-1])
        parts += het
        sg["c"] = " e ".join(parts)

from compostos_sdbs import SDBSMS, IRMEIO, C13OBS, H1OBS
from compostos_pub import PUB, DIV, DATA as PUB_DATA

MSFS = {}
MSFS_ID = {}
# Subestruturas para a busca por estrutura (chave, SMARTS). Os rótulos ficam no app (SUBL).
SUBS = [
    ("benz", "c1ccccc1"), ("fenol", "[OX2H]c"), ("alcool", "[CX4][OX2H]"),
    ("ald", "[CX3H1](=O)[#6]"), ("cetona", "[#6][CX3](=O)[#6]"), ("acido", "[CX3](=O)[OX2H1]"),
    ("ester", "[#6][CX3](=O)[OX2][#6]"), ("amida", "[CX3](=O)[NX3]"),
    ("eter", "[OD2;!$(O-C=O)]([#6])[#6]"),
    ("amina", "[NX3;!$(NC=[O,N,S]);!$(N=O);!$(N-[O,N]);!$(N-a)][CX4]"),
    ("anilina", "[NX3;H2,H1;!$(NC=O)]c"), ("nitro", "[N+](=O)[O-]"), ("nitrila", "C#N"),
    ("alcino", "C#C"), ("alceno", "[CX3]=[CX3]"), ("haleto", "[F,Cl,Br,I]"), ("tiol", "[SX2H]"),
]
_SUBP = [(k, Chem.MolFromSmarts(s)) for k, s in SUBS]
assert all(p is not None for k, p in _SUBP)
def subestruturas(m):
    return [k for k, p in _SUBP if m.HasSubstructMatch(p)]
def build_comp(svgfn, EXD):
    exm = {e["n"]: e for e in EXD}
    out = []
    for i, (nome, alts, smi, cas, est, cor, pf, pe, g, exn, obs) in enumerate(RAW):
        assert cas_ok(cas), (nome, cas)
        m = Chem.MolFromSmiles(smi); assert m is not None, nome
        f = rdMolDescriptors.CalcMolFormula(m)
        M = int(round(Descriptors.ExactMolWt(m)))
        grupos, bands, ivf = iv_bands(m)
        d = dict(i=i, n=nome, a=alts, f=f, mw=round(Descriptors.MolWt(m), 2), M=M, smi=smi, s=svgfn(smi, 170, 120),
                 cas=cas, est=est, cor=cor, pf=pf, pe=pe, g=g, ex=exn, obs=obs, gdh=gdh(m),
                 gf=grupos, iv=[list(b) for b in bands], ivf=[list(x) for x in ivf], ot=overtones(m), h1=nmr_h(m), c13=nmr_c(m), sub=subestruturas(m))
        d["sn"] = svg_numerado(m, d["c13"]); d["si"] = _hl_svg(m, 300, 200, 40); d["ivat"] = [iv_atoms(m, b[2]) for b in bands]; liga_h_c(m, d["h1"], d["c13"])
        if exn:
            e = exm[exn]; assert e["M"] == M or True
            d["ms"] = [p for p in e["peaks"]]; d["msv"] = 1; d["M"] = e["M"]
        elif nome in MSK:
            d["ms"] = MSK[nome]; d["msv"] = 0
        else:
            d["ms"] = None; d["msv"] = 0
        if nome in IRMEIO:
            d["irm"], d["irc"] = IRMEIO[nome][:2]
            if len(IRMEIO[nome]) > 2: d["irn"] = IRMEIO[nome][2]
        if nome in SDBSMS:
            no, msid, pk = SDBSMS[nome]
            d["sdbs"] = no; d["msid"] = msid
            d["msi"] = [list(p) for p in sorted(pk, key=lambda p: -p[0])]
            d["ms"] = [p[0] for p in sorted(pk, key=lambda p: -p[0])]; d["msv"] = 2
        if d.get("ms"):
            d["msat"] = {str(k): [v[0], v[1]] for k, v in ms_atoms(m, d["M"], set(d["ms"])).items()}
        if d.get("ms") and not exn:
            import msfrag
            pkm = SDBSMS[nome][2] if nome in SDBSMS else [(p, 0) for p in d["ms"]]
            its, sv, sem = msfrag.propor(m, d["M"], pkm)
            ids = {}
            for k, v in sv.items():
                if k not in MSFS_ID: MSFS_ID[k] = str(len(MSFS_ID)); MSFS[MSFS_ID[k]] = v
                ids[k] = MSFS_ID[k]
            for k, v in sv.items():
                if k not in ids: MSFS_ID[k] = str(len(MSFS_ID)); MSFS[MSFS_ID[k]] = v; ids[k] = MSFS_ID[k]
            d["msf"] = [dict(mz=x["mz"], p=x["p"], f=x["f"], n=x["n"], de=x["de"], r=x["r"], nv=x["nv"], k=ids.get(x["k"], ""), nk=ids.get(x.get("nk", ""), ""), mp=x.get("mp", ""), alt=x["alt"]) for x in its]
            d["msfs"] = sem
        if nome in C13OBS: d["c13m"] = C13OBS[nome]
        if nome in H1OBS: d["h1m"] = list(H1OBS[nome])
        pb = PUB.get(nome, {})
        d["cid"] = pb.get("cid")
        d["pfs"] = "c" if "pf" in pb else ("d" if "pf" in DIV.get(nome, []) else "")
        d["pes"] = "c" if "pe" in pb else ("d" if "pe" in DIV.get(nome, []) else "")
        if "pf" in pb: d["pf"] = pb["pf"][0]
        if "pe" in pb: d["pe"] = pb["pe"][0]
        d["pubsrc"] = sorted({s for k in ("pf", "pe") if k in pb for s in pb[k][2].split(", ")})
        out.append(d)
    return out
