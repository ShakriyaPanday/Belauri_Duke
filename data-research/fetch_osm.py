import requests,concurrent.futures
boxes=[(80.2561,28.6287,80.3421,28.7007),(80.3421,28.6287,80.4281,28.7007),(80.2561,28.7007,80.3421,28.7727),(80.3421,28.7007,80.4281,28.7727)]
todo=[]
for i,b in enumerate(boxes):
 if i==0:continue
 w,s,e,n=b;x=(w+e)/2;y=(s+n)/2
 for j,t in enumerate([(w,s,x,y),(x,s,e,y),(w,y,x,n),(x,y,e,n)]):todo.append((f'{i}-{j}',t))
def get(x):
 i,b=x;r=requests.get('https://www.openstreetmap.org/api/0.6/map',params={'bbox':','.join(map(str,b))},timeout=60)
 open(f'/tmp/belauri-map-{i}.osm','w').write(r.text);print(i,r.status_code,len(r.content))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:list(e.map(get,todo))
