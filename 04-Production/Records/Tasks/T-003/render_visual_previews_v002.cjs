const fs=require('fs'); const path=require('path'); const {pathToFileURL}=require('url');
const {chromium}=require('C:/Users/RZ1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
const root=path.resolve(__dirname,'../../../..');
const manifestPath=path.join(__dirname,'Previews/v002/preview-manifest_v002.json');
const manifest=JSON.parse(fs.readFileSync(manifestPath,'utf8'));
const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
const page=await browser.newPage({viewport:{width:1920,height:1280},deviceScaleFactor:1});
const checks=[];
try{
for(const shot of manifest.shots){
 await page.goto(pathToFileURL(path.join(root,shot.html)).href);
 await page.evaluate(async()=>{await document.fonts.ready; await Promise.all([...document.images].map(i=>i.decode()));});
 const check=await page.evaluate(()=>({loaded:[...document.images].every(i=>i.complete&&i.naturalWidth>0),bodyHeight:document.querySelector('.page').scrollHeight,footerBottom:document.querySelector('.footer').getBoundingClientRect().bottom,notes:[...document.querySelectorAll('.notes section')].map(e=>e.getBoundingClientRect().bottom)}));
 if(!check.loaded||check.bodyHeight>1280||check.footerBottom>1280||check.notes.some(y=>y>1235)) throw Error('Layout failure '+shot.shot+' '+JSON.stringify(check));
 await page.screenshot({path:path.join(root,shot.png)});
 checks.push({shot:shot.shot,...check});
 console.log('Rendered '+shot.shot);
}
for(const section of [...new Set(manifest.shots.map(s=>s.shot.slice(0,3)))]){
 const shots=manifest.shots.filter(s=>s.shot.startsWith(section));
 const height=170+Math.ceil(shots.length/2)*626;
 const html='<!doctype html><html><head><meta charset="utf-8"><style>*{box-sizing:border-box}body{margin:0;padding:36px;background:#112635;color:#e9f3f7;font:24px Arial}h1{font-size:36px;margin:0 0 12px}p{font-size:19px;color:#abc5d4;margin:0 0 28px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:22px}img{width:100%;height:auto;display:block}</style></head><body><h1>'+section+' · A03 shot previews v002</h1><p>Source-based storyboard sheets · camera / information intent preserved · not product renders</p><div class="grid">'+shots.map(s=>'<img src="'+pathToFileURL(path.join(root,s.png)).href+'">').join('')+'</div></body></html>';
 const proofPath=path.join(__dirname,'Previews/v002/'+section+'_overview_v002.html');
 fs.writeFileSync(proofPath,html);
 await page.setViewportSize({width:1920,height});
 await page.goto(pathToFileURL(proofPath).href);
 await page.evaluate(async()=>await Promise.all([...document.images].map(i=>i.decode())));
 await page.screenshot({path:proofPath.replace('.html','.png')});
}
await page.setViewportSize({width:1440,height:1000});
await page.goto(pathToFileURL(path.join(__dirname,'Previews/v002/gallery_v002.html')).href);
await page.screenshot({path:path.join(__dirname,'Previews/v002/gallery-top_v002.png')});
fs.writeFileSync(path.join(__dirname,'Evidence/preview-layout-checks_v002.json'),JSON.stringify(checks,null,2));
}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
