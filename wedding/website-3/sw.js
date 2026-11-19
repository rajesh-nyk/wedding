// Wedding site offline support: pages load from the network when possible,
// images are kept on the phone after the first visit.
const V='rc-v1';
const CORE=['/','/index.html','/manifest.webmanifest','/icon-192.png','/icon-512.png'];
const ASSETS=['/banana.webp', '/bh/base.webp', '/bh/dn1.webp', '/bh/dn2.webp', '/bh/dn3.webp', '/bh/dr1.webp', '/bh/dr2.webp', '/bh/dr3.webp', '/bh/dr4.webp', '/bh/glowmask.webp', '/bh/heart.webp', '/bh/hero.webp', '/bh/lampL.webp', '/bh/lampR.webp', '/bh/palmL.webp', '/bh/palmR.webp', '/bh/pkL.webp', '/bh/pkR.webp', '/ganesha-sketch.webp', '/ganesha.webp', '/mo/m1.webp', '/mo/m2.webp', '/mo/m3.webp', '/mo/m4.webp', '/mo/m5.webp', '/mo/m6.webp', '/nb/base.webp', '/nb/dn1.webp', '/nb/dn2.webp', '/nb/dn3.webp', '/nb/dr1.webp', '/nb/dr2.webp', '/nb/dr3.webp', '/nb/dr4.webp', '/nb/glowmask.webp', '/nb/lampL.webp', '/nb/lampR.webp', '/nb/palmL.webp', '/nb/palmR.webp', '/nb/pkL.webp', '/nb/pkR.webp', '/rc/base.webp', '/rc/dn1.webp', '/rc/dn2.webp', '/rc/dn3.webp', '/rc/dr1.webp', '/rc/dr2.webp', '/rc/dr3.webp', '/rc/dr4.webp', '/rc/glowmask.webp', '/rc/hero.webp', '/rc/lampL.webp', '/rc/lampR.webp', '/rc/palmL.webp', '/rc/palmR.webp', '/rc/pkL.webp', '/rc/pkR.webp', '/sambalpuri.webp', '/sweets.webp', '/wheel-sm.webp', '/wheel.webp'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(CORE).then(()=>c.addAll(ASSETS).catch(()=>{}))));self.skipWaiting();});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET')return;
 if(r.mode==='navigate'){e.respondWith(fetch(r).then(res=>{const cp=res.clone();caches.open(V).then(c=>c.put('/',cp));return res}).catch(()=>caches.match('/')));return}
 e.respondWith(caches.match(r).then(hit=>hit||fetch(r).then(res=>{if(res.ok&&(r.url.startsWith(self.location.origin)||r.url.includes('fonts.g'))){const cp=res.clone();caches.open(V).then(c=>c.put(r,cp))}return res})));
});
