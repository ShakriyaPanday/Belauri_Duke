import json, math
from pathlib import Path
from shapely.geometry import shape
root=Path('dist/data')
b=json.loads((root/'boundary.geojson').read_text())
g=shape(b['features'][0]['geometry'])
assert g.is_valid
places=json.loads((root/'places.geojson').read_text())
assert len(places['features'])==68
assert all(g.covers(shape(f['geometry'])) for f in places['features'])
p=json.loads((root/'pm25-2024.json').read_text())
assert [m['month'] for m in p['months']]==list(range(1,13))
for m in p['months']:
    assert math.isfinite(m['mean']) and m['mean']>=0
    assert len(m['cells'])>0
    assert all(math.isfinite(c['pm25']) and c['pm25']>=0 for c in m['cells'])
    assert min(c['pm25'] for c in m['cells'])<=m['mean']<=max(c['pm25'] for c in m['cells'])
print('PASS: valid boundary, 68 contained facilities, 12 monthly PM records with valid grid estimates.')
