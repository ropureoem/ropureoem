'use strict';
function sendQuote(e){
 e.preventDefault();const f=document.getElementById('quote-form');const d=new FormData(f);
 const lines=['Name: '+d.get('name'),'Company: '+(d.get('company')||''),'Email: '+d.get('email'),'WhatsApp: '+(d.get('whatsapp')||''),'Target market: '+d.get('market'),'Model of interest: '+d.get('model'),'','Message:',String(d.get('message')||'')];
 window.location.href='mailto:info@ropureoem.com?subject='+encodeURIComponent('Quote request — '+d.get('model')+' — '+d.get('market'))+'&body='+encodeURIComponent(lines.join('\n'));
 let status=document.getElementById('quote-status');if(!status){status=document.createElement('p');status.id='quote-status';status.setAttribute('role','status');f.append(status);}status.textContent=document.documentElement.lang==='zh'?'您的邮件应用将打开并填好需求。请在邮件应用中点击发送至 info@ropureoem.com。':'Your email app will open with your request. Press Send there to email info@ropureoem.com.';return false;
}
(function(){
 document.querySelectorAll('[data-language]').forEach(a=>{const u=new URL(a.href,location.href);u.search=location.search;u.hash=location.hash;a.href=u.href;a.addEventListener('click',()=>{const target=new URL(a.href,location.href);target.search=location.search;target.hash=location.hash;a.href=target.href;});});
 const params=new URLSearchParams(location.search);const model=params.get('model');const select=document.querySelector('select[name=model]');if(model&&select)select.value=model;
 const nav=document.querySelector('.nav-menu');const media=matchMedia('(min-width:1100px)');
 function closeMenu(){nav.open=false;nav.querySelectorAll('.products-menu[open]').forEach(d=>d.open=false);}
 function navState(){if(media.matches)nav.open=true;else closeMenu();}
 navState();media.addEventListener('change',navState);
 window.addEventListener('pageshow',e=>{if(e.persisted)navState();});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'){document.querySelectorAll('.products-menu').forEach(d=>d.open=false);if(!media.matches)closeMenu();}});
 document.addEventListener('click',e=>{document.querySelectorAll('.products-menu[open]').forEach(d=>{if(!d.contains(e.target))d.open=false;});if(!media.matches&&(!nav.contains(e.target)||e.target.closest('a[href]')))closeMenu();});
 document.querySelectorAll('nav a').forEach(a=>{const u=new URL(a.href,location.href);if(u.pathname===location.pathname&&!u.search&&!u.hash)a.setAttribute('aria-current','page');});
 const helpWidget=document.querySelector('.help-widget');
 if(helpWidget){
  helpWidget.open=false;
  helpWidget.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{helpWidget.open=false;}));
  document.addEventListener('click',e=>{if(!helpWidget.contains(e.target))helpWidget.open=false;});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&helpWidget.open){helpWidget.open=false;helpWidget.querySelector('summary').focus();}});
  window.addEventListener('pageshow',e=>{if(e.persisted)helpWidget.open=false;});
 }
 const form=document.querySelector('.catalogue-filters');if(!form)return;
 const input=form.querySelector('[name=q]'),range=form.querySelector('[name=range]');input.value=params.get('q')||'';range.value=params.get('range')||'';
 function filterProducts(update){
  const query=input.value.trim().toLowerCase(),selected=range.value;let count=0;
  document.querySelectorAll('.grid[data-cat]').forEach(grid=>{
   let visible=0;const category=grid.dataset.cat;const alias={ 'under-sink':'Under-Sink RO Systems','countertop':'Countertop','softener':'Water Softening','shower':'Shower Filters','faucet':'Faucet Filters'}[category];
   grid.querySelectorAll('.card').forEach(card=>{const match=(!query||(card.textContent+' '+alias).toLowerCase().includes(query))&&(!selected||(selected==='hot-cold-ice'?card.dataset.thermal==='true':selected===category));card.hidden=!match;if(match){count++;visible++;}});
   grid.hidden=!visible;const heading=grid.previousElementSibling;if(heading&&heading.tagName==='H2')heading.hidden=!visible;
  });
  document.getElementById('result-count').textContent=document.documentElement.lang==='zh'?count+' 款型号':count+' '+(count===1?'model':'models');document.getElementById('empty-state').hidden=count>0;
  if(update){const u=new URL(location.href);u.search='';u.hash='';if(input.value.trim())u.searchParams.set('q',input.value.trim());if(selected)u.searchParams.set('range',selected);history.replaceState(null,'',u);}
 }
 form.addEventListener('submit',e=>{e.preventDefault();filterProducts(true);});input.addEventListener('input',()=>filterProducts(true));range.addEventListener('change',()=>filterProducts(true));filterProducts(false);
})();
/* 2026-11-06 product-image fix: every "Product image pending" placeholder is replaced with the real catalogue photograph (assets/img/<SKU>.jpg). The shared stylesheet shows every product photo in the same 4:3 frame with one saturation/contrast treatment, so the restored photos match the 45 photos that were already published. */
(function restoreProductPhotos(){
  document.querySelectorAll('.image-pending').forEach(function(pending){
    var skuSpan=pending.querySelector('span');
    if(!skuSpan) return;
    var sku=skuSpan.textContent.trim();
    if(!/^RP-[A-Z]\d{2}$/.test(sku)) return;
    var img=document.createElement('img');
    img.src='/assets/img/'+sku+'.jpg';
    img.alt=sku+' product photograph';
    img.width=1200; img.height=900; img.loading='lazy'; img.decoding='async';
    pending.replaceWith(img);
  });
})();
/* 2026-11-06 catalogue merge: 62 SKUs remain orderable, but the split-tank softeners (RP-W01/W02/W03) and the sparkling-water series (RP-C05/C06/C14) are each shown as one entry, so the catalogue lists 58 entries. The header still said "62 models" on every page; relabel it instead of editing the nav in 150 files. */
(function relabelModelCount(){
  var map={'All 62 models':'All models','View all 62 models \u2192':'View all models \u2192','\u5168\u90e8 62 \u6b3e\u578b\u53f7':'\u5168\u90e8\u578b\u53f7','\u67e5\u770b\u5168\u90e8 62 \u6b3e\u578b\u53f7 \u2192':'\u67e5\u770b\u5168\u90e8\u578b\u53f7 \u2192'};
  document.querySelectorAll('a').forEach(function(a){
    var t=a.textContent.trim();
    if(map[t]) a.textContent=map[t];
  });
})();
/* Floating WhatsApp button (2026-11-07): one-tap WhatsApp contact on every page. */
(function addWhatsAppFloat(){
  if(document.querySelector('.wa-float')) return;
  var a=document.createElement('a');
  a.className='wa-float';
  a.href='https://wa.me/8618928823858';
  a.target='_blank';
  a.rel='noopener noreferrer';
  a.setAttribute('aria-label',document.documentElement.lang==='zh'?'WhatsApp 联系我们':'Chat on WhatsApp');
  a.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.263.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>';
  document.body.appendChild(a);
})();
