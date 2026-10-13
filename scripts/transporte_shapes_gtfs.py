"""Extrai do GTFS da NTA os tracados das linhas de onibus dentro da caixa do mapa.
uso: python3 -I scripts/transporte_shapes_gtfs.py <gtfs_dir> "conflito com maratona/dados/shapes_linhas.json"
Para cada linha e sentido, usa o shape mais frequente nas viagens de domingo 25/10/2026, corta na
caixa do mapa (53,303-53,346 N x 6,262-6,198 O, com margem) e descarta pontos a menos de 8 m do anterior.
Saida: {"<linha>|<sentido>": {"shape_id": ..., "segmentos": [[[lat, lon], ...], ...]}}
"""
import csv, sys, os, json, math, collections
gtfs, out = sys.argv[1], sys.argv[2]
DATE = '20261025'
LAT0, LAT1, LON0, LON1 = 53.300, 53.349, -6.266, -6.194   # caixa do mapa + margem
def rd(n):
    with open(os.path.join(gtfs, n), encoding='utf-8-sig', newline='') as f:
        yield from csv.DictReader(f)
act = {r['service_id'] for r in rd('calendar.txt') if r['start_date'] <= DATE <= r['end_date'] and r['sunday'] == '1'}
for r in rd('calendar_dates.txt'):
    if r['date'] == DATE:
        (act.add if r['exception_type'] == '1' else act.discard)(r['service_id'])
routes = {r['route_id']: r['route_short_name'] for r in rd('routes.txt')}
cont = collections.defaultdict(collections.Counter)
for t in rd('trips.txt'):
    if t['service_id'] in act and t.get('shape_id'):
        cont[(routes[t['route_id']], t['direction_id'])][t['shape_id']] += 1
escolha = {k: c.most_common(1)[0][0] for k, c in cont.items()}
pts = collections.defaultdict(list)
alvo = set(escolha.values())
for r in rd('shapes.txt'):
    if r['shape_id'] in alvo:
        pts[r['shape_id']].append((int(r['shape_pt_sequence']), float(r['shape_pt_lat']), float(r['shape_pt_lon'])))
def dist(a, b):
    return math.hypot((a[0]-b[0])*111320, (a[1]-b[1])*111320*math.cos(math.radians(53.325)))
res = {}
for (linha, sentido), sid in sorted(escolha.items()):
    segs, cur = [], []
    for _, la, lo in sorted(pts[sid]):
        if LAT0 <= la <= LAT1 and LON0 <= lo <= LON1:
            p = (round(la, 5), round(lo, 5))
            if not cur or dist(cur[-1], p) >= 8:
                cur.append(p)
        elif cur:
            if len(cur) > 1: segs.append(cur)
            cur = []
    if len(cur) > 1: segs.append(cur)
    if segs:
        res[f'{linha}|{sentido}'] = {'shape_id': sid, 'segmentos': segs}
json.dump(res, open(out, 'w'), ensure_ascii=False, separators=(',', ':'))
print('ok', len(res), 'linha|sentido na caixa', file=sys.stderr)
