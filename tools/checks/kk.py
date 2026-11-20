import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/wedding/wedding/website-3/index.html'
async def run(b,W,H,mob):
    c=await b.new_context(viewport={'width':W,'height':H},is_mobile=mob,has_touch=mob)
    pg=await c.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto(U);await pg.wait_for_timeout(3500)
    await pg.evaluate("document.querySelector('#kk').scrollIntoView({block:'center'})");await pg.wait_for_timeout(1500)
    shots=[];n=f'/tmp/kk_{W}_0.png';await pg.screenshot(path=n);shots.append(n)
    wr=await pg.evaluate("(()=>{const r=document.querySelector('.kk-water').getBoundingClientRect();const c=document.querySelector('.kk-cowrie');return [r.left,r.top,r.width,r.height,parseFloat(c.style.left)/100,parseFloat(c.style.top)/100]})()")
    L,T,Wd,Ht,kx,ky=wr
    miss=[(0.5 if kx<0.5 else 0.2,0.2),(1-kx,1-ky)]
    for mx,my in miss:
        if mob: await pg.touchscreen.tap(L+Wd*mx,T+Ht*my)
        else: await pg.mouse.click(L+Wd*mx,T+Ht*my)
        await pg.wait_for_timeout(500)
    n=f'/tmp/kk_{W}_1.png';await pg.screenshot(path=n);shots.append(n)
    print(W,'msg after misses:',await pg.text_content('.kk-msg'))
    if mob: await pg.touchscreen.tap(L+Wd*kx,T+Ht*ky)
    else: await pg.mouse.click(L+Wd*kx,T+Ht*ky)
    await pg.wait_for_timeout(700);n=f'/tmp/kk_{W}_2.png';await pg.screenshot(path=n);shots.append(n)
    print(W,'msg after hit:',await pg.text_content('.kk-msg'),errs)
    await c.close();return shots
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        a=await run(b,390,844,True);d=await run(b,1470,800,False)
        await b.close()
    from PIL import Image
    s=Image.new('RGB',(3*300+3*420,650),'white')
    for i,n in enumerate(a):s.paste(Image.open(n).resize((300,650)),(i*300,0))
    for i,n in enumerate(d):s.paste(Image.open(n).resize((420,229)),(900+i*420,0))
    s.save('/tmp/kk.png')
asyncio.run(main())
