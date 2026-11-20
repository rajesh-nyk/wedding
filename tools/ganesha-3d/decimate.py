import json,struct,numpy as np,sys,time
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
d=open('g.glb','rb').read();cl=struct.unpack('<I',d[12:16])[0];j=json.loads(d[20:20+cl])
off=20+cl;bl=struct.unpack('<I',d[off:off+4])[0];B=d[off+8:off+8+bl]
def acc(i):
    a=j['accessors'][i];bv=j['bufferViews'][a['bufferView']];o=bv.get('byteOffset',0)+a.get('byteOffset',0)
    dt={5126:np.float32,5125:np.uint32,5123:np.uint16}[a['componentType']];n={'SCALAR':1,'VEC2':2,'VEC3':3}[a['type']]
    return np.frombuffer(B,dtype=dt,count=a['count']*n,offset=o).reshape(-1,n) if n>1 else np.frombuffer(B,dtype=dt,count=a['count'],offset=o)
P=acc(0).astype(np.float64);UV=acc(1).astype(np.float64);N=acc(2).astype(np.float64);I=acc(3).reshape(-1,3).astype(np.int64)
V=len(P);t=time.time()
g=coo_matrix((np.ones(I.size),(np.repeat(I[:,0],1).tolist() and np.concatenate([I[:,0],I[:,1],I[:,2]]),np.concatenate([I[:,1],I[:,2],I[:,0]]))),shape=(V,V))
nc,chart=connected_components(g,directed=False);print('charts',nc,round(time.time()-t,1))
target=int(sys.argv[1]);lo,hi=0.001,0.05
mn=P.min(0)
def run(cs):
    c=np.floor((P-mn)/cs).astype(np.int64);cell=(c[:,0]*100000+c[:,1])*100000+c[:,2]
    cu,cinv=np.unique(cell,return_inverse=True)
    key=cinv.astype(np.int64)*(nc+1)+chart
    ku,kinv=np.unique(key,return_inverse=True)
    T=kinv[I];C=cinv[I]
    ok=(C[:,0]!=C[:,1])&(C[:,1]!=C[:,2])&(C[:,0]!=C[:,2])
    return cu,cinv,ku,kinv,T[ok]
for it in range(18):
    cs=(lo*hi)**.5;r=run(cs);n=len(r[4])
    if n>target:lo=cs
    else:hi=cs
cs=hi;cu,cinv,ku,kinv,T=run(cs);print('cell',cs,'tris',len(T))
# positions: shared per spatial cell (no cracks); uv and normal per (cell, chart)
cp=np.zeros((len(cu),3));np.add.at(cp,cinv,P);cn=np.bincount(cinv,minlength=len(cu))[:,None];cp/=cn
kcell=(ku//(nc+1));pos=cp[kcell]
uv=np.zeros((len(ku),2));np.add.at(uv,kinv,UV);kn=np.bincount(kinv,minlength=len(ku))[:,None];uv/=kn
nr=np.zeros((len(ku),3));np.add.at(nr,kinv,N);nr/=np.linalg.norm(nr,axis=1,keepdims=True)+1e-9
# drop duplicate triangles and unused vertices
T=np.unique(np.sort(T,axis=1),axis=0,return_index=True)[1];T=run(cs)[4][np.sort(T)]
used=np.unique(T);remap=-np.ones(len(ku),np.int64);remap[used]=np.arange(len(used));T=remap[T];pos=pos[used];uv=uv[used];nr=nr[used]
print('verts',len(pos),'tris',len(T))
# pack: positions uint16 in bbox, normals int8, uv uint16, indices uint32
bmin=pos.min(0);bmax=pos.max(0);q=np.round((pos-bmin)/(bmax-bmin)*65535).astype(np.uint16)
nq=np.round(nr*127).astype(np.int8);nq=np.concatenate([nq,np.zeros((len(nq),1),np.int8)],1)
uq=np.round(np.clip(uv,0,1)*65535).astype(np.uint16)
blob=q.tobytes()+nq.tobytes()+uq.tobytes()+T.astype(np.uint32).tobytes()
hdr=json.dumps({'v':len(pos),'t':len(T),'min':bmin.tolist(),'max':bmax.tolist()}).encode()
hdr+=b' '*((4-len(hdr)%4)%4)
open(sys.argv[2],'wb').write(struct.pack('<I',len(hdr))+hdr+blob)
print('bytes',4+len(hdr)+len(blob))
