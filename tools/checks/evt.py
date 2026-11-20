import asyncio
from playwright.async_api import async_playwright
async def run(b,W,H,mob):
    c=await b.new_context(viewport={'width':W,'height':H},is_mobile=mob,has_touch=mob)
    pg=await c.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto('file:///home/claude/wedding/wedding/website-3/index.html');await pg.wait_for_timeout(3500)
    top,ln=await pg.evaluate("(()=>{const b=document.querySelector(window.__S||'.ev-rc');return [b.getBoundingClientRect().top+scrollY,b.offsetHeight-innerHeight]})()")
    ims=[]
    for f in (.8,.86,.9,.94,.98,1.02,1.06,1.12,1.2,1.3):
        await pg.evaluate(f"scrollTo(0,{top}+{ln}*{f})");await pg.wait_for_timeout(700);n=f'/tmp/ev_{W}_{f}.png';await pg.screenshot(path=n);ims.append(n)
    print(W,errs);await c.close();return ims
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        a=await run(b,390,844,True);d=await run(b,1470,800,False);await b.close()
    from PIL import Image
    s=Image.new('RGB',(10*180,390+100),'white')
    for i,n in enumerate(a):s.paste(Image.open(n).resize((180,390)),(i*180,0))
    for i,n in enumerate(d):s.paste(Image.open(n).resize((180,98)),(i*180,392))
    s.save('/tmp/ev.png')
asyncio.run(main())
