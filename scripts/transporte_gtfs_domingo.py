"""Analise GTFS: linhas com paradas perto do portao da Anglesea Road, servico de domingo 25/10/2026.
uso: python3 -I gtfs_sunday.py <gtfs_dir> <saida.json> [raio_m]
"""
import csv, sys, math, json, collections, os
gtfs, out = sys.argv[1], sys.argv[2]
RAIO = float(sys.argv[3]) if len(sys.argv) > 3 else 1500
DATE = '20261025'
G = (53.32578, -6.23124)   # portao Anglesea Road (premissa: meio da testada do RDS Arena)
M = (53.32830, -6.22920)   # portao principal Merrion Road

def hav(a, b):
    R = 6371000; p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = p2 - p1; dl = math.radians(b[1] - a[1])
    h = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(h))

def rd(name):
    with open(os.path.join(gtfs, name), encoding='utf-8-sig', newline='') as f:
        yield from csv.DictReader(f)

# servicos ativos no domingo 25/10
active = set()
dow = 6  # sunday
for r in rd('calendar.txt'):
    if r['start_date'] <= DATE <= r['end_date'] and r['sunday'] == '1':
        active.add(r['service_id'])
for r in rd('calendar_dates.txt'):
    if r['date'] == DATE:
        if r['exception_type'] == '1': active.add(r['service_id'])
        else: active.discard(r['service_id'])
print('servicos ativos em', DATE, sorted(active), file=sys.stderr)

routes = {r['route_id']: r for r in rd('routes.txt')}
agencies = {r['agency_id']: r['agency_name'] for r in rd('agency.txt')}
stops = {r['stop_id']: r for r in rd('stops.txt')}
near = {sid: hav(G, (float(s['stop_lat']), float(s['stop_lon']))) for sid, s in stops.items()
        if s.get('stop_lat') and hav(G, (float(s['stop_lat']), float(s['stop_lon']))) <= RAIO}
print('paradas no raio', len(near), file=sys.stderr)

# trips de domingo
trips = {}
for t in rd('trips.txt'):
    if t['service_id'] in active:
        trips[t['trip_id']] = t
# todas as trips de domingo (para contar linhas que rodam no domingo) e trips de qualquer dia (para 7E/27X)
all_trips_by_route = collections.Counter()
sun_trips_by_route = collections.Counter()
for t in rd('trips.txt'):
    all_trips_by_route[t['route_id']] += 1
    if t['service_id'] in active: sun_trips_by_route[t['route_id']] += 1

# stop_times: para trips de domingo, paradas no raio -> horarios; tambem registrar todas as paradas por rota (qualquer dia) para ver se a rota passa no raio
route_stops_any = collections.defaultdict(set)      # route_id -> stop_ids no raio (qualquer dia)
dep = collections.defaultdict(list)                  # (route_id, direction_id, stop_id) -> [departure seconds]
trip_route_any = {}
for t in rd('trips.txt'):
    trip_route_any[t['trip_id']] = (t['route_id'], t['direction_id'], t['trip_headsign'])
heads = collections.defaultdict(set)
for st in rd('stop_times.txt'):
    sid = st['stop_id']
    if sid not in near: continue
    rid, d, hs = trip_route_any[st['trip_id']]
    route_stops_any[rid].add(sid)
    if st['trip_id'] in trips:
        hh, mm, ss = st['departure_time'].split(':')
        dep[(rid, d, sid)].append(int(hh)*3600 + int(mm)*60 + int(ss))
        heads[(rid, d)].add(hs)

def hw(times, a, b):
    ts = sorted(t for t in times if a*3600 <= t < b*3600)
    if len(ts) < 2: return len(ts), None
    gaps = [ (ts[i+1]-ts[i])/60 for i in range(len(ts)-1) ]
    return len(ts), round(sum(gaps)/len(gaps), 1)

res = []
for rid, sids in route_stops_any.items():
    r = routes[rid]
    for d in ('0', '1'):
        cand = [(sid, near[sid]) for sid in sids if (rid, d, sid) in dep]
        if not cand:
            # rota passa mas nao no domingo nessa direcao
            continue
        cand.sort(key=lambda x: x[1])
        best = cand[0]
        entry = {
            'linha': r['route_short_name'], 'route_id': rid, 'operador': agencies.get(r['agency_id'], r['agency_id']),
            'nome_longo': r['route_long_name'], 'sentido': d, 'headsigns': sorted(heads[(rid, d)]),
            'parada_mais_proxima': {'stop_id': best[0], 'codigo': stops[best[0]]['stop_code'], 'nome': stops[best[0]]['stop_name'],
                                    'lat': float(stops[best[0]]['stop_lat']), 'lon': float(stops[best[0]]['stop_lon']),
                                    'dist_reta_anglesea_m': round(best[1]),
                                    'dist_reta_merrion_m': round(hav(M, (float(stops[best[0]]['stop_lat']), float(stops[best[0]]['stop_lon']))))},
            'paradas_no_raio': [{'codigo': stops[s]['stop_code'], 'nome': stops[s]['stop_name'], 'dist_reta_anglesea_m': round(near[s])} for s, _ in cand],
        }
        times = dep[(rid, d, best[0])]
        entry['domingo'] = {
            'viagens_dia': len(times),
            'primeira': min(times), 'ultima': max(times),
            'viagens_7_18': hw(times, 7, 18)[0], 'headway_medio_min_7_18': hw(times, 7, 18)[1],
            'viagens_8_11': hw(times, 8, 11)[0], 'headway_medio_min_8_11': hw(times, 8, 11)[1],
            'viagens_11_17': hw(times, 11, 17)[0], 'headway_medio_min_11_17': hw(times, 11, 17)[1],
            'por_hora': {str(h): sum(1 for t in times if h*3600 <= t < (h+1)*3600) for h in range(6, 19)},
        }
        res.append(entry)

# rotas que passam no raio mas sem servico de domingo
sem_dom = []
for rid in route_stops_any:
    if sun_trips_by_route[rid] == 0:
        r = routes[rid]
        sem_dom.append({'linha': r['route_short_name'], 'route_id': rid, 'nome_longo': r['nome_longo'] if 'nome_longo' in r else r['route_long_name'],
                        'viagens_total_feed': all_trips_by_route[rid], 'viagens_domingo': 0})
json.dump({'data': DATE, 'raio_m': RAIO, 'portao_anglesea': G, 'portao_merrion': M, 'servicos_ativos': sorted(active),
           'linhas': sorted(res, key=lambda e: (e['linha'], e['sentido'])), 'sem_servico_domingo': sem_dom}, open(out, 'w'), ensure_ascii=False, indent=1)
print('ok', len(res), 'linha/sentido;', len(sem_dom), 'sem domingo', file=sys.stderr)
