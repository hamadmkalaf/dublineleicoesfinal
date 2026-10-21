# Lê o extrato OSM de Dublin (BBBike, .osm.pbf) e grava as vias num pickle.
# Uso: python3 -I 1_carrega_osm.py Dublin.osm.pbf ways.pkl   (requer pip install osmium)
# Extrato: https://download.bbbike.org/osm/bbbike/Dublin/Dublin.osm.pbf
import osmium, pickle, sys, math
DRIVE={'motorway','motorway_link','trunk','trunk_link','primary','primary_link','secondary','secondary_link','tertiary','tertiary_link','unclassified','residential','living_street','service','road'}
class H(osmium.SimpleHandler):
    def __init__(s):
        super().__init__(); s.ways={}
    def way(s,w):
        hw=w.tags.get('highway')
        if hw is None: return
        try: coords=[(n.ref,n.lat,n.lon) for n in w.nodes]
        except osmium.InvalidLocationError: return
        s.ways[w.id]=dict(hw=hw,name=w.tags.get('name',''),ref=w.tags.get('ref',''),oneway=w.tags.get('oneway',''),
            access=w.tags.get('access',''),motor=w.tags.get('motor_vehicle',''),service=w.tags.get('service',''),
            junction=w.tags.get('junction',''),maxspeed=w.tags.get('maxspeed',''),bridge=w.tags.get('bridge',''),
            nodes=coords,drive=hw in DRIVE)
h=H(); h.apply_file(sys.argv[1],locations=True)
pickle.dump(h.ways,open(sys.argv[2],'wb'))
print(len(h.ways),'ways', sum(1 for w in h.ways.values() if w['drive']),'drivable')
