(()=>{
const d=document,root=d.documentElement;
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
const FINE=matchMedia('(hover:hover) and (pointer:fine)').matches;
const $=(s,c=d)=>c.querySelector(s),$$=(s,c=d)=>[...c.querySelectorAll(s)];

/* live open/closed: America/New_York, Mon-Fri 8 AM-5 PM. Google flags these dates "hours might differ" (listed open 8-5). */
const HOLI={'2026-11-26':'Thanksgiving','2026-11-27':'Day after Thanksgiving'};
const FLAGGED={'2026-11-26':1,'2026-11-27':1};
function etNow(t=new Date()){const p=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit',weekday:'short',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(t);const o={};p.forEach(x=>o[x.type]=x.value);
 return{day:['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(o.weekday),min:(+o.hour%24)*60+(+o.minute),date:`${o.year}-${o.month}-${o.day}`}}
function nextOpen(day){if(day===5)return'Monday';if(day===6)return'Monday';return'tomorrow'}
function status(){const n=etNow();const wk=n.day>=1&&n.day<=5;const inH=n.min>=480&&n.min<1020;let st,t;
 if(wk&&FLAGGED[n.date]){st='unk';t=(inH?'Listed open · ':'')+HOLI[n.date]+': hours might differ, call first'}
 else if(wk&&inH){st='open';t='Open now · until 5 PM'}
 else if(wk&&n.min<480){st='closed';t='Closed · opens 8 AM today'}
 else{st='closed';t='Closed · opens 8 AM '+(n.day===0?'Monday':nextOpen(n.day))}
 $$('[data-status]').forEach(el=>{['open','closed','unk'].forEach(c=>el.classList.toggle(c,c===st));const s=$('span',el);if(s)s.textContent=t});
 $$('.hours tr').forEach(tr=>tr.classList.toggle('today',+tr.dataset.d===n.day))}
status();setInterval(status,60000);

/* header, progress stripe, mobile bar */
const hdr=$('.hdr'),prog=$('.progress'),mbar=$('.mbar');
function onScroll(){const y=scrollY,h=root.scrollHeight-innerHeight;hdr&&hdr.classList.toggle('scrolled',y>30);if(prog)prog.style.transform=`scaleX(${h>0?y/h:0})`;if(mbar)mbar.classList.toggle('show',y>260)}
addEventListener('scroll',onScroll,{passive:true});onScroll();

/* mobile nav */
const bg=$('.burger'),mn=$('.mnav');
if(bg&&mn){const set=o=>{bg.setAttribute('aria-expanded',o);bg.setAttribute('aria-label',o?'Close menu':'Open menu');mn.classList.toggle('open',o);mn.setAttribute('aria-hidden',!o);mn.inert=!o;d.body.style.overflow=o?'hidden':''};
 mn.inert=true;
 bg.addEventListener('click',()=>set(bg.getAttribute('aria-expanded')!=='true'));
 $$('a',mn).forEach(a=>a.addEventListener('click',()=>set(false)));
 addEventListener('keydown',e=>{if(e.key==='Escape'&&mn.classList.contains('open')){set(false);bg.focus()}})}

/* split headings into characters */
$$('.split-h').forEach(h=>{if(RM)return;const walk=n=>{[...n.childNodes].forEach(c=>{if(c.nodeType===3){const f=d.createDocumentFragment();c.textContent.split(/(\s+)/).forEach(w=>{if(!w)return;if(/^\s+$/.test(w)){f.appendChild(d.createTextNode(w));return}const ws=d.createElement('span');ws.style.whiteSpace='nowrap';ws.style.display='inline-block';[...w].forEach(ch=>{const s=d.createElement('span');s.className='ch1';s.textContent=ch;ws.appendChild(s)});f.appendChild(ws)});c.replaceWith(f)}else if(c.nodeType===1)walk(c)})};
 h.setAttribute('aria-label',h.textContent.replace(/\s+/g,' ').trim());walk(h);[...h.children].forEach(s=>s.setAttribute('aria-hidden','true'));$$('.ch1',h).forEach((c,i)=>c.style.transitionDelay=(i*18)+'ms')});

/* reveals */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12,rootMargin:'0px 0px -5% 0px'});
$$('[data-r],.stagger,.split-h').forEach(el=>{if(RM)el.classList.add('in');else io.observe(el)});
$$('.stagger').forEach(g=>[...g.children].forEach((c,i)=>c.style.transitionDelay=(i*80)+'ms'));

/* start-lights intro (home only, once per session) */
const hero=$('.hero'),lights=$('.lights');
function goHero(){hero&&hero.classList.add('go')}
if(lights){let seen=false;try{seen=sessionStorage.getItem('ta-lights')==='1';sessionStorage.setItem('ta-lights','1')}catch(e){}
 if(RM||seen){lights.classList.add('gone');goHero()}
 else{const pods=$$('.pod',lights);pods.forEach((p,i)=>setTimeout(()=>p.classList.add('on'),120+i*190));
  const T=120+pods.length*190+260;
  const finish=()=>{lights.classList.add('out');setTimeout(()=>{lights.classList.add('done');goHero()},140);setTimeout(()=>lights.classList.add('gone'),900)};
  const tm=setTimeout(finish,T);lights.addEventListener('click',()=>{clearTimeout(tm);finish()},{once:true})}}
else goHero();

/* hotspot labels: flip to open leftward (or back) so they always stay inside the viewport */
function fitHs(){const vw=root.clientWidth;$$('.hs').forEach(h=>{const l=$('.hl',h);if(!l)return;const d=$('.dot',h).getBoundingClientRect();const w=l.offsetWidth+14;
 if(d.right+w>vw-8&&d.left-w>=8)h.classList.add('rev');else if(d.left-w<8)h.classList.remove('rev')})}
fitHs();addEventListener('resize',fitHs);addEventListener('load',fitHs);

/* parallax */
const px=$$('[data-px]');
if(!RM&&px.length){const tick=()=>{px.forEach(el=>{const r=el.parentElement.getBoundingClientRect();if(r.bottom<-100||r.top>innerHeight+100)return;const f=+el.dataset.px;const c=r.top+r.height/2-innerHeight/2;el.style.transform=`translate3d(0,${(c*-f).toFixed(1)}px,0)`})};
 addEventListener('scroll',()=>requestAnimationFrame(tick),{passive:true});addEventListener('resize',tick);tick()}

/* odometers: each digit column rolls to its final digit (final text is in the markup for no-JS / reduced motion) */
function roll(o){$$('.dg',o).forEach((g,k)=>{const v=+g.dataset.v;const sp=$('span',g);const turns=RM?0:(1+k);sp.style.transform=`translateY(${-(turns*10+v)}em)`})}
$$('.odo').forEach(o=>{$$('.dg',o).forEach((g,k)=>{const v=+g.dataset.v;const turns=RM?0:(1+k);let h='';for(let t=0;t<=turns;t++)for(let i=0;i<10;i++){if(t===turns&&i>v)break;h+=`<b>${i}</b>`}g.innerHTML=`<span>${h}</span>`;g.setAttribute('aria-hidden','true')})});
const oio=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){roll(e.target);oio.unobserve(e.target)}}),{threshold:.4});
$$('.odo').forEach(o=>RM?roll(o):oio.observe(o));

