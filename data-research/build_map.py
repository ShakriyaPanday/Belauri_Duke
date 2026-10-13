import json,xml.etree.ElementTree as ET
from pathlib import Path
from shapely.geometry import LineString,mapping
from shapely.ops import polygonize,unary_union
root=ET.parse('/tmp/belauri-boundary.osm').getroot()
nodes={n.attrib['id']:(float(n.attrib['lon']),float(n.attrib['lat'])) for n in root.findall('node')}
ways={w.attrib['id']:[nodes[n.attrib['ref']] for n in w.findall('nd')] for w in root.findall('way')}
r=next(r for r in root.findall('relation') if r.attrib['id']=='5927493')
lines=[LineString(ways[m.attrib['ref']]) for m in r.findall('member') if m.attrib['type']=='way' and m.attrib['role']=='outer']
poly=unary_union(list(polygonize(lines)))
assert poly.is_valid and not poly.is_empty
out=Path('belauri-map/dist/data')
feature={'type':'Feature','properties':{'name':'Belauri Municipality','name_ne':'बेलौरी नगरपालिका','osm_relation':5927493,'source':'OpenStreetMap contributors','source_url':'https://www.openstreetmap.org/relation/5927493'},'geometry':mapping(poly)}
(out/'boundary.geojson').write_text(json.dumps({'type':'FeatureCollection','features':[feature]},ensure_ascii=False))
print(poly.bounds,poly.geom_type)
