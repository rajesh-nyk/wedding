import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/wedding/wedding/website-3/index.html'
async def run(b,W,H,mob):
    c=await b.new_context(viewport={'width':W,'height':H},is_mobile=mob,has_touch=mob)
    pg=await c.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto(U);await pg.wait_for_timeout(3500)
    top,ln=await pg.evaluate("(()=>{const b=document.querySelector('#bless');return [b.getBoundingClientRect().top+scrollY,b.offsetHeight-innerHeight]})()")
    shots=[]
    for f in (.0,.06,.13):
        await pg.evaluate(f"scrollTo(0,{top}+{ln}*{f})");await pg.wait_for_timeout(900)
        n=f'/tmp/dy_{W}_{f}.png';await pg.screenshot(path=n);shots.append(n)
    # hold on the diya
    bx=await pg.evaluate("(()=>{const r=document.querySelector('#bless .diya').getBoundingClientRect();return [r.left+r.width*.4545,r.top+r.height*.6]})()")
    y0=await pg.evaluate("scrollY")
    if mob:
        cdp=await c.new_cdp_session(pg)
        await cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':bx[0],'y':bx[1]}]})
        await pg.wait_for_timeout(600);n=f'/tmp/dy_{W}_hold.png';await pg.screenshot(path=n);shots.append(n)
        await pg.wait_for_timeout(800)
        await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    else:
        await pg.mouse.move(*bx);await pg.mouse.down()
        await pg.wait_for_timeout(600);n=f'/tmp/dy_{W}_hold.png';await pg.screenshot(path=n);shots.append(n)
        await pg.wait_for_timeout(800);await pg.mouse.up()
    for k in range(4):
        await pg.wait_for_timeout(1100);n=f'/tmp/dy_{W}_auto{k}.png';await pg.screenshot(path=n);shots.append(n)
    y1=await pg.evaluate("scrollY")
    print(W,'scrolled by auto:',round(y1-y0),'lit:',await pg.evaluate("1"),errs)
    await c.close();return shots
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        a=await run(b,390,844,True);d=await run(b,1470,800,False)
        await b.close()
    from PIL import Image
    s=Image.new('RGB',(8*200,433+8*0+250),'white')
    for i,n in enumerate(a):s.paste(Image.open(n).resize((200,433)),(i*200,0))
    for i,n in enumerate(d):s.paste(Image.open(n).resize((200,109)),(i*200,440))
    s.save('/tmp/dy.png')
asyncio.run(main())
