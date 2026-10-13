import io, requests, h5py, json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
class HTTPFile(io.RawIOBase):
 def __init__(self,url):
  self.url=url; self.pos=0; self.session=requests.Session(); self.session.mount('https://',HTTPAdapter(max_retries=Retry(total=5,backoff_factor=0.5))); self.size=int(self.session.head(url).headers['Content-Length']); self.cache={}; self.block=262144
 def readable(self):return True
 def seekable(self):return True
 def tell(self):return self.pos
 def seek(self,offset,whence=0):
  self.pos=offset if whence==0 else self.pos+offset if whence==1 else self.size+offset
  return self.pos
 def readinto(self,b):
  data=self.read(len(b)); b[:len(data)]=data; return len(data)
 def read(self,size=-1):
  end=min(self.size,self.pos+size if size>=0 else self.size); out=[]
  while self.pos<end:
   block=self.pos//self.block; start=block*self.block
   if block not in self.cache:
    r=self.session.get(self.url,headers={'Range':f'bytes={start}-{min(self.size-1,start+self.block-1)}'}); r.raise_for_status()
    if r.status_code!=206:raise Exception('Range unsupported')
    self.cache[block]=r.content
   take=min(end-self.pos,self.block-self.pos%self.block);out.append(self.cache[block][self.pos%self.block:self.pos%self.block+take]);self.pos+=take
  return b''.join(out)
if __name__=='__main__':
 url='https://satpmdata.s3.amazonaws.com/V6GL03/CNNPM25/Monthly/AS/V6GL03.CNNPM25.AS.202401-202401.nc'
 with HTTPFile(url) as remote:
  with h5py.File(remote,'r') as f:
   for k in f:print(k,f[k].shape,dict(f[k].attrs))
