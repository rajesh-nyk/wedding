import asyncio
from playwright.async_api import async_playwright
U='file:///home/claude/wedding/wedding/website-3/index.html'
async def run(b,W,H,mob):
    c=await b.new_context(viewport={'width':W,'height':H},is_mobile=mob,has_touch=mob)
    pg=await c.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto(U);await pg.wait_for_timeout(3500)
    top,ln=await pg.evaluate("(()=>{const b=document.querySelector('#sapt');return [b.getBoundingClientRect().top+scrollY,b.offsetHeight-innerHeight]})()")
    shots=[]
    for f in (-.12,.06,.2,.45,.75,.95):
        await pg.evaluate(f"scrollTo(0,{top}+{ln}*{f})");await pg.wait_for_timeout(1300)
        n=f'/tmp/sp_{W}_{f}.png';await pg.screenshot(path=n);shots.append(n)
    # tap step 3 from the start
    await pg.evaluate(f"scrollTo(0,{top}+{ln}*.06)");await pg.wait_for_timeout(1200)
    bb=await pg.evaluate("(()=>{const r=document.querySelectorAll('#sapt .sp-step')[2].getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()")
    if mob: await pg.tap('#sapt .sp-step:nth-of-type(3)')
    else: await pg.mouse.click(*bb)
    await pg.wait_for_timeout(2200);n=f'/tmp/sp_{W}_tap.png';await pg.screenshot(path=n);shots.append(n)
    print(W,'active step after tapping 3rd:',await pg.evaluate("[...document.querySelectorAll('#sapt .sp-step')].findIndex(e=>e.classList.contains('on'))+1"),errs)
    await c.close();return shots
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        a=await run(b,390,844,True);d=await run(b,1470,800,False)
        await b.close()
    from PIL import Image
    s=Image.new('RGB',(7*230,498+130),'white')
    for i,n in enumerate(a):s.paste(Image.open(n).resize((230,498)),(i*230,0))
    for i,n in enumerate(d):s.paste(Image.open(n).resize((230,125)),(i*230,503))
    s.save('/tmp/sp.png')
asyncio.run(main())
