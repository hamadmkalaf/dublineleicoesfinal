# Janelas de fechamento em horas decimais do domingo 25/10/2026 (0 = já fechada antes de domingo).
# Fonte: irishlifedublinmarathon.ie/road-closures, captura de 13/10/2026.
import re
PERCURSO=[  # regex do nome OSM, abre, fecha
 (r"^Leeson Street Lower$",3.5,13),(r"^St\. Stephen's Green$",7,11),(r"^Cuffe Street$",8.25,10.5),
 (r"^Kevin Street (Lower|Upper)$",8.25,10.5),(r"^Patrick Street$",7,11),
 (r"^(Nicholas Street|High Street|Bridge Street (Upper|Lower)|Merchant's Quay|O'Donovan Rossa Bridge|Inns Quay|Arran Quay|Ellis Quay)$",8.25,11),
 (r"^(Blackhall Place|Stoneybatter|North Road|Spa Road|Lords Walk|Zoo Road|Fountain Road)$",8.25,11.5),
 (r"^(Manor Street|Aughrim Street)$",8+10/60,11.5),(r"^North Circular Road$",8,11.5),
 (r"^(Chesterfield Avenue|Phoenix Roundabout|College Road|Tower Road|Knockmaroon (Road|Hill)|Upper Glen Road)$",8.25,13),
 (r"^Castleknock Road$",7+40/60,13),
 (r"^(Chapelizod Gate|Chapelizod Road|Anna Livia Bridge)$",8.25,14),(r"^(Saint Laurence's Road|Sarsfield Road)$",8.5,14),
 (r"^Inchicore Road$",8+25/60,14),(r"^South Circular Road$",8+25/60,14.5),(r"^Dolphin's Barn$",8.75,14.5),
 (r"^Crumlin Road$",8.5,15),(r"^Drimnagh Road$",7,15),(r"^(Walkinstown Road|Walkinstown Roundabout)$",8.75,15),
 (r"^Cromwellsfort Road$",8.75,15.5),(r"^Kimmage Road West$",8,15.5),
 (r"^(Fortfield Road|Templeogue Road|Terenure Road East|Terenure Place)$",9,16),
 (r"^(Orwell Road|Orwell Park|Dartry Road)$",8,16),(r"^Milltown Road$",9+10/60,16),
 (r"^(Clonskeagh Road|Roebuck Road|Foster's Avenue)$",9+10/60,16.5),
 (r"^Nutley Lane$",8+40/60,17),
 (r"^(Merrion Road|Ball's Bridge|Pembroke Road)$",9+25/60,17.5),   # Pembroke Rd: premissa, mesma janela da Merrion Rd
 (r"^(Northumberland Road|McKenny's Bridge)$",3.5,20.5),
 (r"^(Warrington Place|Mount Street Crescent|Mount Street Upper)$",0,20),
]
ABERTAS_NO_PERCURSO=r"^Stillorgan Road$"   # só o corredor de ônibus fecha
LOCAIS=[  # só no centro (bbox abaixo); tira as arestas, não bloqueia o cruzamento
 (r"^Merrion Square South$",0,24),(r"^(Mount Street Crescent|Merrion Square East|Fitzwilliam Street Lower|Herbert Street)$",0,20),
 (r"^(Merrion Street Upper|Merrion Row|Pembroke Street Lower|Lad Lane|Lad Lane Upper)$",3.5,11),
 (r"^(Fitzwilliam Square (East|North|South|West)|Fitzwilliam Place|Fitzwilliam Street Upper|Cumberland Road|Wilton Terrace|Wilton Place|Clanwilliam Place|Baggot Street Lower|Leeson Street Lower|Hatch Street( Upper| Lower)?)$",3.5,13),
 (r"^(Verschoyle Place|Grattan Street|Grattan Court|Wilson's Place|Grant's Row|Fitzwilliam Lane|Baggot Place|Pembroke Row|Hagan's Court|Mount Street Lower|Stephen's Place|Stephen's Lane|James Street East)$",3.5,17.5),
 (r"^(Merrion Square North|Nassau Street|Kildare Street|Clare Street|Warrington Place|Merrion Square West|Herbert Place|Herbert Lane|Powers Court|Holles Street|Percy Place)$",3.5,20),
 (r"^(St\. Stephen's Green|Earlsfort Terrace)$",7,11),
]
BBOX_LOCAIS=(53.329,53.347,-6.265,-6.236)
def janela(nome,tabela):
    for rx,a,f in tabela:
        if re.search(rx,nome): return (a,f)
    return None
