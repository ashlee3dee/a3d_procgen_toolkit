const q=document.getElementById('q');
const groups=[...document.querySelectorAll('nav details')];
let filtering=false;
q.addEventListener('input',e=>{
const v=e.target.value.trim().toLowerCase();
if(v&&!filtering)groups.forEach(d=>d.dataset.wasOpen=d.open?'1':'');
document.querySelectorAll('nav a').forEach(a=>a.style.display=a.textContent.toLowerCase().includes(v)?'':'none');
groups.forEach(d=>{
const hit=[...d.querySelectorAll('a')].some(a=>a.style.display!=='none');
d.style.display=hit?'':'none';
d.open=v?hit:d.dataset.wasOpen==='1';
});
filtering=!!v;
});
function openCurrent(){
const a=document.querySelector('nav a[href="'+decodeURIComponent(location.hash)+'"]');
const d=a&&a.closest('details');
if(d)d.open=true;
}
window.addEventListener('hashchange',openCurrent);
openCurrent();
