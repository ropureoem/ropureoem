
function filterProducts(q){q=(q||'').toLowerCase();document.querySelectorAll('.grid .card').forEach(function(c){c.style.display=c.textContent.toLowerCase().includes(q)?'':'none';});}
function sendQuote(e){e.preventDefault();var f=document.getElementById('quote-form');var d=new FormData(f);
var lines=['Name: '+d.get('name'),'Company: '+(d.get('company')||''),'Email: '+d.get('email'),'WhatsApp: '+(d.get('whatsapp')||''),'Target market: '+d.get('market'),'Model of interest: '+d.get('model'),'','Message:',''+(d.get('message')||'')];
window.location.href='mailto:info@ropureoem.com?subject='+encodeURIComponent('Quote request — '+d.get('model')+' — '+d.get('market'))+'&body='+encodeURIComponent(lines.join('\n'));
alert('Your email app will open with the quote request addressed to info@ropureoem.com. Please press Send in your email app.');return false;}
(function(){var p=new URLSearchParams(location.search);var m=p.get('model');if(m){var s=document.querySelector('select[name=model]');if(s){s.value=m;}}})();
