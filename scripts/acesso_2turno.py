#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plano de acesso ao RDS no 2º turno (25/10/2026), dia da Maratona de Dublin.

Fonte única da geografia do plano. A partir de um só conjunto de pontos e
trechos, gera:

  mapa/acesso_2turno.kml          — camadas para importar no Google My Maps
  mapa/acesso_2turno.html         — a página do plano, com o esquema embutido
  saidas/acesso_2turno.svg        — mapa esquemático (projeção equirretangular)
  saidas/acesso_2turno.json       — pontos, trechos, rotas e janelas horárias
  saidas/acesso_2turno_links.md   — os links do Google Maps, prontos para colar

E **confere** o plano: nenhuma rota recomendada de veículo pode tocar um
trecho fechado ou de sentido único contra o fluxo na janela da maratona. Se
tocar, sai com código 1 — sem `--grava` não escreve nada e serve de teste.

Uso:
    python3 scripts/acesso_2turno.py            # confere e imprime o relatório
    python3 scripts/acesso_2turno.py --grava    # idem, e grava as saídas

Só biblioteca padrão. Nada acessa a rede.

As coordenadas são de referência, lidas de mapa, com precisão da ordem de
30–60 m. Servem para o esquema e para posicionar as camadas no My Maps, onde
cada ponto pode ser arrastado. Não servem para medir distância com precisão.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from urllib.parse import quote_plus

RAIZ = Path(__file__).resolve().parent.parent
GRAVA = "--grava" in sys.argv

