import json,glob,xml.etree.ElementTree as ET,collections
from pathlib import Path
from shapely.geometry import shape,Point,Polygon,LineString
out=Path('belauri-map/dist/data'); boundary=shape(json.loads((out/'boundary.geojson').read_text())['features'][0]['geometry'])
nodes={};objects={}
for f in glob.glob('/tmp/belauri-map-*.osm'):
 try:r=ET.parse(f).getroot()
 except ET.ParseError:continue
 for el in r:
  if el.tag=='node':nodes[el.attrib['id']]=(float(el.attrib['lon']),float(el.attrib['lat']))
  if el.tag in ['node','way','relation']:objects[(el.tag,el.attrib['id'])]=el
features=[]
for (typ,oid),el in objects.items():
 t={x.attrib['k']:x.attrib['v'] for x in el.findall('tag')}; a=t.get('amenity');cat=None
 if a=='school':cat='school'
 elif a in ['hospital','clinic','doctors'] or t.get('healthcare') in ['hospital','clinic','health_post','centre']:cat='hospital'
 elif 'brick' in t.get('industrial','') or 'brick' in t.get('product','') or t.get('man_made')=='kiln':cat='kiln'
 elif t.get('office')=='government' or a=='townhall' or (typ=='way' and oid=='1092534990'):cat='government'
 if not cat:continue
 if typ=='node':p=Point(nodes[oid])
 elif typ=='way':
  coords=[nodes[n.attrib['ref']] for n in el.findall('nd') if n.attrib['ref'] in nodes]
  if len(coords)<2:continue
  p=Polygon(coords).representative_point() if len(coords)>=4 and coords[0]==coords[-1] else LineString(coords).interpolate(.5,normalized=True)
 else:continue
 if not boundary.covers(p):continue
 name=t.get('name:en') or t.get('name') or {'school':'Unnamed school','hospital':'Unnamed health facility','kiln':'Unnamed brick kiln','government':'Unnamed government office'}[cat]
 features.append({'type':'Feature','geometry':{'type':'Point','coordinates':[p.x,p.y]},'properties':{'name':name,'name_ne':t.get('name:ne'),'category':cat,'facility_type':a or t.get('healthcare') or t.get('industrial') or t.get('office') or t.get('man_made'),'osm_id':f'{typ}/{oid}','source_url':f'https://www.openstreetmap.org/{typ}/{oid}','tags':t}})
kilns=[f for f in features if f['properties']['tags'].get('man_made')=='kiln']
features=[f for f in features if not (f['properties']['tags'].get('industrial')=='brickyard' and any(Point(f['geometry']['coordinates']).distance(Point(k['geometry']['coordinates']))<0.001 for k in kilns))]
(out/'places.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features},ensure_ascii=False))
counts=dict(collections.Counter(f['properties']['category'] for f in features));print(counts)
for f in features:print(f['properties']['category'],f['properties']['name'])
(out/'provenance.json').write_text(json.dumps({'retrieved_date':'2026-10-13','boundary':{'source':'OpenStreetMap contributors','relation_id':5927493,'url':'https://www.openstreetmap.org/relation/5927493','download_url':'https://www.openstreetmap.org/api/0.6/relation/5927493/full'},'places':{'source':'OpenStreetMap contributors','endpoint':'https://www.openstreetmap.org/api/0.6/map','method':'13 bounding-box tiles; deduplicated by OSM object ID; brickyard sites within 100 m of a mapped kiln represented by the kiln; representative points clipped to Belauri polygon','counts':counts,'categories':{'school':'amenity=school','hospital':'amenity hospital/clinic/doctors or healthcare hospital/clinic/health_post/centre','kiln':'industrial or product contains brick; man_made=kiln','government':'office=government or amenity=townhall, plus OSM building way/1092534990 named belauri municipality kanchanpur'},'completeness':'Community-mapped locations only, not a complete official inventory. Health layer includes hospitals, clinics, and health posts. Government layer includes government offices, not only municipal offices. Unnamed mapped features retain descriptive labels. Locations are current map features and are not historical 2024 locations.'},'license':'ODbL 1.0','attribution':'© OpenStreetMap contributors','license_url':'https://www.openstreetmap.org/copyright'},ensure_ascii=False,indent=2))