/* tilt cards + magnetic buttons */
if(FINE&&!RM)$$('.pcard').forEach(c=>{c.addEventListener('pointermove',e=>{const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.setProperty('--ry',(x*8).toFixed(2)+'deg');c.style.setProperty('--rx',(-y*8).toFixed(2)+'deg')});c.addEventListener('pointerleave',()=>{c.style.setProperty('--ry','0deg');c.style.setProperty('--rx','0deg')})});
if(FINE&&!RM)$$('.btn.mag').forEach(b=>{b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect(),x=e.clientX-r.left-r.width/2,y=e.clientY-r.top-r.height/2;b.style.transform=`translate(${(x*.18).toFixed(1)}px,${(y*.28).toFixed(1)}px)`});b.addEventListener('pointerleave',()=>b.style.transform='')});

/* gear selector (tabs on an H-pattern shift gate) */
$$('.shift').forEach(s=>{const tabs=$$('[role=tab]',s),knob=$('.knob',s),cur=$('.cur',s);
 function sel(t,focus,anim){tabs.forEach(x=>{const on=x===t;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1;const p=d.getElementById(x.getAttribute('aria-controls'));if(p){p.hidden=!on;if(on&&anim&&!RM){p.classList.remove('anim');void p.offsetWidth;p.classList.add('anim')}}});
  knob.style.left=t.style.left;knob.style.top=t.style.top;if(cur)cur.textContent=t.dataset.name;if(focus)t.focus()}
 tabs.forEach((t,i)=>{t.addEventListener('click',()=>sel(t,false,true));t.addEventListener('keydown',e=>{let j=null;if(e.key==='ArrowRight'||e.key==='ArrowDown')j=i+1;if(e.key==='ArrowLeft'||e.key==='ArrowUp')j=i-1;if(e.key==='Home')j=0;if(e.key==='End')j=tabs.length-1;if(j!==null){e.preventDefault();sel(tabs[(j+tabs.length)%tabs.length],true,true)}})});
 sel(tabs[0],false,false)});

/* road timeline: lane line draws and the car drives down as you scroll */
$$('.road').forEach(tl=>{const svg=$('svg.line',tl),p=$('.drawn',tl),car=$('.rcar',tl),steps=$$('.step',tl);
 function upd(){const r=tl.getBoundingClientRect(),H=r.height;svg.setAttribute('viewBox',`0 0 40 ${H}`);$$('line',svg).forEach(l=>{if(l!==p)l.setAttribute('y2',H-18)});
  const k=RM?1:Math.min(1,Math.max(0,(innerHeight*.62-r.top)/H));p.setAttribute('y2',Math.max(18,(H-18)*k));if(car)car.style.top=Math.max(0,(H-36)*k)+'px';
  steps.forEach(s=>{const sr=s.getBoundingClientRect();if(RM||sr.top+20<innerHeight*.62)s.classList.add('lit')})}
 addEventListener('scroll',()=>requestAnimationFrame(upd),{passive:true});addEventListener('resize',upd);upd()});

