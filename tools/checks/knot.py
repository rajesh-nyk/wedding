import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/wedding/wedding/website-3/index.html'
async def run(b,W,H,mob):
    c=await b.new_context(viewport={'width':W,'height':H},is_mobile=mob,has_touch=mob)
    pg=await c.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto(U);await pg.wait_for_timeout(3500)
    top,ln=await pg.evaluate("(()=>{const b=document.querySelector('#knot');return [b.getBoundingClientRect().top+scrollY,b.offsetHeight-innerHeight]})()")
    shots=[]
    await pg.evaluate(f"scrollTo(0,{top}+{ln}*.11)");await pg.wait_for_timeout(1200)
    n=f'/tmp/kn_{W}_a.png';await pg.screenshot(path=n);shots.append(n)
    r=await pg.evaluate("(()=>{const r=document.querySelector('#knot .kst').getBoundingClientRect();return [r.left,r.top,r.width,r.height]})()")
    x=r[0]+r[2]*.2 if not mob else 60;y=r[1]+r[3]*.5
    y0=await pg.evaluate("scrollY")
    if mob:
        cdp=await c.new_cdp_session(pg)
        await cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
        for i in range(1,13):
            await cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+i*14,'y':y+1}]});await pg.wait_for_timeout(40)
            if i==6:n=f'/tmp/kn_{W}_mid.png';await pg.screenshot(path=n);shots.append(n)
        await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    else:
        await pg.mouse.move(x,y);await pg.mouse.down()
        for i in range(1,13):
            await pg.mouse.move(x+i*32,y);await pg.wait_for_timeout(40)
            if i==6:n=f'/tmp/kn_{W}_mid.png';await pg.screenshot(path=n);shots.append(n)
        await pg.mouse.up()
    st=await pg.evaluate("(()=>({}))()")
    for k in range(4):
        await pg.wait_for_timeout(1200);n=f'/tmp/kn_{W}_t{k}.png';await pg.screenshot(path=n);shots.append(n)
    y1=await pg.evaluate("scrollY");print(W,'auto scrolled',round(y1-y0),errs)
    await c.close();return shots
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        a=await run(b,390,844,True);d=await run(b,1470,800,False)
        await b.close()
    from PIL import Image
    s=Image.new('RGB',(6*260,563+150),'white')
    for i,n in enumerate(a):s.paste(Image.open(n).resize((260,563)),(i*260,0))
    for i,n in enumerate(d):s.paste(Image.open(n).resize((260,141)),(i*260,570))
    s.save('/tmp/kn.png')
asyncio.run(main())
