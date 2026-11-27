const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:794,height:1123}});
const names=['page1_cover','page2_meta-glasses','page3_essilorluxottica','page4_charts','page5_sources'];
const out=[];
for(const n of names){await pg.goto('file://'+process.cwd()+'/'+n+'.html');await pg.waitForTimeout(300);
 const o=await pg.evaluate(()=>{const p=document.querySelector('.page');const f=document.querySelector('footer');return [p.scrollHeight,p.clientHeight,[...p.children].reduce((m,c)=>c.tagName=='FOOTER'?m:Math.max(m,c.getBoundingClientRect().bottom),0),f.getBoundingClientRect().top]});
 console.log(n,o);
 await pg.screenshot({path:'/tmp/claude-0/-home-user-adhoc-Equity/9746c044-5665-561c-b0e4-2be86e403ba7/scratchpad/'+n+'.png'});
 await pg.pdf({path:'/tmp/claude-0/-home-user-adhoc-Equity/9746c044-5665-561c-b0e4-2be86e403ba7/scratchpad/'+n+'.pdf',width:'794px',height:'1123px',printBackground:true});}
await b.close();})();
