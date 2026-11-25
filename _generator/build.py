#!/usr/bin/env python3
"""Generator for the Turner's Automotive demo site (RGWebD). Writes ../site."""
import json, shutil, html, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from icons import I
from data import *
GEN=Path(__file__).parent; OUT=GEN.parent/'site'; BR=GEN.parent/'brand'
e=html.escape
# ---------- assets ----------
OUT.mkdir(parents=True,exist_ok=True)
for p in OUT.iterdir():
    if p.name in ('.git',): continue
    shutil.rmtree(p) if p.is_dir() else p.unlink()
A=OUT/'assets'; shutil.copytree(GEN/'assets'/'img',A/'img'); shutil.copytree(GEN/'assets'/'fonts',A/'fonts')
for f in ['ta-horizontal-dark.svg','ta-horizontal-light.svg','ta-stacked-dark.svg','ta-stacked-light.svg','ta-emblem.svg','ta-mono-white.svg','ta-mono-navy.svg','ta-favicon.svg']: shutil.copy(BR/f,A/f)
shutil.copy(BR/'png/favicon.ico',OUT/'favicon.ico'); shutil.copy(BR/'png/favicon-180.png',OUT/'apple-touch-icon.png')
for f in ['favicon-32.png','favicon-512.png']: shutil.copy(BR/'png'/f,A/f)
shutil.copy(GEN/'src/styles.css',A/'styles.css'); shutil.copy(GEN/'src/script.js',A/'script.js')
# OG image: navy plate + hero photo + logo
og=Image.new('RGB',(1200,630),(11,26,46))
ph=Image.open(A/'img/g01-1600.webp').convert('RGB'); ph=ph.resize((840,630)); ph=ph.crop((120,0,840,630))
m=Image.new('L',ph.size,255); ImageDraw.Draw(m).rectangle((0,0,160,630),fill=0); m=m.filter(ImageFilter.GaussianBlur(70))
og.paste(ph,(480,0),m)
d=ImageDraw.Draw(og); d.polygon([(1010,0),(1050,0),(990,630),(950,630)],fill=(227,38,46)); d.polygon([(1065,0),(1080,0),(1020,630),(1005,630)],fill=(227,38,46))
lg=Image.open(BR/'png/horizontal-dark-1400.png').convert('RGBA'); lg=lg.resize((600,round(lg.height*600/lg.width)))
og=og.convert('RGBA'); og.alpha_composite(lg,(54,190)); og=og.convert('RGB'); d=ImageDraw.Draw(og)
try:
    fnt=ImageFont.truetype('/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf',27); fnt.set_variation_by_axes([14,650])
    d.text((60,430),'Auto repair & transmissions · Keystone Heights, FL',font=fnt,fill=(235,240,246)); d.text((60,472),f'{PHONE} · Mon–Fri 8–5 · {RATING}★ from {COUNT} Google reviews',font=fnt,fill=(255,120,125))
except Exception as ex: print('og font',ex)
og.save(A/'og-image.jpg',quality=86)

def dims(name,w=1600): return Image.open(A/'img'/f'{name}-{w}.webp').size
def pic(name,alt=None,cls='',sizes='(max-width:980px) 100vw, 50vw',eager=False,attrs=''):
    alt=PH[name] if alt is None else alt; w,h=dims(name); w8,_=dims(name,800)
    lazy='fetchpriority="high" ' if eager else 'loading="lazy" '
    return (f'<img src="assets/img/{name}-1600.webp" srcset="assets/img/{name}-800.webp {w8}w, assets/img/{name}-1600.webp {w}w" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{e(alt)}" {lazy}decoding="async"{(" class=\""+cls+"\"") if cls else ""}{(" "+attrs) if attrs else ""}>')
def stars(n=5): return f'<span class="stars" aria-label="{n} out of 5 stars">'+I['star']*n+'</span>'
STAR5='<span class="row">'+'<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.3 1.3-6.6L2.5 9.4l6.6-.8z"/></svg>'*5+'</span>'
def pstars(): return f'<span class="pstars" role="img" aria-label="{RATING} out of 5 stars">{STAR5}<span class="top" style="width:{RATING/5*100:.0f}%">{STAR5}</span></span>'
def btn_call(cls='',label=None): return f'<a class="btn mag {cls}" href="{TEL}">{I["phone"]}<span class="lbl">{label or "Call "+PHONE}</span></a>'
def btn_est(cls='ghost'): return f'<a class="btn mag {cls}" href="contact.html#estimate">{I["msg"]}<span class="lbl">Get an estimate</span></a>'
def btn_dir(cls='ghost'): return f'<a class="btn mag {cls}" href="{DIR}" target="_blank" rel="noopener">{I["dir"]}<span class="lbl">Directions</span></a>'
STATUS='<span class="status" data-status><i></i><span>Mon–Fri 8 AM–5 PM</span></span>'
NAV=[('index.html','Home'),('services.html','Services'),('shop.html','The Shop'),('reviews.html','Reviews'),('contact.html','Contact')]
HOURS=[(1,'Monday','8 AM – 5 PM'),(2,'Tuesday','8 AM – 5 PM'),(3,'Wednesday','8 AM – 5 PM'),(4,'Thursday','8 AM – 5 PM'),(5,'Friday','8 AM – 5 PM'),(6,'Saturday','Closed'),(0,'Sunday','Closed')]
def hours_table(): return '<table class="hours"><caption class="sr">Hours (Eastern Time)</caption><tbody>'+''.join(f'<tr data-d="{n}"><th scope="row">{d_}</th><td>{h}</td></tr>' for n,d_,h in HOURS)+'</tbody></table><p class="note">Eastern Time. Google flags Thanksgiving (Nov 26) and the day after (Nov 27) as “hours might differ,” so call ahead on holidays.</p>'

