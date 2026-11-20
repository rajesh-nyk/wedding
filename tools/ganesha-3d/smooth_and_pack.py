"""Step 2 of the Ganesha 3D pipeline.

Takes the compact mesh written by decimate.py, recomputes smooth surface normals
(the AI-generated mesh is bumpy, which made the skin look like crumpled foil),
and packs the result as base64 JSON so any static host will serve it.

Usage: python3 smooth_and_pack.py ganesha.bin ../../wedding/website-3/ganesha-mesh.json [rounds=4]

Mesh layout (little endian): uint32 header length, JSON header {v,t,min,max} padded to 4 bytes,
then positions uint16x3 (normalised to min..max), normals int8x4, uv uint16x2, indices uint32x3.
"""
import base64, json, struct, sys
import numpy as np

src, dst = sys.argv[1], sys.argv[2]
rounds = int(sys.argv[3]) if len(sys.argv) > 3 else 4
d = open(src, 'rb').read()
hl = struct.unpack('<I', d[:4])[0]; h = json.loads(d[4:4 + hl]); o = 4 + hl; v, t = h['v'], h['t']
q = np.frombuffer(d, np.uint16, v * 3, o).reshape(-1, 3); o += v * 6
o += v * 4  # old normals, replaced below
uq = np.frombuffer(d, np.uint16, v * 2, o).reshape(-1, 2); o += v * 4
T = np.frombuffer(d, np.uint32, t * 3, o).reshape(-1, 3).astype(np.int64)
P = q.astype(np.float64)

# vertices at the same spot (split only by texture seams) share one smooth direction
_, pid = np.unique(q, axis=0, return_inverse=True); pid = pid.ravel(); npts = pid.max() + 1
a, b, c = P[T[:, 0]], P[T[:, 1]], P[T[:, 2]]; fn = np.cross(b - a, c - a)
N = np.zeros((npts, 3))
for k in range(3): np.add.at(N, pid[T[:, k]], fn)
N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
E = pid[np.concatenate([T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]])]
for _ in range(rounds):
    acc = N.copy(); np.add.at(acc, E[:, 0], N[E[:, 1]]); np.add.at(acc, E[:, 1], N[E[:, 0]])
    N = acc / (np.linalg.norm(acc, axis=1, keepdims=True) + 1e-12)
nn = np.round(N[pid] * 127).astype(np.int8); nn = np.concatenate([nn, np.zeros((v, 1), np.int8)], 1)

out = d[:4 + hl] + q.tobytes() + nn.tobytes() + uq.tobytes() + T.astype(np.uint32).tobytes()
json.dump({'b': base64.b64encode(out).decode()}, open(dst, 'w'))
print('wrote', dst, len(out), 'bytes before base64')
