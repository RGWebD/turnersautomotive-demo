import asyncio,sys,json,io
from playwright.async_api import async_playwright
import http.server,threading,functools,socketserver
from PIL import Image
import imagehash
BASEURL=sys.argv[1] if len(sys.argv)>1 else None
if not BASEURL:
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*a):pass
    socketserver.TCPServer.allow_reuse_address=True
    srv=socketserver.ThreadingTCPServer(('127.0.0.1',8972),functools.partial(Q,directory='/workspace/turnersautomotive/site')); threading.Thread(target=srv.serve_forever,daemon=True).start()
    BASEURL='http://127.0.0.1:8972/'
PAGES=['index','services','shop','reviews','contact','404']
fails=[]
def F(m): fails.append(m); print('FAIL',m)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for w,h in [(1440,900),(390,844)]:
            for rm in ['no-preference','reduce']:
                ctx=await b.new_context(viewport={'width':w,'height':h},reduced_motion=rm)
                pg=await ctx.new_page(); errs=[]
                pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
                pg.on('pageerror',lambda e: errs.append(str(e)))
                for n in PAGES:
                    errs.clear()
                    url=BASEURL+(n+'.html')
                    r=await pg.goto(url,wait_until='load')
                    if n!='404' and r.status!=200: F(f'{n} status {r.status}')
                    H=await pg.evaluate('document.body.scrollHeight')
                    for y in range(0,H+900,450): await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(60)
                    await pg.wait_for_timeout(2400)
                    res=await pg.evaluate('''()=>{
                      const W=document.documentElement.clientWidth,sw=document.documentElement.scrollWidth;
                      const broken=[...document.images].filter(i=>i.getAttribute('src')&&i.complete&&i.naturalWidth===0).map(i=>i.getAttribute('src'));
                      const hidden=[...document.querySelectorAll('[data-r],.stagger>*,.reveal-h,.stage')].filter(e=>parseFloat(getComputedStyle(e).opacity)<0.99).length;
                      const counters=[...document.querySelectorAll('.odo .dg')].map(g=>{const r=g.getBoundingClientRect();const bs=[...g.querySelectorAll('b')];const vis=bs.find(b=>{const q=b.getBoundingClientRect();return Math.abs(q.top-r.top)<4});return [g.dataset.v,vis?vis.textContent:(bs.length?'none':g.textContent)]});
                      const ld=[...document.querySelectorAll('script[type="application/ld+json"]')].map(s=>s.textContent);
                      const imgs=[...document.images].filter(i=>i.closest('.tlb')===null&&i.getAttribute('src')).map(i=>i.currentSrc||i.src);
                      const titles=[document.title,(document.querySelector('meta[name=description]')||{}).content];
                      const h1=document.querySelectorAll('h1').length;
                      const ring=[...document.querySelectorAll('body *')].filter(e=>{const s=getComputedStyle(e);return s.position==='fixed'&&s.pointerEvents==='none'&&s.borderRadius.includes('50%')}).length;
                      return {W,sw,broken,hidden,counters,ld,imgs,titles,h1,ring}}''')
                    tag=f'{n}@{w}/{rm}'
                    if res['sw']>res['W']: F(f'{tag} overflow {res["sw"]}>{res["W"]}')
                    if res['broken']: F(f'{tag} broken {res["broken"]}')
                    if res['hidden']: F(f'{tag} hidden after scroll {res["hidden"]}')
                    for want,got in res['counters']:
                        if abs(float(want)-float(got))>1e-9: F(f'{tag} counter {want}!={got}')
                    if res['h1']!=1: F(f'{tag} h1 count {res["h1"]}')
                    if res['ring']: F(f'{tag} possible cursor ring')
                    e2=[e for e in errs if 'google' not in e.lower() and 'maps' not in e.lower()]
                    if e2: F(f'{tag} console {e2[:3]}')
                    if errs and not e2: print('note: 3rd-party map console msgs on',tag,len(errs))
                    for s in res['ld']:
                        try: g=json.loads(s)
                        except Exception as ex: F(f'{tag} bad json-ld {ex}'); continue
                    from collections import Counter
                    rep=[k for k,v in Counter(u.split('/')[-1].rsplit('-',1)[0] for u in res['imgs'] if not u.endswith('.svg')).items() if v>1]
                    if rep: F(f'{tag} repeated photo {rep}')
                    if w==390 and rm=='no-preference' and n=='index':
                        await pg.evaluate('scrollTo(0,0)'); await pg.click('.burger'); await pg.wait_for_timeout(700)
                        ok=await pg.evaluate("(()=>{const m=document.querySelector('.mnav');const r=m.getBoundingClientRect();return m.classList.contains('open')&&r.top>=-1&&getComputedStyle(m).visibility==='visible'})()")
                        if not ok: F('mobile menu did not open')
                        await pg.click('.burger'); await pg.wait_for_timeout(500)
                    if n=='index':
                        await pg.evaluate("document.querySelector('.shift').scrollIntoView()"); await pg.wait_for_timeout(300)
                        await pg.click('#gt-4'); await pg.wait_for_timeout(900)
                        ok=await pg.evaluate("(()=>{const p=document.getElementById('gp-4');const k=document.querySelector('.knob');return !p.hidden&&p.getBoundingClientRect().height>50&&document.getElementById('gp-1').hidden&&k.style.left===document.getElementById('gt-4').style.left&&document.getElementById('gt-4').getAttribute('aria-selected')==='true'})()")
                        if not ok: F(f'{tag} gear selector failed')
                        lg=await pg.evaluate("(()=>{const l=document.querySelector('.lights');return l?getComputedStyle(l).display:'none'})()")
                        if lg!='none': F(f'{tag} intro overlay still visible')
                        vis=await pg.evaluate("(()=>{const h=document.querySelector('.hero');return h.classList.contains('go')})()")
                        if not vis: F(f'{tag} hero never started')
                    if w==1440 and rm=='no-preference':
                        # duplicate photo check per page
                        hs=[]
                        for u in set(res['imgs']):
                            if u.endswith('.svg'): continue
                            data=await (await pg.request.get(u)).body()
                            hs.append((u.split('/')[-1],imagehash.phash(Image.open(io.BytesIO(data)))))
                        for i in range(len(hs)):
                            for j in range(i+1,len(hs)):
                                if hs[i][1]-hs[j][1]<12 and hs[i][0][:3]!=hs[j][0][:3]: F(f'{n} near-duplicate {hs[i][0]} {hs[j][0]} d={hs[i][1]-hs[j][1]}')
                        print(n,'ok imgs',len(hs),'|',res['titles'][0][:60],'| desc',len(res['titles'][1] or ''))
                await ctx.close()
        await b.close()
asyncio.run(main())
print('FAILS',len(fails))
