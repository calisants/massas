# Picos de MS lidos dos prints do SDBS (AIST) enviados por Camila em 04/11/2026.
# Intensidades relativas lidas a olho no grafico (erro de uns 3 pontos). So entram picos acima de ~5%.
# Cada entrada: nome -> (numero SDBS, codigo do espectro de MS, [(m/z, intensidade)])
DATA = "04/11/2026"
SDBSMS = {
 "acetona": (319, "MS-IW-7880", [(43,100),(58,64),(15,23),(42,9),(27,6)]),
 "etanol": (1300, "MS-NW-0073", [(31,100),(45,57),(46,25),(27,18),(29,12),(43,10)]),
 "ácido acético": (306, "MS-NW-0080", [(43,100),(45,90),(60,75),(15,17),(42,13),(29,8)]),
 "acetato de etila": (889, "MS-NW-0025", [(43,100),(45,15),(61,15),(70,15),(29,14),(27,7),(15,6),(73,5),(88,5)]),
 "benzaldeído": (672, "MS-NW-5506", [(106,100),(105,94),(77,92),(51,37),(50,18),(78,16),(39,6)]),
 "acetofenona": (722, "MS-NW-2178", [(105,100),(77,73),(120,26),(51,23),(43,13),(78,8),(50,8)]),
 "butanona": (888, "MS2014-05104CW", [(43,100),(72,34),(29,13),(28,11),(27,9),(57,9),(42,5)]),
 "éter dietílico": (2150, "MS2014-05055CW", [(31,100),(59,64),(74,44),(45,43),(29,41),(27,19),(28,14),(43,8)]),
 "ciclo-hexanona": (571, "MS2014-05106CW", [(55,100),(98,92),(42,55),(69,34),(41,31),(70,28),(39,23),(83,16)]),
 "tolueno": (97, "MS-NW-0067", [(91,100),(92,78),(65,12),(39,11),(63,8),(51,7)]),
 "anilina": (905, "MS2014-05102CW", [(93,100),(66,50),(65,24),(92,22),(94,14),(39,10)]),
 "ácido benzoico": (673, "MS-NW-1867", [(105,100),(122,81),(77,75),(51,37),(50,20)]),
 "ácido salicílico": (1149, "MS-NW-0323", [(120,100),(92,57),(138,55),(64,18),(39,12),(121,11)]),
 "nitrobenzeno": (552, "MS-NW-5496", [(77,100),(123,53),(51,43),(50,13),(65,12),(93,11),(30,7)]),
 "fenol": (554, "MS-NW-9060", [(94,100),(66,23),(65,17),(39,14),(40,9),(55,7)]),
 "ácido benzílico": (1713, "MS-NW-0170", [(105,100),(183,95),(77,68),(51,18),(184,14),(165,11),(166,7),(78,7)]),
 "álcool benzílico": (685, "MS-NW-5494", [(79,100),(108,99),(107,68),(77,49),(51,21),(91,17),(39,11),(78,11),(80,10),(65,7)]),
 "ciclo-hexanol": (581, "MS-NW-5520", [(57,100),(82,46),(67,26),(44,24),(41,23),(55,15),(71,13),(56,13),(27,12),(39,12),(29,10)]),
 "dimetilsulfóxido": (2459, "MS2006-03133WA", [(63,100),(78,87),(45,34),(61,17),(46,11),(15,8)]),
 "N,N-dimetilformamida": (324, "MS-NW-0574", [(73,100),(44,84),(42,32),(30,22),(15,16),(28,16),(18,15),(58,8),(43,8),(72,8),(29,8)]),
 "tetra-hidrofurano": (497, "MS-NW-0076", [(42,100),(41,44),(72,38),(71,34),(43,16),(27,16),(39,13),(40,9),(29,8)]),
 "acetato de metila": (2778, "MS2014-05094CW", [(43,100),(74,32),(28,10),(59,9),(42,9),(15,8)]),
 "propanal": (2899, "MS-NW-0778", [(29,100),(28,91),(58,85),(27,59),(26,16),(59,12),(57,8),(30,8),(31,6)]),
 "acetonitrila": (1218, "MS-NW-4393", [(41,100),(40,50),(39,18),(38,9),(14,6)]),
 "2-butanol": (507, "MS2014-05098CW", [(45,100),(59,30),(41,20),(43,12),(31,12),(27,11),(57,8),(29,7),(39,7),(55,6)]),
 "acetamida": (1491, "MS-NW-0720", [(59,100),(44,90),(43,61),(18,55),(28,44),(42,29),(15,24),(17,13),(32,9),(41,8)]),
}

# Meio em que o IV do SDBS foi medido (lido no cabeçalho do print) e se conferi as bandas-chave contra o print.
# irc: 1 = bandas-chave conferidas nas tabelas do print; 2 = conferência parcial (etanol: só vi O–H largo e C–O no gráfico).
IRMEIO = {
 "acetona": ("filme líquido", 1), "etanol": ("filme líquido", 2), "ácido acético": ("solução em CCl₄", 1), "acetato de etila": ("filme líquido", 1),
 "benzaldeído": ("filme líquido", 1), "acetofenona": ("filme líquido", 1), "butanona": ("solução em CCl₄", 1), "éter dietílico": ("filme líquido", 1),
 "ciclo-hexanona": ("filme líquido", 1), "tolueno": ("filme líquido", 1), "anilina": ("solução em CCl₄", 1), "ácido benzoico": ("solução em CCl₄", 1),
 "ácido salicílico": ("pastilha de KBr", 1), "nitrobenzeno": ("filme líquido", 1), "fenol": ("pasta em Nujol", 1),
}
