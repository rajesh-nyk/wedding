import asyncio
from playwright.async_api import async_playwright
JS="""(()=>{const out=[];const vw=innerWidth;
 if(document.documentElement.scrollWidth>vw+1)out.push('page wider than screen: '+document.documentElement.scrollWidth);
 const vis=e=>{const cs=getComputedStyle(e);if(cs.visibility==='hidden'||cs.display==='none')return false;let n=e;while(n&&n!==document.body){const o=parseFloat(getComputedStyle(n).opacity);if(o<.05)return false;n=n.parentElement}const r=e.getBoundingClientRect();return r.width>0&&r.bottom>0&&r.top<innerHeight};
 // text must sit inside its framed box
 const boxes=['.rc','.kk','.cd > div','#bar span','.kk-again','.card','.skyfoot','.sp-say','.ev-info'];
 for(const sel of boxes)for(const b of document.querySelectorAll(sel)){if(!vis(b))continue;const R=b.getBoundingClientRect();
  const w=document.createTreeWalker(b,NodeFilter.SHOW_TEXT);let t;while(t=w.nextNode()){if(!t.textContent.trim())continue;const el=t.parentElement;if(!vis(el))continue;
   const rg=document.createRange();rg.selectNodeContents(t);for(const r of rg.getClientRects()){if(r.width<1)continue;
    if(r.left<R.left-2||r.right>R.right+2||r.top<R.top-2||r.bottom>R.bottom+2)out.push(sel+' text outside: "'+t.textContent.trim().slice(0,30)+'" '+[r.left-R.left,R.right-r.right,r.top-R.top,R.bottom-r.bottom].map(Math.round))}}}
 // any visible text cut by the screen edge
 const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let t;while(t=w.nextNode()){if(!t.textContent.trim())continue;const el=t.parentElement;if(!el||el.closest('.giant,#loader,.pd-head,.wm,script,style')||!vis(el))continue;
  const rg=document.createRange();rg.selectNodeContents(t);for(const r of rg.getClientRects()){if(r.width<1||r.bottom<0||r.top>innerHeight)continue;if(r.left<-1||r.right>vw+1)out.push('text off screen edge: "'+t.textContent.trim().slice(0,30)+'"')}}
 return out})()"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        for W,H in ((375,667),(390,844),(430,932),(820,1180),(1280,680),(1470,800),(1920,1080)):
            pg=await b.new_page(viewport={'width':W,'height':H},is_mobile=W<700,has_touch=W<1000)
            await pg.goto('file:///home/claude/wedding/wedding/website-3/index.html');await pg.wait_for_timeout(3500)
            tot=await pg.evaluate("document.documentElement.scrollHeight-innerHeight");y=0;found={}
            while y<=tot:
                await pg.evaluate(f"scrollTo(0,{y})");await pg.wait_for_timeout(450)
                for m in await pg.evaluate(JS):found.setdefault(m,y)
                y+=H*0.35
            print(W,H,'issues:',len(found))
            for m,yy in list(found.items())[:12]:print('   ',int(yy),m)
            await pg.close()
        await b.close()
asyncio.run(main())