# ─────────────────────────────────────────────────────────────────────────────
# 1. Fonte: o plano de trânsito da Garda (reunião de setembro de 2026)
# ─────────────────────────────────────────────────────────────────────────────
FONTE_POLICIA = {
    "percurso": (
        "Milltown Bridge → Milltown Road → Clonskeagh Road → Roebuck Road → "
        "Fosters Avenue → faixa de ônibus inbound da N11 → viaduto da UCD → "
        "faixa de ônibus outbound (no sentido inbound) → direita na Nutley Lane → "
        "esquerda na Merrion Road (inbound) → Pembroke Road → Northumberland Road."
    ),
    "fechados_a_partir_das_10h": [
        "Nutley Lane", "Merrion Road (inbound)", "Shelbourne Road",
        "Haddington Road", "Northumberland Road",
    ],
    "abertos": [
        "Stillorgan Road (N11) — aberta ao tráfego geral o dia todo",
        "Donnybrook Road, Morehampton Road e Leeson Street Upper — abertas",
        "Anglesea Road — aberta ao tráfego do RDS; proibida a saída para a Merrion Road",
        "Merrion Road — só outbound, a partir da Serpentine Avenue",
    ],
    "desvios": [
        "Sandford Road (saindo de Ranelagh) → Eglinton Road → direita na Stillorgan Road",
        "Rock Road inbound → desviado nos Merrion Gates pela Strand Road",
        "Tráfego para o norte da cidade → Ringsend Road via Irishtown, ou East Link via Sean Moore Road",
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# 2. Pontos de referência (lat, lon). Aproximados — ver nota do módulo.
# ─────────────────────────────────────────────────────────────────────────────
P = {
    # RDS
    "rds_merrion":    dict(nome="RDS · portão da Merrion Road (P1, eleitores a pé)", lat=53.32670, lon=-6.22960, tipo="portao"),
    "rds_anglesea":   dict(nome="RDS · Anglesea Gate (veículos, táxi, preferencial)", lat=53.32580, lon=-6.23430, tipo="portao"),
    "rds_simmons":    dict(nome="RDS · entrada Simmonscourt Road (saída de veículos para o sul, a confirmar)", lat=53.32330, lon=-6.22960, tipo="portao"),
    "hall2":          dict(nome="Hall 2 · salão de votação", lat=53.32620, lon=-6.23120, tipo="local"),
    "ring3":          dict(nome="Ring 3 · pátio de fila", lat=53.32560, lon=-6.23080, tipo="local"),
    # cruzamentos
    "ballsbridge":    dict(nome="Ballsbridge · Merrion Rd × Pembroke Rd × Anglesea Rd", lat=53.32870, lon=-6.23180, tipo="cruz"),
    "merrion_serp":   dict(nome="Merrion Rd × Serpentine Ave × Simmonscourt Rd", lat=53.32500, lon=-6.22640, tipo="cruz"),
    "merrion_nutley": dict(nome="Merrion Rd × Nutley Lane", lat=53.32240, lon=-6.22280, tipo="cruz"),
    "merrion_gates":  dict(nome="Merrion Gates (passagem de nível)", lat=53.31650, lon=-6.21250, tipo="cruz"),
    "donnybrook":     dict(nome="Donnybrook · Stillorgan Rd × Anglesea Rd × Donnybrook Rd", lat=53.32000, lon=-6.23820, tipo="cruz"),
    "n11_nutley":     dict(nome="Stillorgan Rd × Nutley Lane (RTÉ)", lat=53.31350, lon=-6.21990, tipo="cruz"),
    "ucd_flyover":    dict(nome="Viaduto da UCD", lat=53.31050, lon=-6.21700, tipo="cruz"),
    "n11_fosters":    dict(nome="Stillorgan Rd × Fosters Ave", lat=53.30580, lon=-6.21200, tipo="cruz"),
    "n11_booterstown":dict(nome="Stillorgan Rd × Booterstown Ave", lat=53.30300, lon=-6.20750, tipo="cruz"),
    "n11_mtmerrion":  dict(nome="Stillorgan Rd × Mount Merrion Ave", lat=53.29950, lon=-6.20150, tipo="cruz"),
    "eglinton_n11":   dict(nome="Eglinton Rd × Stillorgan Rd", lat=53.31950, lon=-6.23950, tipo="cruz"),
    "sandford_egl":   dict(nome="Sandford Rd × Eglinton Rd", lat=53.32250, lon=-6.24700, tipo="cruz"),
    "leeson_bridge":  dict(nome="Leeson Street Bridge", lat=53.33200, lon=-6.25300, tipo="cruz"),
    "morehampton":    dict(nome="Morehampton Road", lat=53.32650, lon=-6.24500, tipo="cruz"),
    "pembroke_north": dict(nome="Pembroke Rd × Northumberland Rd × Lansdowne Rd", lat=53.33050, lon=-6.23520, tipo="cruz"),
    "north_hadd":     dict(nome="Northumberland Rd × Haddington Rd", lat=53.33300, lon=-6.23800, tipo="cruz"),
    "chegada":        dict(nome="Chegada da maratona (Mount Street Upper)", lat=53.33750, lon=-6.24400, tipo="cruz"),
    "milltown":       dict(nome="Milltown Bridge (entrada dos corredores no Dublin 4)", lat=53.31050, lon=-6.24500, tipo="cruz"),
    "clonskeagh":     dict(nome="Clonskeagh Road", lat=53.31100, lon=-6.23400, tipo="cruz"),
    "roebuck":        dict(nome="Roebuck Road", lat=53.30850, lon=-6.22900, tipo="cruz"),
    "fosters":        dict(nome="Fosters Avenue", lat=53.30500, lon=-6.21800, tipo="cruz"),
    "sean_moore":     dict(nome="Strand Rd × Sean Moore Rd", lat=53.33550, lon=-6.21050, tipo="cruz"),
    "irishtown":      dict(nome="Irishtown", lat=53.33800, lon=-6.22300, tipo="cruz"),
    "ringsend_rd":    dict(nome="Ringsend Road", lat=53.34150, lon=-6.23000, tipo="cruz"),
    "east_link":      dict(nome="East Link Bridge", lat=53.34400, lon=-6.21900, tipo="cruz"),
    "rock_rd_sul":    dict(nome="Rock Road (Booterstown)", lat=53.30800, lon=-6.20200, tipo="cruz"),
    # transporte público
    "dart_sandymount":dict(nome="DART · Sandymount", lat=53.32460, lon=-6.21720, tipo="dart"),
    "dart_lansdowne": dict(nome="DART · Lansdowne Road", lat=53.32810, lon=-6.22770, tipo="dart"),
    "dart_sydney":    dict(nome="DART · Sydney Parade", lat=53.32000, lon=-6.21180, tipo="dart"),
    "dart_booterstown":dict(nome="DART · Booterstown", lat=53.31050, lon=-6.20000, tipo="dart"),
    "bus_donnybrook": dict(nome="Ônibus · paradas de Donnybrook (Stillorgan Rd, igreja)", lat=53.32050, lon=-6.23720, tipo="bus"),
    # pontos operacionais do plano
    "trav_serp":      dict(nome="Travessia controlada 1 · Merrion Rd × Serpentine Ave (pedir à Garda)", lat=53.32500, lon=-6.22640, tipo="travessia"),
    "trav_balls":     dict(nome="Travessia controlada 2 · Ballsbridge (pedir à Garda)", lat=53.32870, lon=-6.23180, tipo="travessia"),
    "p0_merrion":     dict(nome="P0 · «descubra sua seção», calçada da Merrion Road (lado do RDS)", lat=53.32690, lon=-6.22990, tipo="posto"),
    "p0_anglesea":    dict(nome="G1 · recepção no Anglesea Gate (posto novo)", lat=53.32575, lon=-6.23400, tipo="posto"),
    "drop_off":       dict(nome="Embarque e desembarque de táxi e preferencial (dentro do Anglesea Gate)", lat=53.32590, lon=-6.23380, tipo="posto"),
}

def ll(*chaves):
    """Lista de (lat, lon) a partir de chaves de P."""
    return [(P[c]["lat"], P[c]["lon"]) for c in chaves]

# ─────────────────────────────────────────────────────────────────────────────
# 3. Malha viária de fundo (só para o esquema) e trechos com estado
# ─────────────────────────────────────────────────────────────────────────────
# estado ∈ {aberto, percurso, fechado, so_outbound, rds_sem_saida, desvio, dart}
TRECHOS = [
    dict(nome="Stillorgan Road (N11)", estado="aberto",
         nota="Aberta ao tráfego geral o dia todo. Corredores nas faixas de ônibus: contar com lentidão.",
         coords=ll("donnybrook") + [(53.3172, -6.2318), (53.3150, -6.2258)] + ll("n11_nutley", "ucd_flyover", "n11_fosters", "n11_booterstown", "n11_mtmerrion")),
    dict(nome="Merrion Road · Ballsbridge → Serpentine Ave", estado="fechado",
         nota="Percurso da maratona. Fechada nos dois sentidos a partir das 10h.",
         coords=ll("ballsbridge", "rds_merrion", "merrion_serp")),
    dict(nome="Merrion Road · Serpentine Ave → Merrion Gates", estado="so_outbound",
         nota="Só outbound (para o sul) a partir da Serpentine Avenue. Inbound fechado.",
         coords=ll("merrion_serp", "merrion_nutley") + [(53.3200, -6.2185)] + ll("merrion_gates")),
    dict(nome="Nutley Lane", estado="fechado", nota="Percurso. Fechada a partir das 10h.",
         coords=ll("merrion_nutley") + [(53.3180, -6.2210)] + ll("n11_nutley")),
    dict(nome="Pembroke Road", estado="fechado", nota="Percurso.",
         coords=ll("ballsbridge", "pembroke_north") + [(53.3325, -6.2408)]),
    dict(nome="Northumberland Road", estado="fechado", nota="Percurso. Fechada a partir das 10h.",
         coords=ll("pembroke_north", "north_hadd", "chegada")),
    dict(nome="Shelbourne Road", estado="fechado", nota="Fechada a partir das 10h.",
         coords=[(53.3292, -6.2322), (53.3325, -6.2320), (53.3352, -6.2335)]),
    dict(nome="Haddington Road", estado="fechado", nota="Fechada a partir das 10h.",
         coords=[(53.3338, -6.2440)] + ll("north_hadd") + [(53.3345, -6.2340)]),
    dict(nome="Anglesea Road", estado="rds_sem_saida",
         nota="Aberta ao tráfego do RDS. Proibida a saída para a Merrion Road: quem entra por aqui sai por Donnybrook.",
         coords=ll("donnybrook") + [(53.3225, -6.2365)] + ll("rds_anglesea", "ballsbridge")),
    dict(nome="Simmonscourt Road", estado="aberto",
         nota="Liga a Merrion Road (na Serpentine Ave) à Anglesea Road. Saída para a Merrion outbound: a confirmar com a Garda.",
         coords=ll("merrion_serp", "rds_simmons") + [(53.3222, -6.2345)]),
    dict(nome="Serpentine Avenue", estado="aberto", nota="Caminho a pé do DART Sandymount até a Merrion Road.",
         coords=ll("merrion_serp", "dart_sandymount")),
    dict(nome="Lansdowne Road", estado="aberto", nota="Caminho a pé do DART Lansdowne Road até Ballsbridge.",
         coords=ll("pembroke_north") + [(53.3298, -6.2320)] + ll("dart_lansdowne")),
    dict(nome="Donnybrook Rd · Morehampton Rd · Leeson St Upper", estado="aberto",
         nota="Abertas. Corredor de carro a partir do centro.",
         coords=ll("donnybrook") + [(53.3235, -6.2420)] + ll("morehampton") + [(53.3300, -6.2500)] + ll("leeson_bridge")),
    dict(nome="Eglinton Road", estado="desvio", nota="Desvio do tráfego outbound da Sandford Road para a Stillorgan Road.",
         coords=ll("sandford_egl", "eglinton_n11", "donnybrook")),
    dict(nome="Sandford Road", estado="aberto", nota="",
         coords=[(53.3260, -6.2520)] + ll("sandford_egl") + [(53.3130, -6.2440)]),
    dict(nome="Rock Road", estado="aberto", nota="Inbound desviado nos Merrion Gates para a Strand Road.",
         coords=ll("merrion_gates") + [(53.3120, -6.2060)] + ll("rock_rd_sul") + [(53.3030, -6.1985)]),
    dict(nome="Strand Road → Sean Moore Road → East Link", estado="desvio",
         nota="Desvio do tráfego inbound da Rock Road. Não leva ao RDS.",
         coords=ll("merrion_gates") + [(53.3220, -6.2095), (53.3300, -6.2075)] + ll("sean_moore", "east_link")),
    dict(nome="Irishtown → Ringsend Road", estado="desvio", nota="Alternativa do desvio para o norte da cidade.",
         coords=ll("sean_moore", "irishtown", "ringsend_rd")),
    dict(nome="Milltown Rd · Clonskeagh Rd · Roebuck Rd · Fosters Ave", estado="percurso",
         nota="Percurso dos corredores antes da N11.",
         coords=ll("milltown") + [(53.3120, -6.2400)] + ll("clonskeagh", "roebuck") + [(53.3060, -6.2240)] + ll("fosters", "n11_fosters")),
    dict(nome="Linha do DART", estado="dart", nota="Funciona normalmente. É a forma mais previsível de chegar.",
         coords=[(53.3345, -6.2330)] + ll("dart_lansdowne", "dart_sandymount", "dart_sydney", "merrion_gates", "dart_booterstown")),
]

# O percurso da maratona como uma linha só (para a camada própria no KML)
PERCURSO = (ll("milltown") + [(53.3120, -6.2400)] + ll("clonskeagh", "roebuck") + [(53.3060, -6.2240)]
            + ll("fosters", "n11_fosters", "ucd_flyover", "n11_nutley") + [(53.3180, -6.2210)]
            + ll("merrion_nutley", "merrion_serp", "rds_merrion", "ballsbridge", "pembroke_north", "north_hadd", "chegada"))

# ─────────────────────────────────────────────────────────────────────────────
# 4. Rotas recomendadas
# ─────────────────────────────────────────────────────────────────────────────
ROTAS = [
    dict(cod="V1", modo="carro", nome="Carro vindo do sul (Blackrock, Dún Laoghaire, Bray, M50)",
         resumo="N11/Stillorgan Road → Donnybrook → Anglesea Road → Anglesea Gate. Nunca pela Rock Road: nos Merrion Gates o inbound é desviado para a Strand Road e não chega ao RDS.",
         coords=ll("n11_mtmerrion", "n11_booterstown", "n11_fosters", "ucd_flyover", "n11_nutley") + [(53.3150, -6.2258), (53.3172, -6.2318)] + ll("donnybrook") + [(53.3225, -6.2365)] + ll("rds_anglesea"),
         gmaps=dict(origem="Stillorgan Road, Mount Merrion, Dublin", destino="RDS Anglesea Road Gate, Anglesea Road, Dublin 4",
                    waypoints=["Donnybrook Church, Stillorgan Road, Dublin 4"], modo="driving")),
    dict(cod="V2", modo="carro", nome="Carro vindo do centro, do oeste e do norte (M1, Port Tunnel, N4, N7)",
         resumo="Leeson Street Upper → Morehampton Road → Donnybrook Road → Anglesea Road → Anglesea Gate. Não tentar Merrion Road, Shelbourne Road nem Northumberland Road.",
         coords=ll("leeson_bridge") + [(53.3300, -6.2500)] + ll("morehampton") + [(53.3235, -6.2420)] + ll("donnybrook") + [(53.3225, -6.2365)] + ll("rds_anglesea"),
         gmaps=dict(origem="Leeson Street Bridge, Dublin 2", destino="RDS Anglesea Road Gate, Anglesea Road, Dublin 4",
                    waypoints=["Donnybrook Church, Stillorgan Road, Dublin 4"], modo="driving")),
    dict(cod="V3", modo="carro", nome="Saída de carro (todos os destinos)",
         resumo="Anglesea Gate → Anglesea Road → Donnybrook, e daí N11 (sul) ou Morehampton/Leeson (centro). É proibido sair da Anglesea para a Merrion Road.",
         coords=ll("rds_anglesea") + [(53.3225, -6.2365)] + ll("donnybrook"),
         gmaps=dict(origem="RDS Anglesea Road Gate, Anglesea Road, Dublin 4", destino="Donnybrook Church, Stillorgan Road, Dublin 4", waypoints=[], modo="driving")),
    dict(cod="V4", modo="carro", nome="Saída alternativa para o sul (a confirmar com a Garda)",
         resumo="Entrada Simmonscourt Road → Merrion Road outbound (permitido a partir da Serpentine Avenue) → Merrion Gates → Rock Road. Só se a Garda confirmar que a boca da Simmonscourt fica liberada.",
         coords=ll("rds_simmons", "merrion_serp", "merrion_nutley") + [(53.3200, -6.2185)] + ll("merrion_gates", "rock_rd_sul"),
         gmaps=dict(origem="RDS Simmonscourt, Simmonscourt Road, Dublin 4", destino="Rock Road, Booterstown", waypoints=["Merrion Gates, Dublin 4"], modo="driving")),
    dict(cod="A1", modo="ape", nome="A pé do DART Sandymount",
         resumo="Serpentine Avenue até a Merrion Road (≈750 m); travessia controlada 1 no cruzamento com a Simmonscourt Road; calçada do lado do RDS para o norte até o portão P1 (≈250 m). Total ≈1,0 km, 13 min.",
         coords=ll("dart_sandymount", "merrion_serp", "rds_merrion"),
         gmaps=dict(origem="Sandymount DART Station", destino="RDS Main Entrance, Merrion Road, Dublin 4", waypoints=["Serpentine Avenue, Dublin 4"], modo="walking")),
    dict(cod="A2", modo="ape", nome="A pé do DART Lansdowne Road",
         resumo="Lansdowne Road e Shelbourne Road (fechada a carros, livre a pé) até Ballsbridge (≈450 m); travessia controlada 2 da Pembroke/Merrion Road; calçada do lado do RDS para o sul até o portão P1 (≈250 m). Total ≈700 m, 9 min.",
         coords=ll("dart_lansdowne") + [(53.3298, -6.2320)] + ll("ballsbridge", "rds_merrion"),
         gmaps=dict(origem="Lansdowne Road DART Station", destino="RDS Main Entrance, Merrion Road, Dublin 4", waypoints=[], modo="walking")),
    dict(cod="A3", modo="ape", nome="A pé de Donnybrook (ônibus 46A, 145, 155, 39A, 11 e desvios do 4/7)",
         resumo="Da parada da igreja de Donnybrook pela Anglesea Road até o Anglesea Gate (≈750 m, 10 min). Não cruza o percurso. Rota interna do Anglesea Gate ao Ring 3: a confirmar com o RDS.",
         coords=ll("bus_donnybrook", "donnybrook") + [(53.3225, -6.2365)] + ll("rds_anglesea"), rotulo_em=2,
         gmaps=dict(origem="Donnybrook Church, Stillorgan Road, Dublin 4", destino="RDS Anglesea Road Gate, Anglesea Road, Dublin 4", waypoints=[], modo="walking")),
    dict(cod="T1", modo="taxi", nome="Táxi, preferencial e pessoas com mobilidade reduzida",
         resumo="Destino a informar ao motorista: «RDS Anglesea Road Gate». Embarque e desembarque dentro do portão. Não pedir «RDS Merrion Road»: o aplicativo pode tentar a Merrion Road fechada.",
         coords=ll("donnybrook") + [(53.3225, -6.2365)] + ll("rds_anglesea", "drop_off"), rotulo_em=3,
         gmaps=dict(origem="", destino="RDS Anglesea Road Gate, Anglesea Road, Dublin 4", waypoints=[], modo="driving")),
]

# ─────────────────────────────────────────────────────────────────────────────
# 5. Janelas horárias (25/10/2026). Votação 8h–17h.
# ─────────────────────────────────────────────────────────────────────────────
JANELAS = [
    dict(ini="07:00", fim="10:00", regime="Normal",
         o_que="Todos os acessos abertos, como no 1º turno. Mesários, seguranças e entregas já dentro. Garda pode começar a conar antes das 10h: premissa a confirmar.",
         corredores="Nenhum no RDS. Largadas em ondas às 8h45, 9h05, 9h25 e 9h45 no centro."),
    dict(ini="10:00", fim="10:45", regime="Maratona · sem corredores ainda",
         o_que="Fechamentos em vigor. Merrion Road vazia mas fechada. Trocar a sinalização de chegada para o regime maratona; abrir o G1 no Anglesea Gate.",
         corredores="Os primeiros (elite) chegam ao RDS por volta das 10h45 — estimativa: km 40 a 3 min/km, largada 8h45."),
    dict(ini="10:45", fim="14:30", regime="Maratona · pico",
         o_que="Fluxo contínuo de corredores na Merrion Road. Travessias a pé só nos pontos controlados, com espera. Todo veículo pela Anglesea Road.",
         corredores="Grosso do pelotão: ondas de 3h a 5h passam pelo km 40 entre 11h30 e 14h30 (estimativa)."),
    dict(ini="14:30", fim="16:00", regime="Maratona · cauda",
         o_que="Fluxo esparso; travessias mais fáceis. Fechamentos seguem até a Garda reabrir. Não presumir reabertura.",
         corredores="Últimos corredores (≈6h da onda 4) por volta das 15h40 (estimativa). Reabertura provável entre 15h30 e 16h30: a confirmar."),
    dict(ini="16:00", fim="17:00", regime="Reabertura progressiva (a confirmar)",
         o_que="Tratar como regime maratona até confirmação da Garda no rádio. Última hora de votação: pico de chegada tardia — comunicar que quem está na fila às 17h vota.",
         corredores="Varredura e recolha de cones."),
    dict(ini="17:00", fim="18:30", regime="Normal",
         o_que="Saída dos últimos eleitores, mesários e material. Merrion Road normal (premissa).",
         corredores="—"),
]

# ─────────────────────────────────────────────────────────────────────────────
# 6. Conferência: rotas de veículo não tocam trecho fechado / contramão
# ─────────────────────────────────────────────────────────────────────────────
def _nos(coords):
    return {(round(a, 5), round(b, 5)) for a, b in coords}

def confere():
    erros = []
    fechados = {}
    for t in TRECHOS:
        if t["estado"] in ("fechado", "percurso"):
            # nós internos do trecho (os extremos são cruzamentos compartilhados)
            for n in _nos(t["coords"][1:-1]):
                fechados[n] = t["nome"]
    for r in ROTAS:
        if r["modo"] not in ("carro", "taxi"):
            continue
        for n in _nos(r["coords"]):
            if n in fechados:
                erros.append(f"{r['cod']} toca trecho fechado: {fechados[n]}")
        # a rota V4 corre pela Merrion outbound: sentido tem de ser sul (lat decrescente)
        if r["cod"] == "V4":
            lats = [c[0] for c in r["coords"][1:5]]
            if any(b > a for a, b in zip(lats, lats[1:])):
                erros.append("V4 corre no sentido inbound na Merrion Road (só outbound é permitido)")
    # a Anglesea não pode ser saída para a Merrion: nenhuma rota de saída passa por Ballsbridge
    for r in ROTAS:
        if r["cod"].startswith("V") and r["modo"] == "carro" and "Saída" in r["nome"]:
            if _nos(ll("ballsbridge")) & _nos(r["coords"]):
                erros.append(f"{r['cod']} sai da Anglesea para a Merrion Road em Ballsbridge (proibido)")
    return erros

# ─────────────────────────────────────────────────────────────────────────────
# 7. Google Maps: links
# ─────────────────────────────────────────────────────────────────────────────
def link_dir(g):
    base = "https://www.google.com/maps/dir/?api=1"
    q = f"&destination={quote_plus(g['destino'])}&travelmode={g['modo']}"
    if g.get("origem"):
        q = f"&origin={quote_plus(g['origem'])}" + q
    if g.get("waypoints"):
        q += "&waypoints=" + quote_plus("|".join(g["waypoints"]))
    return base + q

def link_pin(chave):
    p = P[chave]
    return f"https://www.google.com/maps/search/?api=1&query={p['lat']:.5f}%2C{p['lon']:.5f}"

# ─────────────────────────────────────────────────────────────────────────────
# 8. KML para o Google My Maps
# ─────────────────────────────────────────────────────────────────────────────
CORES_KML = {  # aabbggrr
    "percurso": "ff1f7fe0", "fechado": "ff2c3aab", "so_outbound": "ff0f5d9c",
    "rds_sem_saida": "ff66701e", "desvio": "ff8a4a8a", "aberto": "ff8a8a8a", "dart": "ff2e7d32",
    "carro": "ff17786a", "ape": "ffb06b1a", "taxi": "ff7a3fbf",
}
LARG_KML = {"percurso": 7, "fechado": 5, "so_outbound": 5, "rds_sem_saida": 5, "desvio": 4, "aberto": 2, "dart": 4,
            "carro": 6, "ape": 5, "taxi": 5}

def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def _linha(nome, desc, coords, estilo):
    cs = " ".join(f"{lon:.5f},{lat:.5f},0" for lat, lon in coords)
    return (f"<Placemark><name>{_esc(nome)}</name><description>{_esc(desc)}</description>"
            f"<styleUrl>#{estilo}</styleUrl><LineString><tessellate>1</tessellate>"
            f"<coordinates>{cs}</coordinates></LineString></Placemark>")

def _ponto(nome, desc, lat, lon, estilo):
    return (f"<Placemark><name>{_esc(nome)}</name><description>{_esc(desc)}</description>"
            f"<styleUrl>#{estilo}</styleUrl><Point><coordinates>{lon:.5f},{lat:.5f},0</coordinates></Point></Placemark>")

def kml():
    estilos = []
    for k, cor in CORES_KML.items():
        estilos.append(f'<Style id="{k}"><LineStyle><color>{cor}</color><width>{LARG_KML[k]}</width></LineStyle></Style>')
    for k, cor in {"portao": "ff17786a", "dart": "ff2e7d32", "bus": "ff2e7d32", "travessia": "ff1f7fe0",
                   "posto": "ff7a3fbf", "cruz": "ff8a8a8a", "local": "ff57616d"}.items():
        estilos.append(f'<Style id="pt_{k}"><IconStyle><color>{cor}</color><scale>1.1</scale>'
                       f'<Icon><href>https://maps.google.com/mapfiles/kml/paddle/wht-blank.png</href></Icon></IconStyle></Style>')
    pastas = []
    pastas.append("<Folder><name>1 · Percurso da maratona</name>"
                  + _linha("Percurso dos corredores (trecho Dublin 4)", FONTE_POLICIA["percurso"], PERCURSO, "percurso")
                  + "</Folder>")
    pastas.append("<Folder><name>2 · Vias: fechadas, sentido único, desvios</name>"
                  + "".join(_linha(t["nome"] + f" [{t['estado']}]", t["nota"], t["coords"], t["estado"])
                            for t in TRECHOS if t["estado"] != "aberto")
                  + "</Folder>")
    pastas.append("<Folder><name>3 · Rotas de acesso recomendadas</name>"
                  + "".join(_linha(f"{r['cod']} · {r['nome']}", r["resumo"] + "\n\nGoogle Maps: " + link_dir(r["gmaps"]),
                                   r["coords"], r["modo"]) for r in ROTAS)
                  + "</Folder>")
    pastas.append("<Folder><name>4 · Pontos: portões, DART, travessias, postos</name>"
                  + "".join(_ponto(p["nome"], f"{k} · {p['lat']:.5f}, {p['lon']:.5f}", p["lat"], p["lon"], "pt_" + p["tipo"])
                            for k, p in P.items() if p["tipo"] in ("portao", "dart", "bus", "travessia", "posto", "local"))
                  + "</Folder>")
    doc = ('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document>'
           "<name>Acesso ao RDS · 2º turno 25/10/2026 · dia da Maratona de Dublin</name>"
           "<description>Gerado por scripts/acesso_2turno.py. Coordenadas aproximadas (30–60 m): arraste no My Maps se preciso.</description>"
           + "".join(estilos) + "".join(pastas) + "</Document></kml>")
    return doc

# ─────────────────────────────────────────────────────────────────────────────
# 9. SVG esquemático
# ─────────────────────────────────────────────────────────────────────────────
LAT0, LAT1 = 53.2975, 53.3405
LON0, LON1 = -6.2570, -6.1960
W = 980
K = math.cos(math.radians((LAT0 + LAT1) / 2))
ESC = W / ((LON1 - LON0) * K)
H = int((LAT1 - LAT0) * ESC)
MARGEM = 20

def xy(lat, lon):
    return ((lon - LON0) * K * ESC + MARGEM, (LAT1 - lat) * ESC + MARGEM)

def _path(coords):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in (xy(a, b) for a, b in coords))

ESTILO_SVG = {
    "aberto":        'stroke="var(--via)" stroke-width="5"',
    "dart":          'stroke="var(--dart)" stroke-width="3" stroke-dasharray="10 6"',
    "desvio":        'stroke="var(--desvio)" stroke-width="5" stroke-dasharray="14 7"',
    "so_outbound":   'stroke="var(--outbound)" stroke-width="7"',
    "rds_sem_saida": 'stroke="var(--rds)" stroke-width="7"',
    "fechado":       'stroke="var(--fechado)" stroke-width="7"',
    "percurso":      'stroke="var(--fechado)" stroke-width="7"',
}
ESTILO_ROTA = {
    "carro": 'stroke="var(--carro)" stroke-width="4.5"',
    "ape":   'stroke="var(--ape)" stroke-width="4" stroke-dasharray="7 5"',
    "taxi":  'stroke="var(--taxi)" stroke-width="3" stroke-dasharray="3 4"',
}

def svg(embutido=False):
    partes = []
    tw, th = W + 2 * MARGEM, H + 2 * MARGEM
    partes.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {tw} {th}" '
                  f'class="planta" role="img" aria-label="Mapa esquemático do acesso ao RDS no dia da maratona">')
    if not embutido:
        partes.append('<style>:root{--papel:#efece4;--via:#d7d1c3;--dart:#2e7d32;--desvio:#8a4a8a;--outbound:#9c5d0f;'
                      '--rds:#1e7066;--fechado:#ab3a2c;--carro:#146f66;--ape:#1a6bb0;--taxi:#7a3fbf;--tinta:#161f29;'
                      '--meio:#57616d;--folha:#fbf9f4}'
                      'text{font-family:"IBM Plex Sans",Helvetica,Arial,sans-serif}</style>')
    partes.append(f'<rect width="{tw}" height="{th}" fill="var(--papel)"/>')
    # água (baía) — só um lembrete de orientação
    baia = [(53.3405, -6.2085), (53.3355, -6.2085), (53.3300, -6.2058), (53.3220, -6.2078), (53.3165, -6.2108),
            (53.3105, -6.1975), (53.2975, -6.1930), (53.2975, -6.1960), (53.3405, -6.1960)]
    partes.append(f'<path d="{_path(baia)} Z" fill="var(--via)" opacity=".35"/>')
    partes.append(f'<text x="{xy(53.3300,-6.1985)[0]:.0f}" y="{xy(53.3300,-6.1985)[1]:.0f}" font-size="12" fill="var(--meio)" font-style="italic">Baía de Dublin</text>')
    # percurso (halo) + trechos
    partes.append(f'<path d="{_path(PERCURSO)}" fill="none" stroke="var(--fechado)" stroke-width="16" opacity=".16" stroke-linejoin="round" stroke-linecap="round"/>')
    for t in TRECHOS:
        partes.append(f'<path d="{_path(t["coords"])}" fill="none" {ESTILO_SVG[t["estado"]]} stroke-linejoin="round" stroke-linecap="round"><title>{_esc(t["nome"])}: {_esc(t["nota"])}</title></path>')
    # setas do sentido dos corredores
    for a, b in zip(PERCURSO, PERCURSO[1:]):
        (x1, y1), (x2, y2) = xy(*a), xy(*b)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        partes.append(f'<path d="M -6 -5 L 4 0 L -6 5 Z" fill="var(--fechado)" transform="translate({mx:.1f} {my:.1f}) rotate({ang:.0f})"/>')
    # rotas recomendadas
    for r in ROTAS:
        partes.append(f'<path d="{_path(r["coords"])}" fill="none" {ESTILO_ROTA[r["modo"]]} stroke-linejoin="round" stroke-linecap="round" opacity=".95"><title>{r["cod"]} · {_esc(r["nome"])}</title></path>')
        # rótulo no meio da rota
        c = r["coords"][r.get("rotulo_em", len(r["coords"]) // 2)]
        x, y = xy(*c)
        cor = {"carro": "var(--carro)", "ape": "var(--ape)", "taxi": "var(--taxi)"}[r["modo"]]
        partes.append(f'<rect x="{x-14:.0f}" y="{y-22:.0f}" width="28" height="16" rx="3" fill="var(--folha)" stroke="{cor}"/>'
                      f'<text x="{x:.0f}" y="{y-10:.0f}" text-anchor="middle" font-size="10.5" font-weight="700" fill="{cor}">{r["cod"]}</text>')
    # RDS
    for k in ("hall2", "ring3"):
        x, y = xy(P[k]["lat"], P[k]["lon"])
        partes.append(f'<rect x="{x-16:.0f}" y="{y-9:.0f}" width="32" height="18" rx="2" fill="var(--folha)" stroke="var(--meio)"/>'
                      f'<text x="{x:.0f}" y="{y+4:.0f}" text-anchor="middle" font-size="9.5" fill="var(--tinta)">{"Hall 2" if k=="hall2" else "Ring 3"}</text>')
    # pontos
    rot = {
        "rds_merrion": ("P1 · portão Merrion Rd (a pé)", 12, -8), "rds_anglesea": ("Anglesea Gate (veículos, táxi)", -12, -8),
        "rds_simmons": ("Simmonscourt (saída V4, a confirmar)", -10, 4), "dart_sandymount": ("DART Sandymount", 8, 14),
        "dart_lansdowne": ("DART Lansdowne Rd", 8, -8), "dart_sydney": ("DART Sydney Parade", 8, 4),
        "dart_booterstown": ("DART Booterstown", -8, -8), "bus_donnybrook": ("Ônibus · Donnybrook", 10, 4),
        "trav_serp": ("travessia 1", 10, 14), "trav_balls": ("travessia 2 · Ballsbridge", 10, -10),
        "merrion_gates": ("Merrion Gates · desvio", 10, 14), "merrion_nutley": ("Nutley Lane", 10, -4),
        "ucd_flyover": ("viaduto UCD", 10, 12), "chegada": ("chegada da maratona", 12, 14),
        "leeson_bridge": ("Leeson St Bridge", 10, 4), "milltown": ("Milltown Bridge", -6, 16),
        "eglinton_n11": ("Eglinton Rd", -8, 16), "n11_fosters": ("Fosters Ave", 10, 12),
    }
    for k, (txt, dx, dy) in rot.items():
        p = P[k]; x, y = xy(p["lat"], p["lon"])
        cor = {"portao": "var(--carro)", "dart": "var(--dart)", "bus": "var(--dart)", "travessia": "var(--ape)"}.get(p["tipo"], "var(--meio)")
        rr = 6 if p["tipo"] in ("portao", "travessia") else 4.5
        partes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr}" fill="var(--folha)" stroke="{cor}" stroke-width="2.5"/>')
        anc = "end" if dx < 0 else "start"
        partes.append(f'<text x="{x+dx:.0f}" y="{y+dy:.0f}" text-anchor="{anc}" font-size="11" font-weight="600" fill="var(--tinta)" stroke="var(--papel)" stroke-width="3" paint-order="stroke">{_esc(txt)}</text>')
    # rótulos de vias
    vias = [("STILLORGAN ROAD · N11 · aberta", 53.3115, -6.2290, -38), ("MERRION ROAD · só outbound", 53.3195, -6.2150, -45),
            ("ANGLESEA ROAD · tráfego do RDS", 53.3232, -6.2405, -35), ("ROCK ROAD", 53.3115, -6.2010, -45),
            ("STRAND ROAD · desvio", 53.3250, -6.2060, -85), ("SANDFORD RD", 53.3200, -6.2500, -60),
            ("MOREHAMPTON RD", 53.3275, -6.2500, -40), ("NORTHUMBERLAND RD", 53.3340, -6.2395, -55),
            ("SERPENTINE AVE", 53.3262, -6.2215, 0)]
    for txt, lat, lon, ang in vias:
        x, y = xy(lat, lon)
        partes.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="9.5" letter-spacing="1.2" fill="var(--meio)" transform="rotate({ang} {x:.0f} {y:.0f})" stroke="var(--papel)" stroke-width="3" paint-order="stroke">{txt}</text>')
    # escala (500 m)
    m500 = 500 / 111_320 * ESC
    x0, y0 = MARGEM + 30, th - 30
    partes.append(f'<line x1="{x0}" y1="{y0}" x2="{x0+m500:.0f}" y2="{y0}" stroke="var(--tinta)" stroke-width="2"/>'
                  f'<text x="{x0}" y="{y0-6}" font-size="10" fill="var(--meio)">500 m · esquema, coordenadas aproximadas · N ↑</text>')
    partes.append("</svg>")
    return "".join(partes)


# ─────────────────────────────────────────────────────────────────────────────
# 9b. Página HTML (mapa/acesso_2turno.html) — mesma fonte, mesmo estilo dos
#     outros artefatos de mapa/
# ─────────────────────────────────────────────────────────────────────────────
CSS = """
:root{
  --papel:#efece4; --folha:#fbf9f4; --tinta:#161f29; --meio:#57616d; --fraco:#8b919a;
  --regua:#d7d1c3; --regua2:#e7e2d6; --via:#d7d1c3;
  --dart:#2e7d32; --desvio:#8a4a8a; --outbound:#9c5d0f; --rds:#1e7066; --fechado:#ab3a2c;
  --carro:#146f66; --ape:#1a6bb0; --taxi:#7a3fbf; --alerta:#ab3a2c; --ok:#17786a;
  --realce:rgba(26,107,176,.09);
}
@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]){
  --papel:#0e1216; --folha:#161b21; --tinta:#e4e8ed; --meio:#9ea6b0; --fraco:#727b85;
  --regua:#293038; --regua2:#1e242b; --via:#3a434d;
  --dart:#6cc07a; --desvio:#c98ccb; --outbound:#d9a054; --rds:#4ec0a8; --fechado:#e0796a;
  --carro:#4ec0a8; --ape:#6aa9e2; --taxi:#b48ae6; --alerta:#e0796a; --ok:#4ec0a8;
  --realce:rgba(106,169,226,.13);
}}
:root[data-theme="dark"]{
  --papel:#0e1216; --folha:#161b21; --tinta:#e4e8ed; --meio:#9ea6b0; --fraco:#727b85;
  --regua:#293038; --regua2:#1e242b; --via:#3a434d;
  --dart:#6cc07a; --desvio:#c98ccb; --outbound:#d9a054; --rds:#4ec0a8; --fechado:#e0796a;
  --carro:#4ec0a8; --ape:#6aa9e2; --taxi:#b48ae6; --alerta:#e0796a; --ok:#4ec0a8;
  --realce:rgba(106,169,226,.13);
}
*{box-sizing:border-box}
body{margin:0; background:var(--papel); color:var(--tinta);
  font-family:"IBM Plex Sans",ui-sans-serif,system-ui,Helvetica,Arial,sans-serif;
  font-size:16.5px; line-height:1.62; -webkit-font-smoothing:antialiased}
.folha{max-width:1060px; margin:0 auto; padding:0 16px 96px}
.prosa{max-width:66ch}
h1,h2,h3{font-family:Archivo,ui-sans-serif,system-ui,Helvetica,Arial,sans-serif; margin:0;
  letter-spacing:-.018em; text-wrap:balance}
h1{font-size:clamp(2rem,5.2vw,3.2rem); line-height:1.03; font-weight:700}
h2{font-size:clamp(1.35rem,2.5vw,1.8rem); line-height:1.16; font-weight:700}
h3{font-size:1rem; font-weight:600}
p{margin:0 0 1.05em} strong{font-weight:600}
.mono{font-family:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace; font-variant-numeric:tabular-nums}
a{color:var(--ape)}
.olho{font-family:"IBM Plex Mono",monospace; font-size:.7rem; letter-spacing:.17em; text-transform:uppercase; color:var(--meio); margin:0 0 16px}
header{padding-top:56px}
.chamada{font-size:clamp(1.02rem,1.9vw,1.18rem); line-height:1.55; color:var(--meio); max-width:60ch; margin:20px 0 0}
.chamada b{color:var(--tinta); font-weight:600}
.carimbo{display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:1px; background:var(--regua); border:1px solid var(--regua); margin:38px 0 0}
.carimbo>div{background:var(--papel); padding:13px 14px}
.carimbo dt{font-size:.68rem; letter-spacing:.1em; text-transform:uppercase; color:var(--meio); margin:0 0 5px}
.carimbo dd{margin:0; font-family:"IBM Plex Mono",monospace; font-size:1.3rem; font-weight:500; line-height:1.14}
.carimbo dd small{display:block; font-family:"IBM Plex Sans",sans-serif; font-size:.72rem; font-weight:400; color:var(--fraco); margin-top:4px}
section{margin:64px 0 0}
.rotulo{font-family:"IBM Plex Mono",monospace; font-size:.7rem; letter-spacing:.17em; text-transform:uppercase; color:var(--meio); margin:0 0 10px; padding-bottom:9px; border-bottom:1px solid var(--regua)}
section>h2{margin-bottom:16px}
figure{margin:26px 0 0}
.prancha{background:var(--folha); border:1px solid var(--regua); padding:10px; overflow-x:auto}
svg.planta{display:block; width:100%; height:auto; min-width:560px}
figcaption{font-size:.85rem; color:var(--meio); margin-top:12px; max-width:70ch}
.legenda{display:grid; gap:8px 22px; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); margin:14px 0 0; font-size:.88rem}
.legenda span{display:flex; align-items:center; gap:10px}
.legenda i{display:inline-block; width:34px; height:0; border-top:5px solid var(--c); flex:none}
.legenda i.tr{border-top-style:dashed}
table{border-collapse:collapse; width:100%; margin:18px 0 0; font-size:.92rem}
th,td{text-align:left; vertical-align:top; padding:9px 10px; border-bottom:1px solid var(--regua2)}
th{font-family:"IBM Plex Mono",monospace; font-size:.68rem; letter-spacing:.12em; text-transform:uppercase; color:var(--meio); font-weight:500}
td.cod{font-family:"IBM Plex Mono",monospace; font-weight:600; white-space:nowrap}
td.cod.carro{color:var(--carro)} td.cod.ape{color:var(--ape)} td.cod.taxi{color:var(--taxi)}
td.hora{font-family:"IBM Plex Mono",monospace; white-space:nowrap}
.aviso{border-left:4px solid var(--alerta); background:var(--realce); padding:12px 16px; margin:18px 0 0; max-width:70ch}
.ok{border-left-color:var(--ok)}
ol.lista{padding-left:1.2em; max-width:70ch} ol.lista li{margin:0 0 .6em}
.pill{display:inline-block; font-family:"IBM Plex Mono",monospace; font-size:.7rem; letter-spacing:.08em; padding:1px 7px; border:1px solid var(--regua); border-radius:3px; color:var(--meio); margin-left:6px; vertical-align:middle}
footer{margin-top:80px; color:var(--fraco); font-size:.82rem; max-width:70ch}
@media (max-width:640px){ .folha{padding:0 16px 64px} table{font-size:.85rem} th,td{padding:7px 6px} }
"""

def html():
    def linhas_rotas():
        out = []
        for r in ROTAS:
            out.append(f'<tr><td class="cod {r["modo"]}">{r["cod"]}</td><td><b>{_esc(r["nome"])}</b><br>{_esc(r["resumo"])}</td>'
                       f'<td><a href="{link_dir(r["gmaps"])}" target="_blank" rel="noopener">Google&nbsp;Maps</a></td></tr>')
        return "".join(out)
    def linhas_janelas():
        return "".join(f'<tr><td class="hora">{j["ini"]}–{j["fim"]}</td><td><b>{_esc(j["regime"])}</b></td>'
                       f'<td>{_esc(j["o_que"])}</td><td>{_esc(j["corredores"])}</td></tr>' for j in JANELAS)
    def linhas_vias():
        nomes = {"fechado": "fechada", "percurso": "percurso", "so_outbound": "só outbound", "rds_sem_saida": "aberta ao RDS, sem saída p/ Merrion", "desvio": "desvio", "aberto": "aberta", "dart": "DART"}
        return "".join(f'<tr><td><b>{_esc(t["nome"])}</b></td><td class="mono">{nomes[t["estado"]]}</td><td>{_esc(t["nota"])}</td></tr>'
                       for t in TRECHOS if t["estado"] not in ("aberto", "dart") or t["nota"])
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Acesso no 2º Turno</title>
<meta name="description" content="Plano de acesso ao RDS em 25/10/2026, dia da Maratona de Dublin: como eleitores, mesários e veículos chegam e saem com a Merrion Road fechada.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<div class="folha">
<header>
  <p class="olho">Eleições 2026 · Posto de Dublin · 2º turno · 25/10/2026</p>
  <h1>Acesso ao RDS no dia da Maratona</h1>
  <p class="chamada">Se houver 2º turno, ele cai no domingo da <b>Maratona de Dublin</b>, e a <b>Merrion Road</b> — a porta do RDS no 1º turno — é o percurso dos corredores, <b>fechada a partir das 10h</b>. O plano troca a entrada de veículos para o <b>Anglesea Gate</b>, mantém a entrada a pé pelo portão da Merrion Road e pede à Garda <b>duas travessias controladas</b>. Base: o plano de trânsito enviado pela chefia de polícia da região (setembro de 2026).</p>
  <dl class="carimbo">
    <div><dt>Votação</dt><dd>8h–17h<small>25/10/2026, domingo</small></dd></div>
    <div><dt>Fechamentos</dt><dd>a partir das 10h<small>Merrion Rd inbound, Nutley Lane, Shelbourne, Haddington, Northumberland</small></dd></div>
    <div><dt>Veículos</dt><dd>Anglesea Gate<small>única entrada; saída por Donnybrook</small></dd></div>
    <div><dt>A pé</dt><dd>portão Merrion Rd<small>P1 do 1º turno, pela calçada do lado do RDS</small></dd></div>
    <div><dt>Corredores no RDS</dt><dd>≈10h45–15h40<small>estimativa, km 40 do percurso</small></dd></div>
    <div><dt>Regime maratona</dt><dd>≈6 h de 9<small>cobre ~2/3 do dia de votação</small></dd></div>
  </dl>
</header>

<section>
  <p class="rotulo">01 · O mapa</p>
  <h2>O percurso, os fechamentos e as rotas recomendadas</h2>
  <p class="prosa">O RDS fica entre a Merrion Road (leste) e a Anglesea Road (oeste). Os corredores descem a Nutley Lane, entram na Merrion Road e seguem por Ballsbridge até a chegada — ou seja, passam <b>exatamente pela fachada do RDS</b>. Tudo o que vem do leste (DART, Sandymount) tem de cruzar o percurso; tudo o que vem do oeste (Donnybrook, N11, centro) chega sem cruzar.</p>
  <figure>
    <div class="prancha">{svg(embutido=True)}</div>
    <div class="legenda">
      <span style="--c:var(--fechado)"><i></i>percurso da maratona / via fechada (10h→)</span>
      <span style="--c:var(--outbound)"><i></i>Merrion Road: só outbound, da Serpentine Ave</span>
      <span style="--c:var(--rds)"><i></i>Anglesea Road: tráfego do RDS, sem saída p/ Merrion</span>
      <span style="--c:var(--desvio)"><i class="tr"></i>desvios da Garda (não levam ao RDS)</span>
      <span style="--c:var(--carro)"><i></i>V1–V4 · rotas de carro</span>
      <span style="--c:var(--ape)"><i class="tr"></i>A1–A3 · rotas a pé</span>
      <span style="--c:var(--taxi)"><i class="tr"></i>T1 · táxi e preferencial</span>
      <span style="--c:var(--dart)"><i class="tr"></i>linha do DART</span>
    </div>
    <figcaption>Esquema em projeção simples, com coordenadas de referência (precisão de 30–60 m). Para o mapa real, importe <span class="mono">mapa/acesso_2turno.kml</span> no Google My Maps ou use os links de cada rota abaixo. Gerado por <span class="mono">scripts/acesso_2turno.py</span>.</figcaption>
  </figure>
</section>

<section>
  <p class="rotulo">02 · O que a Garda decidiu</p>
  <h2>Vias, estado e consequência para o RDS</h2>
  <table>
    <thead><tr><th>Via</th><th>Estado</th><th>Consequência</th></tr></thead>
    <tbody>{linhas_vias()}</tbody>
  </table>
  <div class="aviso"><b>A frase que manda no plano:</b> «Anglesea Road will remain open to R.D.S. traffic but traffic will not be allowed exit Anglesea onto Merrion Road.» A Anglesea é a única via que a Garda reservou ao RDS. Entra-se e sai-se por ela, sempre por Donnybrook.</div>
</section>

<section>
  <p class="rotulo">03 · As rotas</p>
  <h2>Como chegar e como sair, por modo</h2>
  <table>
    <thead><tr><th>Cód.</th><th>Rota</th><th>Abrir</th></tr></thead>
    <tbody>{linhas_rotas()}</tbody>
  </table>
  <div class="aviso"><b>O Google Maps não sabe da maratona com antecedência.</b> No dia, o Waze e o Google costumam receber os fechamentos da Garda, mas o eleitor que planeja de véspera verá a Merrion Road aberta. Por isso a comunicação diz o destino pelo nome do portão — «RDS Anglesea Road Gate» — e nunca «RDS».</div>
</section>

<section>
  <p class="rotulo">04 · O dia, hora a hora</p>
  <h2>Três regimes: normal, maratona, reabertura</h2>
  <table>
    <thead><tr><th>Janela</th><th>Regime</th><th>O que vale</th><th>Corredores</th></tr></thead>
    <tbody>{linhas_janelas()}</tbody>
  </table>
  <p class="prosa" style="margin-top:14px">As horas dos corredores são <b>estimativas</b> a partir das ondas de largada (8h45, 9h05, 9h25, 9h45) e do RDS estar perto do km 40. A Garda não informou hora de reabertura: o plano trata o regime maratona como vigente até confirmação no dia.</p>
</section>

<section>
  <p class="rotulo">05 · O que muda em relação ao 1º turno</p>
  <h2>Sete diferenças operacionais</h2>
  <ol class="lista">
    <li><b>Veículos só pelo Anglesea Gate.</b> Mesários que chegam depois das 10h, táxis, ambulância, entregas, saída de material. Saída sempre por Donnybrook. O portão da Merrion Road fica só para pedestres.</li>
    <li><b>Posto novo G1 no Anglesea Gate</b> (2 pessoas): recebe quem chega de carro, táxi e ônibus de Donnybrook, aponta o caminho interno até o Ring 3 e cobre o preferencial. Em C1 (9 pessoas) sai de um dos 3 operadores do P0 mais o T1 em rodízio; de C2 em diante, +2 na fila de preenchimento. <b>Não editado em <span class="mono">lista_postos.md</span></b>: é proposta a decidir pelo Posto.</li>
    <li><b>Rota interna Anglesea Gate → Ring 3.</b> A entrada do Ring 3 é pelo canto nordeste; quem entra pelo oeste precisa de um caminho sinalizado dentro do RDS. A confirmar com o RDS na vistoria.</li>
    <li><b>Fila da calçada capada.</b> No 1º turno a fila pode se formar na calçada da Merrion Road; no 2º a calçada é zona de espectadores e a Garda não vai aceitar fila na via. O Ring 3 tem lotação 2.118: a instrução é <b>puxar a fila para dentro</b> e manter o P0 encostado no gradil.</li>
    <li><b>Duas travessias controladas</b> a pedir à Garda: Merrion Rd × Serpentine Ave (quem vem do DART Sandymount) e Ballsbridge (quem vem do DART Lansdowne Road). Sem elas, ~2/3 dos eleitores a pé ficam do lado errado do percurso durante 5 horas.</li>
    <li><b>Comunicação muda de tom:</b> «venha de DART» (Sandymount ou Lansdowne Road) e «de carro, só Anglesea Road Gate». E «descubra sua seção antes de sair de casa» vale ainda mais: o P0 terá menos espaço.</li>
    <li><b>Tudo o que é entrega chega antes das 10h</b> — comida, material, reposição — ou vem pela Anglesea com margem: a N11 e Donnybrook estarão lentas.</li>
  </ol>
</section>

<section>
  <p class="rotulo">06 · Pedidos a terceiros</p>
  <h2>O que ainda depende da Garda e do RDS</h2>
  <ol class="lista">
    <li><b>Garda:</b> travessias controladas 1 e 2 (com horário); hora prevista de reabertura da Merrion Road; se a boca da Simmonscourt Road pode sair para a Merrion outbound (rota V4); ponto de contato no dia (rádio/telefone).</li>
    <li><b>RDS:</b> Anglesea Gate aberto e operado das 7h às 18h30; rota interna sinalizável até o Ring 3; estacionamento Anglesea/Simmonscourt para mesários; se o RDS recebe alguma operação da maratona no mesmo dia.</li>
    <li><b>Dublin Bus / TFI:</b> desvios das linhas 4, 7, 7A e 18 (Merrion Road) e paradas alternativas em Donnybrook — o plano assume Donnybrook como ponto de ônibus.</li>
  </ol>
  <div class="aviso ok"><b>O que não muda:</b> o Ring 3, as três zonas, as portas S4–S7, o P0 no gradil da Merrion Road e toda a rota P0–P7. O plano muda como se chega ao P0, não o que acontece depois dele.</div>
</section>

<footer>Gerado por <span class="mono">scripts/acesso_2turno.py</span> a partir do plano de trânsito da Garda. Coordenadas aproximadas; horários dos corredores são estimativa. Fonte da data e das ondas: Irish Life Dublin Marathon 2026, 25/10, largadas 8h45–9h45.</footer>
</div>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────────────────
# 10. Saídas
# ─────────────────────────────────────────────────────────────────────────────
def links_md():
    L = ["# Links do Google Maps · acesso ao RDS no 2º turno", "",
         "Gerados por `scripts/acesso_2turno.py`. Abrem no Google Maps com origem, destino e pontos de passagem já preenchidos.",
         "O Google Maps **não conhece os fechamentos da maratona com antecedência**: confira que a rota exibida segue o desenho aqui descrito.", ""]
    L.append("## Rotas")
    L.append("")
    L.append("| Cód. | Rota | Link |")
    L.append("|---|---|---|")
    for r in ROTAS:
        L.append(f"| {r['cod']} | {r['nome']} | [abrir]({link_dir(r['gmaps'])}) |")
    L += ["", "## Pontos", "", "| Ponto | Coordenadas (aprox.) | Link |", "|---|---|---|"]
    for k, p in P.items():
        if p["tipo"] in ("portao", "dart", "bus", "travessia", "posto"):
            L.append(f"| {p['nome']} | {p['lat']:.5f}, {p['lon']:.5f} | [abrir]({link_pin(k)}) |")
    L += ["", "## Google My Maps", "",
          "1. Abrir <https://www.google.com/maps/d/> e criar um mapa.",
          "2. *Importar* → escolher `mapa/acesso_2turno.kml`. Cada pasta do KML vira uma camada: percurso, vias, rotas, pontos.",
          "3. Arrastar os pontos que estiverem fora do lugar (as coordenadas são aproximadas, 30–60 m).",
          "4. *Compartilhar* → link público, para a comunicação com os eleitores."]
    return "\n".join(L) + "\n"

def relatorio(erros):
    print("Plano de acesso · 2º turno 25/10/2026 · Maratona de Dublin")
    print(f"  pontos: {len(P)} · trechos: {len(TRECHOS)} · rotas: {len(ROTAS)} · janelas: {len(JANELAS)}")
    print("  trechos fechados/percurso:", ", ".join(t["nome"] for t in TRECHOS if t["estado"] in ("fechado", "percurso")))
    print("  só outbound:", ", ".join(t["nome"] for t in TRECHOS if t["estado"] == "so_outbound"))
    print("  aberto ao RDS sem saída para a Merrion:", ", ".join(t["nome"] for t in TRECHOS if t["estado"] == "rds_sem_saida"))
    if erros:
        print("\nCONFERÊNCIA FALHOU:")
        for e in erros:
            print("  -", e)
    else:
        print("\nConferência OK: nenhuma rota de veículo toca trecho fechado; V3 não sai por Ballsbridge; V4 corre outbound.")

def main():
    erros = confere()
    relatorio(erros)
    if erros:
        sys.exit(1)
    if not GRAVA:
        print("\n(sem --grava: nada foi escrito)")
        return
    (RAIZ / "mapa").mkdir(exist_ok=True)
    (RAIZ / "saidas").mkdir(exist_ok=True)
    (RAIZ / "mapa" / "acesso_2turno.kml").write_text(kml(), encoding="utf-8")
    (RAIZ / "saidas" / "acesso_2turno.svg").write_text(svg(), encoding="utf-8")
    (RAIZ / "saidas" / "acesso_2turno_links.md").write_text(links_md(), encoding="utf-8")
    (RAIZ / "mapa" / "acesso_2turno.html").write_text(html(), encoding="utf-8")
    dados = dict(
        gerado_por="scripts/acesso_2turno.py", data_evento="2026-10-25", votacao="08:00-17:00",
        fonte_policia=FONTE_POLICIA,
        pontos={k: dict(v, gmaps=link_pin(k)) for k, v in P.items()},
        trechos=[dict(t, coords=[list(c) for c in t["coords"]]) for t in TRECHOS],
        percurso=[list(c) for c in PERCURSO],
        rotas=[dict(r, coords=[list(c) for c in r["coords"]], gmaps_url=link_dir(r["gmaps"])) for r in ROTAS],
        janelas=JANELAS,
    )
    (RAIZ / "saidas" / "acesso_2turno.json").write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nGravados: mapa/acesso_2turno.kml · mapa/acesso_2turno.html · saidas/acesso_2turno.svg · saidas/acesso_2turno.json · saidas/acesso_2turno_links.md")

if __name__ == "__main__":
    main()