def header(cur):
    nav=''.join(f'<a href="{f}"{" aria-current=\"page\"" if f==cur else ""}>{t}</a>' for f,t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a><div class="progress" aria-hidden="true"></div>
<header class="hdr"><div class="wrap"><a class="brand" href="index.html" aria-label="Turner’s Automotive home"><img src="assets/ta-horizontal-dark.svg" width="425" height="120" alt="Turner’s Automotive &amp; Transmission"></a>
<nav class="nav" aria-label="Main">{nav}</nav><div class="hdr-cta">{STATUS}<a class="btn sm mag" href="{TEL}">{I["phone"]}<span class="lbl">{PHONE}</span></a></div>
<button class="burger" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Open menu"><span></span><span></span><span></span></button></div></header>
<nav class="mnav" id="mnav" aria-label="Mobile" aria-hidden="true">{nav}<div class="ctas">{btn_call()}{btn_est()}</div><p style="margin-top:18px">{STATUS}</p></nav>'''
def footer():
    pages=''.join(f'<li><a href="{f}">{t}</a></li>' for f,t in NAV)
    sv=''.join(f'<li><a href="services.html#{s["id"]}">{s["t"]}</a></li>' for s in SERV[:6])
    return f'''<footer class="ftr"><div class="wrap"><div class="fgrid">
<div><img src="assets/ta-horizontal-dark.svg" width="300" height="85" alt="Turner’s Automotive" loading="lazy" style="width:300px;height:auto;margin-bottom:18px"><p>Auto repair and transmission work in Keystone Heights, Florida: diagnostics, brakes, A/C, electrical, maintenance and alignments for cars, trucks, vans and 4×4s.</p>
<address style="font-style:normal"><a href="{DIR}" target="_blank" rel="noopener">{ADDR}</a><br><a href="{TEL}">{PHONE}</a></address></div>
<div><h4>Pages</h4><ul>{pages}</ul></div><div><h4>Services</h4><ul>{sv}</ul></div><div><h4>Hours</h4><ul><li>Mon–Fri: 8 AM – 5 PM</li><li>Sat–Sun: Closed</li><li class="muted" style="font-size:.85rem">Eastern Time · holiday hours may vary</li></ul><h4 style="margin-top:22px">Find us</h4><ul><li><a href="{GLIST}" target="_blank" rel="noopener">Google Maps listing</a></li><li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li></ul></div>
</div><div class="bigword" aria-hidden="true">Turner’s</div><div class="legal"><span>© 2026 {LEGAL}. All rights reserved.</span><span>Design preview by RGWebD</span></div></div></footer>
<div class="mbar">{btn_call('', 'Call now')}{btn_est()}</div>
<div class="demo" role="note">Design preview by RGWebD<button type="button" aria-label="Dismiss preview note">×</button></div>'''
def lightbox(): return f'<div class="tlb" role="dialog" aria-modal="true" aria-label="Photo viewer" aria-hidden="true"><figure><img alt=""><p></p></figure><button class="x1" type="button" aria-label="Close">{I["x"]}</button><button class="pv" type="button" aria-label="Previous photo">{I["left"]}</button><button class="nx" type="button" aria-label="Next photo">{I["arrow"]}</button></div>'

# ---------- JSON-LD ----------
def biz(extra=None):
    b={"@context":"https://schema.org","@type":"AutoRepair","@id":BASE+"#business","name":NAME,"alternateName":["Turner’s Automotive & Transmission","Turner’s Auto LLC"],
       "description":"Auto repair and transmission shop in Keystone Heights, Florida: transmissions, differentials and gearboxes, diagnostics and check engine lights, brakes, shocks and struts, A/C and heating, radiators and cooling systems, fuel systems, electrical repair, oil changes, tune-ups and alignments.",
       "url":BASE,"telephone":"+1-352-473-3404","image":[BASE+"assets/img/g01-1600.webp",BASE+"assets/img/g17-1600.webp",BASE+"assets/og-image.jpg"],"logo":BASE+"assets/favicon-512.png",
       "address":{"@type":"PostalAddress","streetAddress":STREET,"addressLocality":CITY,"addressRegion":REGION,"postalCode":ZIP,"addressCountry":"US"},
       "geo":{"@type":"GeoCoordinates","latitude":LAT,"longitude":LNG},"hasMap":GPLACE,"sameAs":[GPLACE,FB],
       "areaServed":[{"@type":"City","name":"Keystone Heights, FL"},{"@type":"Place","name":"Northeast and Central Florida"}],
       "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"08:00","closes":"17:00"}],
       "paymentAccepted":"Credit cards, debit cards",
       "amenityFeature":[{"@type":"LocationFeatureSpecification","name":"Wheelchair accessible entrance","value":True},{"@type":"LocationFeatureSpecification","name":"Wheelchair accessible parking lot","value":True}],
       "knowsAbout":["Transmission repair","Differentials","Check engine light diagnosis","Brake repair","Auto A/C repair","Radiator and cooling system repair","Fuel injection","Automotive electrical repair","Oil change","Wheel alignment"],
       "aggregateRating":{"@type":"AggregateRating","ratingValue":RATING,"reviewCount":COUNT,"bestRating":5},
       "makesOffer":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s["t"],"url":BASE+"services.html#"+s["id"]}} for s in SERV]}
    if extra: b.update(extra)
    return b
def reviews_ld(): return {"review":[{"@type":"Review","author":{"@type":"Person","name":n},"reviewRating":{"@type":"Rating","ratingValue":5,"bestRating":5},"reviewBody":t,"publisher":{"@type":"Organization","name":"Google"}} for n,_,t in REV]}
def crumbs_ld(name,f): return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE},{"@type":"ListItem","position":2,"name":name,"item":BASE+f}]}
faq_ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
def crumbs(name): return f'<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <span aria-current="page">{name}</span></nav>'
def phero(img,kick,h1,lead,name,pos='50% 50%'):
    return f'''<section class="phero"><div class="bg" data-px="0.12">{pic(img,sizes="100vw",eager=True,attrs=f'style="object-position:{pos}"')}</div><div class="wrap">{crumbs(name)}<p class="kicker">{kick}</p><h1 class="split-h">{h1}</h1><p class="lead">{lead}</p><div class="ctas" style="margin-top:26px">{btn_call()}{btn_est()}</div></div></section>'''
def cta(img,h,sub,pos='50% 50%',word='Call the shop'):
    bg=f'<div class="bg" data-px="0.1">{pic(img,alt="",sizes="100vw",attrs=f"style=\"object-position:{pos}\"")}</div>' if img else f'<div class="gword" aria-hidden="true">{word}</div>'
    return f'''<section class="cta{"" if img else " graphic"}">{bg}<div class="lanes" aria-hidden="true"></div><div class="wrap"><p class="kicker">Mon–Fri · 8 AM to 5 PM</p><h2 class="split-h">{h}</h2><p class="lead">{sub}</p><a class="phone" href="{TEL}">{PHONE}</a><div class="ctas">{btn_call()}{btn_dir()}</div></div></section>'''
def odo(txt,lab,note=''):
    parts=''
    for ch in txt:
        if ch.isdigit(): parts+=f'<span class="dg" data-v="{ch}">{ch}</span>'
        elif ch=='.': parts+='<span class="sep" aria-hidden="true">.</span>'
        else: parts+=f'<span class="suf" aria-hidden="true">{ch}</span>'
    return f'<div class="odo"><div class="digits" aria-hidden="true">{parts}</div><span class="sr">{txt}</span><div class="lab">{lab}{f"<em>{note}</em>" if note else ""}</div></div>'
def page(fname,title,desc,body,ld):
    canon=BASE+('' if fname=='index.html' else fname)
    lds=''.join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>' for x in ld)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{canon}"><meta name="robots" content="index,follow">
<meta name="theme-color" content="#0B1A2E"><link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" href="assets/ta-favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="{SHORT}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{BASE}assets/og-image.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}assets/og-image.jpg">
<link rel="preload" href="assets/fonts/archivo-italic.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/styles.css"><script>document.documentElement.classList.add('js')</script>{lds}</head>
<body>{header(fname)}<main id="main">{body}</main>{footer()}{lightbox() if 'gal-item' in body else ''}<script src="assets/script.js" defer></script></body></html>'''

# ---------- HOME ----------
tick=''.join(f'<li>{s["t"]}</li>' for s in SERV)
GEARS=SERV[:6]+[dict(id="maintenance",t="Routine service & alignment",img="g06",g="R",ic="oil",
      s="Oil change, lube and tune-up, filters, fluids, belts, hoses and alignments.",
      li=["Oil change, lube and tune-up (from their site)","Filters, fluids, belts and hoses (from their site)","Wheel alignments on the drive-on rack (from their site)"])]
POS={'1':(14,12),'2':(14,88),'3':(38,12),'4':(38,88),'5':(62,12),'6':(62,88),'R':(86,12)}
slots='<line class="slot" x1="14" y1="12" x2="14" y2="88"/><line class="slot" x1="38" y1="12" x2="38" y2="88"/><line class="slot" x1="62" y1="12" x2="62" y2="88"/><line class="slot" x1="86" y1="12" x2="86" y2="50"/><line class="slot" x1="14" y1="50" x2="86" y2="50"/>'
slots2=slots.replace('class="slot"','class="slot2"')
tabs=''.join(f'<button type="button" role="tab" id="gt-{g["g"]}" aria-controls="gp-{g["g"]}" aria-selected="false" tabindex="-1" data-name="{e(g["t"])}" style="left:{POS[g["g"]][0]}%;top:{POS[g["g"]][1]}%" aria-label="Gear {g["g"]}: {e(g["t"])}">{g["g"]}</button>' for g in GEARS)
ck=I['check']
panels=''.join(f'''<div class="gpanel" role="tabpanel" id="gp-{g["g"]}" aria-labelledby="gt-{g["g"]}"{"" if k==0 else " hidden"}><div class="gph">{pic(g["img"],sizes="(max-width:980px) 92vw, 460px")}<span class="gnum" aria-hidden="true">{g["g"]}</span></div>
<div class="gtx"><p class="label red">Gear {g["g"]}</p><h3>{g["t"]}</h3><p class="muted">{g["s"]}</p><ul>{"".join(f"<li>{ck}<span>{x}</span></li>" for x in g["li"])}</ul><a class="more" href="services.html#{g["id"]}">Full details {I["arrow"]}</a></div></div>''' for k,g in enumerate(GEARS))
HR=[(REV[3][0],"I have never met or dealt with ANY automotive repair shop that was as fair and honest as these people. If they tell you something is wrong.... it is."),
    (REV[2][0],REV[2][2]),
    (REV[0][0],"I experienced the problem being diagnosed in less than 15 minutes, parts ordered, replaced, and out the door all in a few hours."),
    (REV[5][0],"They kept us informed on what the problem was and what they were doing. They didn't pressure us into any extra work, even if they recommend something. And their prices are very fair."),
    (REV[9][0],"We were camping at the state park when the check engine light came on. They found the problem, got the part on time did the work at a good price; plus they helped getting me to and from my camp site.")]
def carousel(items):
    sl=''.join(f'<div class="slide" role="group" aria-roledescription="slide" aria-label="{k+1} of {len(items)}">{stars()}<span class="qm" aria-hidden="true">“</span><blockquote>{e(t)}</blockquote><p class="who"><span>{e(n)}</span> · Google review</p></div>' for k,(n,t) in enumerate(items))
    return f'<div class="car" aria-roledescription="carousel" aria-label="Customer reviews"><div class="car-view"><div class="car-track">{sl}</div></div><button class="pv" type="button" aria-label="Previous review">{I["left"]}</button><button class="nx" type="button" aria-label="Next review">{I["arrow"]}</button><div class="dots"></div></div>'
pods=''.join('<div class="pod"><i></i><i></i><i></i></div>' for _ in range(5))
home=f'''<div class="lights" aria-hidden="true"><div class="rig">{pods}</div><p>Lights out</p></div>
<section class="hero" aria-labelledby="h1"><div class="bgword" aria-hidden="true">TRANSMISSION</div>
<div class="wrap"><div class="hero-top"><div><p class="kicker fade">Auto repair &amp; transmissions · Keystone Heights, FL</p>
<h1 id="h1"><span class="l"><span>Honest repairs.</span></span><span class="l"><span class="speed">Straight</span></span><span class="l"><span class="red">answers.</span></span></h1></div>
<div class="hero-side"><p class="lead fade d1">Transmissions, check engine lights, brakes, A/C, electrical and everyday maintenance for cars, trucks, vans and 4×4s. Open Monday to Friday, 8 to 5.</p>
<div class="ctas fade d2">{btn_call()}{btn_est()}</div>
<div class="trust fade d3"><a class="chip" href="{GLIST}" target="_blank" rel="noopener">{pstars()} {RATING} from {COUNT} Google reviews</a>{STATUS}</div></div></div>
<div class="wind"><div class="ph">{pic("g01",sizes="(max-width:640px) 100vw, 1240px",eager=True)}</div><span class="stripe" aria-hidden="true"></span>
<div class="hs" style="--x:12%;--y:41%;--ym:45%"><a href="services.html#transmissions"><span class="dot"></span><span class="hl">Transmission shop</span></a></div>
<div class="hs" style="--x:43%;--y:35%;--ym:40%"><a href="services.html#alignment"><span class="dot"></span><span class="hl">Wheel alignment</span></a></div>
<div class="hs rev" style="--x:63%;--y:62%;--ym:58%"><a href="services.html#models"><span class="dot"></span><span class="hl">Trucks &amp; 4×4s</span></a></div>
<a class="rate-card" href="reviews.html"><span class="big">{RATING}</span><span>{pstars()}<small>{COUNT} Google reviews</small></span></a></div></div></section>
<div class="ticker" aria-hidden="true"><ul>{tick}{tick}</ul></div>
<section class="sec"><div class="wrap"><div class="head"><div><p class="kicker">What we fix</p><h2 class="split-h">Pick a <span class="red">gear.</span></h2></div><p>Every service here comes from the shop’s own site, its Google profile and what customers describe in their reviews. Tap a gear to shift.</p></div>
<div class="shift"><div class="gatebox"><span class="label">Shift through the shop</span><div class="gate" role="tablist" aria-label="Services"><svg class="slots" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">{slots}{slots2}</svg><span class="knob" aria-hidden="true"></span>{tabs}</div><p class="cur" aria-live="polite"></p></div>
<div class="gpanels">{panels}</div></div></div></section>
<section class="sec dark slant-top"><div class="wrap why"><div class="why-img" data-r="left">{pic("g17",attrs='data-px="0.06"')}<span class="tagline">Commercial Circle · Keystone Heights</span></div>
<div data-r><p class="kicker">Why Keystone Heights calls</p><h2 class="split-h">The shop that <span class="red">tells it straight.</span></h2>
<p class="lead">Their site traces the shop’s roots to a family garage in Beaumont, Texas in 1966, and says the team brings over 40 years of auto repair experience, with more than a decade at this location. <span class="src">From their site</span></p>
<div class="pts"><div class="pt"><span class="n">{I["shield"]}</span><div><h3>Honest diagnosis</h3><p>Customers came in expecting big bills and were told they only needed a caliper, or a loose plug wire.</p></div></div>
<div class="pt"><span class="n">{I["chat"]}</span><div><h3>A call before any extra work</h3><p>Reviewers say the quote doesn’t change unless something unforeseen comes up, and you get a call first.</p></div></div>
<div class="pt"><span class="n">{I["clock"]}</span><div><h3>Quick turnaround</h3><p>“Diagnosed in less than 15 minutes … out the door all in a few hours,” one customer writes.</p></div></div>
<div class="pt"><span class="n">{I["key"]}</span><div><h3>Night drop</h3><p>Reviewers describe an after-hours key drop: an envelope with your details, the key inside, into the slot.</p></div></div></div></div></div></section>
<section class="sec dark" style="padding-top:0"><div class="wrap"><div class="odos stagger">{odo("4.7","Google rating","out of 5 stars")}{odo(str(COUNT),"Google reviews","as of Nov 2026")}{odo("40+","Years in auto repair","from their site")}</div>
<div class="head center"><div><p class="kicker">Straight from Google</p><h2 class="split-h">You will NOT get <span class="red">ripped off.</span></h2></div></div>
{carousel(HR)}<p style="text-align:center;margin-top:40px"><a class="btn ghost mag" href="reviews.html"><span class="lbl">Read the reviews</span>{I["arrow"]}</a></p></div></section>
<section class="sec paper2"><div class="wrap"><div class="head"><div><p class="kicker">Take a look</p><h2 class="split-h">Around the <span class="red">shop.</span></h2></div></div>
<div class="teasers stagger"><a class="pcard" href="shop.html">{pic("g24",sizes="(max-width:980px) 100vw, 33vw")}<span class="go">{I["arrow"]}</span><span class="tx"><span class="label">The Shop</span><h3>RVs to Corvettes</h3><p>The story, the bays and a photo gallery</p></span></a>
<a class="pcard" href="reviews.html">{pic("g19",sizes="(max-width:980px) 100vw, 33vw")}<span class="go">{I["arrow"]}</span><span class="tx"><span class="label">Reviews</span><h3>{RATING}★ on Google</h3><p>{COUNT} reviews, ten quoted word for word</p></span></a>
<a class="pcard" href="contact.html">{pic("g16",sizes="(max-width:980px) 100vw, 33vw")}<span class="go">{I["arrow"]}</span><span class="tx"><span class="label">Contact</span><h3>Get an estimate</h3><p>{ADDR}</p></span></a></div></div></section>
{cta("g25","Check engine light <span class='red'>on?</span>","Call the shop, describe what it’s doing, and get it on the schedule.",pos='50% 60%')}'''

# ---------- SERVICES ----------
svc=''.join(f'''<article class="svc" id="{s["id"]}"><div class="svc-img" data-r>{pic(s["img"])}<span class="gnum">Gear <b>{s["g"]}</b></span></div>
<div data-r><span class="ic">{I[s["ic"]]}</span><h2 class="split-h">{s["t"]}</h2><p class="lead">{s["s"]}</p><p>{s["d"]}</p><ul>{"".join(f"<li>{ck}<span>{x}</span></li>" for x in s["li"])}</ul><div class="ctas">{btn_call("sm")}</div></div></article>''' for s in SERV)
STEPS=[("01","Call or drop it off",f"Call {PHONE} during business hours. Reviewers describe a night drop slot for after-hours drop-offs: your details and the key in an envelope."),
       ("02","Diagnosis","The problem gets tracked down first. Problem diagnosis is the topic customers mention most in their Google reviews."),
       ("03","A quote and a phone call","Reviewers say you get a quote and a call with the update, and the price doesn’t change unless something unforeseen comes up."),
       ("04","The repair","Parts ordered and the work done. One customer was “out the door all in a few hours.”"),
       ("05","Back on the road","You get a call when it’s ready. Pay by credit or debit card, as listed on Google.")]
road=f'''<div class="road" data-r><svg class="line" aria-hidden="true"><line class="asph" x1="20" y1="18" x2="20" y2="100"/><line class="dash" x1="20" y1="18" x2="20" y2="100"/><line class="drawn" x1="20" y1="18" x2="20" y2="18"/></svg><span class="rcar" aria-hidden="true">{I["wheel"]}</span>{"".join(f'<div class="step"><span class="k">Step {k}</span><h3>{t}</h3><p>{p}</p></div>' for k,t,p in STEPS)}</div>'''
models=''.join(f'<span><b>{m}</b></span>' for m in MODELS)
services=f'''{phero("g04","Services","Every gear, <span class='red'>covered.</span>","From transmissions and differentials to oil changes and alignments, the services their site lists and that customers describe in their reviews.","Services",pos='50% 55%')}
<section class="sec tight" id="models"><div class="wrap"><div class="head"><div><p class="kicker">What we work on</p><h2 class="split-h">Cars, trucks, <span class="red">vans &amp; 4×4s.</span></h2></div><p>Models serviced, as listed on their site. The shop’s photos also show motorhomes, lifted trucks and classic sports cars.</p></div><div class="models stagger">{models}</div><p style="margin-top:16px"><span class="src">From their site</span></p></div></section>
<section class="sec" style="padding-top:0"><div class="wrap">{svc}</div></section>
<section class="sec dark"><div class="wrap"><div class="head center"><div><p class="kicker">How it works</p><h2 class="split-h">From drop-off to <span class="red">drive-off.</span></h2></div></div>{road}</div></section>
{cta("g22","Not sure what it <span class='red'>needs?</span>","Describe the noise, the light or the leak. The shop will tell you what it actually needs.",pos='50% 45%')}'''

# ---------- THE SHOP ----------
TL=[("1966","Beaumont, Texas","Their site says the story began at a family repair shop in Beaumont, where a three-year-old could often be found at his father’s side."),
    ("At 18","Transmission rebuilding","By eighteen, transmission rebuilding had joined years of hands-on engine work."),
    ("At 22","A shop of his own","A transmission and full-service auto repair shop opened."),
    ("1993","Moving to Florida","The move to Florida began a new chapter."),
    ("Today","Keystone Heights","Over 40 years of auto repair experience, with more than a decade on Commercial Circle.")]
tlr=f'''<div class="road light-road" data-r><svg class="line" aria-hidden="true"><line class="asph" x1="20" y1="18" x2="20" y2="100"/><line class="dash" x1="20" y1="18" x2="20" y2="100"/><line class="drawn" x1="20" y1="18" x2="20" y2="18"/></svg><span class="rcar" aria-hidden="true">{I["wrench"]}</span>{"".join(f'<div class="step"><span class="k">{k}</span><h3>{t}</h3><p>{p}</p></div>' for k,t,p in TL)}</div>'''
AM=[("wc","Wheelchair accessible","Accessible entrance and parking lot, per the Google profile."),("card","Cards accepted","Credit and debit cards, per the Google profile."),("key","Night drop","Reviewers describe an after-hours key drop slot. Call to confirm."),
    ("wrench","Onsite services","Listed under service options on Google."),("heart","Welcoming to all","LGBTQ+ friendly and a transgender safe space, per the Google profile."),("pin","Commercial Circle",f"{ADDR}. Reviewers mention grabbing lunch nearby while they wait.")]
amen=''.join(f'<div class="am"><span class="ic">{I[i]}</span><div><h3>{t}</h3><p>{p}</p></div></div>' for i,t,p in AM)
GAL=['g01','g15','g09','g06','g24','g08','g19','g07','g10','g20','g22','g05','g23','g12','g16','g14','g25','g21','g04','g11']
gal=''.join(f'<button class="gal-item" type="button" data-full="assets/img/{g}-1600.webp">{pic(g,sizes="(max-width:640px) 70vw, 400px")}<span class="cap" aria-hidden="true">{e(PH[g])}</span></button>' for g in GAL)
shop=f'''{phero("g17","The Shop","Built on <span class='red'>honest work.</span>","A family story that started in a Texas repair shop and runs through the bays on Commercial Circle in Keystone Heights.","The Shop",pos='50% 60%')}
<section class="sec"><div class="wrap" style="display:grid;grid-template-columns:1fr;gap:clamp(36px,5vw,60px)"><div class="head"><div><p class="kicker">Our story</p><h2 class="split-h">From Beaumont <span class="red">to Keystone.</span></h2></div><p>The milestones below are summarized from the About section of the shop’s own website. <span class="src">From their site</span></p></div>
{tlr}
<figure class="quote" data-r style="margin:0"><p class="big">“If we can’t fix it, it’s not broken.”</p><blockquote>“When you contact us, I or a member of our experienced team will provide you with updates on your vehicle. With over 40 years of dedication to automotive repair, including more than a decade at this location, our reputation speaks for itself.”</blockquote><figcaption class="label" style="color:var(--steel)">The shop’s general manager · <span class="src">From their site</span></figcaption></figure></div></section>
<section class="sec paper2"><div class="wrap"><div class="head"><div><p class="kicker">Good to know</p><h2 class="split-h">Before you <span class="red">pull in.</span></h2></div></div><div class="amen stagger">{amen}</div></div></section>
<section class="sec" style="padding-bottom:clamp(50px,6vw,80px)"><div class="wrap"><div class="head"><div><p class="kicker">Gallery</p><h2 class="split-h">In the <span class="red">bays.</span></h2></div><p class="gal-hint">Drag or swipe the strip. Tap a photo to enlarge it.</p></div></div><div class="gal-track" tabindex="0" aria-label="Shop photo gallery">{gal}</div></section>
{cta(None,"Bring it to <span class='red'>Turner’s.</span>","Monday to Friday, 8 AM to 5 PM on Commercial Circle in Keystone Heights.",word="Turner’s Automotive")}'''

# ---------- REVIEWS ----------
rv=''.join(f'<figure class="rv" data-r>{stars()}<blockquote>{e(t)}</blockquote><figcaption class="who">{e(n)}<small>{e(m)} · Google</small></figcaption></figure>' for n,m,t in REV)
reviews=f'''{phero("g23","Reviews",f"{RATING} stars. <span class='red'>{COUNT} reviews.</span>","What Keystone Heights drivers say on Google, quoted word for word.","Reviews",pos='50% 50%')}
<section class="sec"><div class="wrap"><div class="rsum light" data-r><div><div class="score">{RATING}</div>{pstars()}<p class="muted" style="margin:10px 0 0">{COUNT} Google reviews</p></div>
<div><p class="kicker">What customers mention most</p><div class="topics"><span>Courteous staff <b>14</b></span><span>Problem diagnosis <b>13</b></span><span>Transmission repair <b>5</b></span><span>Check engine light repair <b>2</b></span></div><p class="muted" style="margin:16px 0 0;font-size:.92rem">Review topics and counts as shown on the Google profile, Nov 2026.</p><p style="margin:18px 0 0"><a class="btn sm mag" href="{GLIST}" target="_blank" rel="noopener"><span class="lbl">See all on Google</span>{I["arrow"]}</a></p></div></div>
<div class="head" style="margin-top:clamp(50px,6vw,80px)"><div><p class="kicker">Word for word</p><h2 class="split-h">In their <span class="red">own words.</span></h2></div><p>Ten five-star Google reviews, copied exactly as written, including the spelling.</p></div><div class="rgrid">{rv}</div></div></section>
{cta("g14","Your turn to <span class='red'>find out.</span>","Call the shop and see why customers keep coming back.",pos='50% 40%')}'''

# ---------- CONTACT ----------
opts=''.join(f'<option>{s["t"]}</option>' for s in SERV)+'<option>Not sure / something else</option>'
contact=f'''{phero("g10","Contact","Let’s get you <span class='red'>rolling.</span>",f"Call {PHONE}, drop by {STREET} or send the shop the details. Monday to Friday, 8 to 5.","Contact",pos='50% 50%')}
<section class="sec"><div class="wrap cgrid"><div class="panel navy dark" data-r><p class="kicker">The shop</p>
<div class="facts"><div class="fact"><span class="ic">{I["phone"]}</span><div><b>Call</b><a class="bigtel" href="{TEL}">{PHONE}</a></div></div>
<div class="fact"><span class="ic">{I["pin"]}</span><div><b>Visit</b><a href="{DIR}" target="_blank" rel="noopener">{STREET}<br>{CITY}, {REGION} {ZIP}</a></div></div>
<div class="fact"><span class="ic">{I["clock"]}</span><div><b>Right now</b>{STATUS}</div></div></div>
{hours_table()}<div class="ctas" style="margin-top:20px">{btn_call()}{btn_dir()}</div></div>
<div class="panel" id="estimate" data-r><p class="kicker">Estimate request</p><h2 style="font-size:clamp(1.7rem,3vw,2.4rem)">Tell us what it’s <span class="red">doing.</span></h2>
<form class="est" id="estimate-form" data-sms="{SMS}"><div class="row"><div class="f"><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></div><div class="f"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div></div>
<div class="row"><div class="f"><label for="f-veh">Year, make &amp; model</label><input id="f-veh" name="vehicle" placeholder="e.g. 2016 Ford F-150"></div><div class="f"><label for="f-svc">Service</label><select id="f-svc" name="service">{opts}</select></div></div>
<div class="f"><label for="f-det">What’s going on?</label><textarea id="f-det" name="details" placeholder="Noises, warning lights, when it started…"></textarea></div>
<div class="ctas"><button class="btn mag" type="submit">{I["chat"]}<span class="lbl">Text it to the shop</span></button>{btn_call("ghost","Or call")}</div>
<p class="fine">This opens a pre-filled text message to {PHONE} on your phone. Nothing is sent until you press send. Prefer to talk? Calling during business hours is quickest.</p></form></div></div>
<div class="wrap"><div class="map" data-r><iframe title="Map to Turner’s Automotive, {ADDR}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=TURNER%E2%80%99S+AUTOMOTIVE,+135+Commercial+Cir,+Keystone+Heights,+FL+32656&output=embed"></iframe></div></div></section>
<section class="sec paper2"><div class="wrap"><div class="head center"><div><p class="kicker">FAQ</p><h2 class="split-h">Good <span class="red">questions.</span></h2></div></div><div class="faq">{"".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q,a in FAQ)}</div></div></section>'''

PAGES=[
 ('index.html',"Turner’s Automotive | Auto Repair & Transmissions in Keystone Heights, FL",f"Auto repair and transmission shop in Keystone Heights, FL: diagnostics, check engine lights, brakes, A/C, electrical, oil changes and alignments. {RATING}★ from {COUNT} Google reviews. Mon–Fri 8–5. Call {PHONE}.",home,[biz()]),
 ('services.html',"Services | Transmissions, Diagnostics, Brakes, A/C & Alignments | Turner’s Automotive","Transmissions and differentials, check engine light diagnosis, brakes, shocks and struts, A/C and cooling, fuel systems, electrical, oil changes, tune-ups and alignments in Keystone Heights, FL.",services,[biz(),crumbs_ld('Services','services.html')]),
 ('shop.html',"The Shop | Our Story & Gallery | Turner’s Automotive, Keystone Heights",f"The story behind Turner’s Automotive & Transmission in Keystone Heights, FL, what to know before you visit, and a gallery of work in the bays.",shop,[biz(),crumbs_ld('The Shop','shop.html')]),
 ('reviews.html',f"Reviews | {RATING} Stars from {COUNT} Google Reviews | Turner’s Automotive",f"Read what customers say about Turner’s Automotive in Keystone Heights, FL: {RATING} stars from {COUNT} Google reviews, ten quoted word for word.",reviews,[biz(reviews_ld()),crumbs_ld('Reviews','reviews.html')]),
 ('contact.html',"Contact & Hours | Turner’s Automotive, 135 Commercial Cir, Keystone Heights, FL",f"Turner’s Automotive: {ADDR}. Call {PHONE}. Open Monday–Friday 8 AM–5 PM. Map, hours, estimate form and FAQ.",contact,[biz(),crumbs_ld('Contact','contact.html'),faq_ld]),
]
for f,t,dsc,b,ld in PAGES: (OUT/f).write_text(page(f,t,dsc,b,ld))
nf=f'''<section class="phero" style="min-height:80vh"><div class="wrap"><p class="kicker">Error 404</p><h1>Wrong <span class="red">turn.</span></h1><p class="lead">That page isn’t here. Head back home or give the shop a call.</p><div class="ctas" style="margin-top:24px"><a class="btn mag" href="index.html"><span class="lbl">Back home</span></a>{btn_call('ghost')}</div></div></section>'''
P=f'/{REPO}/'
h404=page('404.html','Page not found | Turner’s Automotive','This page could not be found.',nf,[biz()])
for a in ['href="index.html','href="services.html','href="shop.html','href="reviews.html','href="contact.html','src="assets/','href="assets/','href="favicon.ico"','href="apple-touch-icon.png"']:
    h404=h404.replace(a,a.replace('="','="'+P,1))
h404=h404.replace('content="index,follow"','content="noindex"').replace(f'<link rel="canonical" href="{BASE}404.html">','')
(OUT/'404.html').write_text(h404)
(OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{BASE}{"" if f=="index.html" else f}</loc><lastmod>2026-11-25</lastmod></url>\n' for f,*_ in PAGES)+'</urlset>\n')
llms=f'''# {NAME}

> Auto repair and transmission shop at {ADDR}. Phone {PHONE}. Open Monday–Friday 8 AM–5 PM Eastern Time, closed Saturday and Sunday (Google flags Thanksgiving and the day after as "hours might differ"). Rated {RATING} stars from {COUNT} Google reviews. Legal name on its Google photos: {LEGAL}. Also known as "Turner’s Automotive & Transmission".

## Key facts
- Category: Car repair and maintenance service (AutoRepair)
- Services (from the shop's own site, keystone-auto-repair.com, April 2026 archive): transmissions; differentials and gearboxes; radiator and coolant system repair; A/C and heating repair; brakes, shocks and struts; carburetor, fuel injection and fuel pump repair; check engine / service engine soon lights; electrical repair (battery, starter, alternator, generator); filters, fluids, belts and hoses; oil change, lube and tune-up; alignments
- Vehicles: domestic and import cars and trucks, vans, 4×4s and special interest vehicles
- Service area (from their site): Keystone Heights and Northeast & Central Florida
- Google attributes: wheelchair accessible entrance and parking; onsite services; oil change; credit and debit cards; LGBTQ+ friendly
- Reviewers describe a night drop slot for after-hours drop-offs (unconfirmed by the shop)
- No email, prices, warranties or certifications are published
- Google Maps: {GPLACE}
- Facebook: {FB}

## Pages
- [Home]({BASE}): overview, interactive service selector, why customers choose the shop, reviews
- [Services]({BASE}services.html): every service in detail and how a repair works
- [The Shop]({BASE}shop.html): the shop's story (from its own site), visitor info and a photo gallery
- [Reviews]({BASE}reviews.html): {RATING}★ from {COUNT} Google reviews, ten quoted verbatim
- [Contact]({BASE}contact.html): map, hours, phone, estimate form and FAQ
'''
(OUT/'llms.txt').write_text(llms)
(OUT/'.nojekyll').write_text('')
(OUT/'README.md').write_text(f'# {NAME} — website design preview\n\nStatic site generated by `_generator/build.py` (RGWebD). Live: {BASE}\n')
g=OUT/'_generator'; g.mkdir(exist_ok=True)
for f in ['build.py','data.py','icons.py']: shutil.copy(GEN/f,g/f)
if (GEN/'qa.py').exists(): shutil.copy(GEN/'qa.py',g/'qa.py')
shutil.copytree(GEN/'src',g/'src')
print('built',[p[0] for p in PAGES])