/* reviews carousel */
$$('.car').forEach(c=>{const tr=$('.car-track',c),sl=$$('.slide',c),dots=$('.dots',c);let i=0,tm;
 sl.forEach((s,k)=>{const b=d.createElement('button');b.type='button';b.setAttribute('aria-label','Show review '+(k+1));b.onclick=()=>go(k,1);dots.appendChild(b)});
 function go(k,user){i=(k+sl.length)%sl.length;tr.style.transform=`translateX(${-100*i}%)`;$$('button',dots).forEach((b,j)=>b.setAttribute('aria-current',j===i));sl.forEach((s,j)=>{s.setAttribute('aria-hidden',j!==i);s.inert=j!==i});if(user)auto()}
 function auto(){clearInterval(tm);if(!RM)tm=setInterval(()=>go(i+1),7000)}
 $('.pv',c).onclick=()=>go(i-1,1);$('.nx',c).onclick=()=>go(i+1,1);
 c.addEventListener('mouseenter',()=>clearInterval(tm));c.addEventListener('mouseleave',auto);c.addEventListener('focusin',()=>clearInterval(tm));c.addEventListener('focusout',auto);
 let sx=null;tr.addEventListener('pointerdown',e=>sx=e.clientX);addEventListener('pointerup',e=>{if(sx===null)return;const dx=e.clientX-sx;sx=null;if(Math.abs(dx)>50)go(i+(dx<0?1:-1),1)});
 go(0);auto()});

/* draggable gallery + lightbox */
$$('.gal-track').forEach(t=>{let down=false,sx=0,sl=0,moved=0,v=0,lx=0,raf;
 t.addEventListener('pointerdown',e=>{if(e.pointerType!=='mouse')return;down=true;moved=0;sx=lx=e.clientX;sl=t.scrollLeft;t.classList.add('drag');cancelAnimationFrame(raf)});
 addEventListener('pointermove',e=>{if(!down)return;const dx=e.clientX-sx;moved=Math.max(moved,Math.abs(dx));v=e.clientX-lx;lx=e.clientX;t.scrollLeft=sl-dx});
 addEventListener('pointerup',()=>{if(!down)return;down=false;t.classList.remove('drag');if(!RM){(function m(){v*=.92;t.scrollLeft-=v;if(Math.abs(v)>.5)raf=requestAnimationFrame(m)})()}});
 t.addEventListener('click',e=>{if(moved>6){e.preventDefault();e.stopPropagation();moved=0}},true)});
const lb=$('.tlb');
if(lb){const items=$$('.gal-item'),im=$('img',lb),cap=$('p',lb),btns=$$('button',lb);let k=0,last=null;
 function show(n){k=(n+items.length)%items.length;const it=items[k],ti=$('img',it);im.src=it.dataset.full;im.alt=ti.alt;cap.textContent=ti.alt}
 items.forEach((it,n)=>it.addEventListener('click',()=>{last=it;show(n);lb.classList.add('open');lb.setAttribute('aria-hidden','false');d.body.style.overflow='hidden';$('.x1',lb).focus()}));
 const close=()=>{lb.classList.remove('open');lb.setAttribute('aria-hidden','true');d.body.style.overflow='';last&&last.focus()};
 $('.x1',lb).onclick=close;$('.pv',lb).onclick=()=>show(k-1);$('.nx',lb).onclick=()=>show(k+1);
 lb.addEventListener('click',e=>{if(e.target===lb)close()});
 let tx=null;lb.addEventListener('touchstart',e=>tx=e.touches[0].clientX,{passive:true});lb.addEventListener('touchend',e=>{if(tx===null)return;const dx=e.changedTouches[0].clientX-tx;tx=null;if(Math.abs(dx)>50)show(k+(dx<0?1:-1))});
 addEventListener('keydown',e=>{if(!lb.classList.contains('open'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(k-1);if(e.key==='ArrowRight')show(k+1);
  if(e.key==='Tab'){const i=btns.indexOf(d.activeElement);e.preventDefault();btns[(i+(e.shiftKey?-1:1)+btns.length)%btns.length].focus()}})}

/* estimate form: builds a text message to the shop; nothing is submitted anywhere */
const f=$('#estimate-form');
if(f){const msg=()=>{const v=n=>(f.elements[n]&&f.elements[n].value||'').trim();return `Estimate request from the website\nName: ${v('name')}\nPhone: ${v('phone')}\nVehicle: ${v('vehicle')}\nService: ${v('service')}\nDetails: ${v('details')}`};
 f.addEventListener('submit',e=>{e.preventDefault();if(!f.reportValidity())return;const ios=/iP(hone|ad|od)/.test(navigator.userAgent);location.href=f.dataset.sms+(ios?'&':'?')+'body='+encodeURIComponent(msg())})}

/* demo pill */
const dm=$('.demo');if(dm){try{if(sessionStorage.getItem('ta-demo')==='x')dm.remove()}catch(e){};const x=$('button',dm);x&&x.addEventListener('click',()=>{dm.remove();try{sessionStorage.setItem('ta-demo','x')}catch(e){}})}
})();
