const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:794,height:1123}});
const dir=process.cwd();const files=['page1_cover','page2_essilorluxottica','page3_charts','page4_sources'];
for(const f of files){await p.goto('file://'+dir+'/'+f+'.html');await p.waitForTimeout(500);
 const ov=await p.evaluate(()=>{const pg=document.querySelector('.page');const ft=document.querySelector('footer').getBoundingClientRect();let m=0;pg.querySelectorAll('*').forEach(x=>{if(x.closest('footer'))return;m=Math.max(m,x.getBoundingClientRect().bottom)});return [pg.scrollHeight,m,ft.top]});
 console.log(f,'scrollH',ov[0],'content bottom',Math.round(ov[1]),'footer top',Math.round(ov[2]));
 await p.pdf({path:'/tmp/'+f+'.pdf',width:'794px',height:'1123px',printBackground:true});}
await b.close()})()
