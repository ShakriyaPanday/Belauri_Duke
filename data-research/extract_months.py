from remote_extract import HTTPFile
import h5py,numpy as np,json,concurrent.futures
from shapely.geometry import shape,box
from pathlib import Path
root=Path(__file__).parent
geo=json.loads(Path('belauri-map/dist/data/boundary.geojson').read_text())
geom=shape(geo['features'][0]['geometry'] if geo['type']=='FeatureCollection' else geo['geometry'] if geo['type']=='Feature' else geo)
bounds=geom.bounds

def extract(month):
 cached=root/f'2024-{month:02d}.json'
 if cached.exists():return json.loads(cached.read_text())
 url=f'https://satpmdata.s3.amazonaws.com/V6GL03/CNNPM25/Monthly/AS/V6GL03.CNNPM25.AS.2024{month:02d}-2024{month:02d}.nc'
 with HTTPFile(url) as remote:
  with h5py.File(remote,'r') as f:
   lat=f['lat'][:];lon=f['lon'][:]
   iy=np.where((lat>=bounds[1]-.005)&(lat<=bounds[3]+.005))[0];ix=np.where((lon>=bounds[0]-.005)&(lon<=bounds[2]+.005))[0]
   values=f['PM25'][iy[0]:iy[-1]+1,ix[0]:ix[-1]+1]
   cells=[];weights=[];vals=[]
   for j,y in enumerate(lat[iy]):
    for i,x in enumerate(lon[ix]):
     intersection=geom.intersection(box(x-.005,y-.005,x+.005,y+.005))
     v=float(values[j,i])
     if not intersection.is_empty and intersection.area>0 and np.isfinite(v) and v>=0:
      weights.append(intersection.area*np.cos(np.radians(y))); vals.append(v)
      cells.append({'lat':round(float(y),5),'lon':round(float(x),5),'pm25':round(v,3)})
   result={'month':month,'mean':round(float(np.average(vals,weights=weights)),3),'minimum':round(min(vals),3),'maximum':round(max(vals),3),'cellCount':len(vals),'source':url,'cells':cells}
   (root/f'2024-{month:02d}.json').write_text(json.dumps(result))
   print(month,result['mean'],len(vals),flush=True)
   return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: months=list(pool.map(extract,range(1,13)))
data={'dataset':'SatPM V6.GL.03','year':2024,'pollutant':'PM2.5','units':'µg/m³','resolution':0.01,'status':'verified','method':'Municipal mean weighted by grid-cell overlap area and cosine of latitude. Cells intersect the OpenStreetMap Belauri municipality boundary (relation 5927493). Satellite/model-derived estimates, not local monitor observations.','boundarySource':'https://www.openstreetmap.org/relation/5927493','source':'https://www.satpm.org/v6-gl-03','license':'CC BY 4.0','months':months}
data['methodology']=data['method']
(root/'pm25-2024.json').write_text(json.dumps(data))
import csv
with (root/'pm25-2024.csv').open('w',newline='') as out:
 writer=csv.writer(out);writer.writerow(['year','month','mean_pm25_ug_m3','min_cell_pm25_ug_m3','max_cell_pm25_ug_m3','intersecting_cells','source_url'])
 for m in months:writer.writerow([2024,m['month'],m['mean'],m['minimum'],m['maximum'],m['cellCount'],m['source']])
