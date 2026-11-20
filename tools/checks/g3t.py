import asyncio
from playwright.async_api import async_playwright
async def run(b,W,H,mob):
    c=await b.new_context(viewport={'width':W,'height':H},is_mobile=mob,has_touch=mob,device_scale_factor=2 if mob else 1)
    pg=await c.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto('http://localhost:8822/');await pg.wait_for_timeout(4000)
    await pg.wait_for_function("document.querySelector('#bless').classList.contains('g3on')",timeout=180000)
    top,ln=await pg.evaluate("(()=>{const b=document.querySelector('#bless');return [b.getBoundingClientRect().top+scrollY,b.offsetHeight-innerHeight]})()")
    ims=[]
    for f in (.47,.52,.58,.64,.7,.76,.84,.97):
        await pg.evaluate(f"scrollTo(0,{top}+{ln}*.78*{f})");await pg.wait_for_timeout(2500)
        n=f'/tmp/g3s_{W}_{f}.png';await pg.screenshot(path=n);ims.append(n)
    print(W,errs);await c.close();return ims
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        a=await run(b,390,844,True);d=await run(b,1470,800,False);await b.close()
    from PIL import Image
    s=Image.new('RGB',(8*230,498+130),'white')
    for i,n in enumerate(a):s.paste(Image.open(n).resize((230,498)),(i*230,0))
    for i,n in enumerate(d):s.paste(Image.open(n).resize((230,125)),(i*230,502))
    s.save('/tmp/g3s.png')
asyncio.run(main())
