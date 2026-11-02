const {chromium}=require('playwright');
(async()=>{const [D]=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage({viewport:{width:794,height:1123}});
await p.goto('file://'+D+'/note.html');await p.waitForLoadState('networkidle');await p.evaluate(()=>document.fonts.ready);
const r=await p.evaluate(()=>[...document.querySelectorAll('.page')].map((pg,i)=>{const f=pg.querySelector('footer').getBoundingClientRect();let mx=0;
 pg.querySelectorAll('footer ~ *, .page > *:not(footer)').forEach(e=>{mx=Math.max(mx,e.getBoundingClientRect().bottom)});
 return {i:i+1,contentBottom:Math.round(mx-pg.getBoundingClientRect().top),footerTop:Math.round(f.top-pg.getBoundingClientRect().top),scroll:pg.scrollHeight}}));
console.log(JSON.stringify(r));
await p.pdf({path:D+'/ServiceNow_adhoc_opinion_2026-11-02.pdf',width:'794px',height:'1123px',printBackground:true});
for(let i=0;i<4;i++){await p.locator('.page').nth(i).screenshot({path:process.argv[3]+'/p'+(i+1)+'.png'});}
await b.close();})();
