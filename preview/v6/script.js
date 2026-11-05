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
 const nav=document.querySelector('.nav-menu');const media=matchMedia('(min-width:1100px)');function navState(){nav.open=media.matches;}navState();media.addEventListener('change',navState);
 document.addEventListener('keydown',e=>{if(e.key==='Escape'){document.querySelectorAll('.products-menu').forEach(d=>d.open=false);if(!media.matches)nav.open=false;}});
 document.addEventListener('click',e=>{document.querySelectorAll('.products-menu[open]').forEach(d=>{if(!d.contains(e.target))d.open=false;});if(!media.matches&&!nav.contains(e.target))nav.open=false;});
 document.querySelectorAll('nav a').forEach(a=>{const u=new URL(a.href,location.href);if(u.pathname===location.pathname&&!u.search&&!u.hash)a.setAttribute('aria-current','page');});
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
