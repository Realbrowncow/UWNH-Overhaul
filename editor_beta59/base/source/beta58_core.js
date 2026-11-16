// Beta 5.8: guarded editing of project-native Test53 tables, separate from the
// older clean-2MiB map exporter and the former Beta5.7 Test44 workspace.
const UW53Core=(()=>{
 const SOURCE_SHA='9f91aaa32e91808397b470e58fd3104fe35c5885b554de5bf6e39a2d5efe6b78';
 const GOODS=__GOODS_JSON__;
 const SHIPS=__SHIPS_JSON__;
 const RULES=__RULES_JSON__;
 const STOCK_CAPS=__STOCK_JSON__;
 const PORT=0x08da7f,PRICE=0x240000,SHIP=0x08ce27,NAV=0x0881f3;
 const CK=new Set([0xffdc,0xffdd,0xffde,0xffdf]);
 let baseline=null,originLabel='',portNames=[],staged=new Map(),validOffsets=null;
 const loaded=()=>baseline!==null;
 function assertLoaded(){if(!loaded())throw Error('Load the exact Test53 ROM first.');}
 function makeOption(value,description){const o=document.createElement('option');o.value=String(value);o.textContent=description;return o;}
 function rangeInt(v,low,high,label){if(!Number.isInteger(v)||v<low||v>high)throw Error(`${label} must be an integer from ${low} to ${high}.`);return v;}
 function hx(v){return '0x'+v.toString(16).toUpperCase().padStart(6,'0');}
 function read8(at){assertLoaded();return staged.has(at)?staged.get(at):baseline[at];}
 function read16(at){return read8(at)|(read8(at+1)<<8);}
 function stage8(at,val){if(!validOffsets.has(at))throw Error('Unsafe/unmapped address '+hx(at));rangeInt(val,0,255,'Byte');if(baseline[at]===val)staged.delete(at);else staged.set(at,val);}
 function stage16(at,val){rangeInt(val,0,65535,'16-bit value');stage8(at,val&255);stage8(at+1,(val>>>8)&255);}
 const quoteAt=(port,good)=>PRICE+128*port+2*good;
 const economyAt=(port,slot)=>PRICE+128*port+119+slot;
 const shipAt=id=>SHIP+12*id;
 const portAt=id=>PORT+37*id;
 const faceAt=id=>NAV+50*id+26;
 function makeValidSet(){
  const a=new Set();const add=(p,n)=>{for(let i=0;i<n;i++)a.add(p+i);};
  for(let p=0;p<100;p++){
   for(let g=0;g<46;g++)add(quoteAt(p,g),2);
   for(let s=0;s<9;s++)add(economyAt(p,s),1);
   add(portAt(p)+32,3);
  }
  for(let s=0;s<25;s++){add(shipAt(s)+2,2);add(shipAt(s)+6,2);}
  // Existing navigator portrait references are u16, not single bytes. Their
  // high bytes can be nonzero for composed portrait records.
  for(let n=0;n<120;n++)add(faceAt(n),2);
  return a;
 }
 function refreshStatus(){
  $('t53Status').textContent=loaded()
   ?'TEST53 LOADED · SHA-256 VERIFIED\n'+SOURCE_SHA+'\n'+staged.size+' staged data byte(s) · 4,194,304-byte headerless image\nNo map re-encoding or NPC/stock-code rewrite.'
   :'Test53 not loaded. Choose the exact game image or load the bundled Test53.';
 }
 function fillUI(){
  portNames=uwReadPorts(baseline).slice(0,100).map((p,i)=>p?.name||('Port '+i));
  for(const key of ['t53Port','t53RareFrom','t53RareTo']){
   const s=$(key);s.replaceChildren();for(let p=0;p<100;p++)s.append(makeOption(p,p+' · '+portNames[p]));
  }
  $('t53Port').value='33';$('t53RareFrom').value='3';$('t53RareTo').value='77';
  const gs=$('t53Good');gs.replaceChildren();for(let g=0;g<46;g++)gs.append(makeOption(g,g+' · '+GOODS[g]));gs.value='0';
  const os=$('t53Offer');os.replaceChildren();for(let s=0;s<9;s++)os.append(makeOption(s,'Offer slot '+s));os.value='0';
  const sh=$('t53Ship');sh.replaceChildren();for(let id=0;id<25;id++)sh.append(makeOption(id,id+' · '+SHIPS[id]));sh.value='11';
  const nv=$('t53Navigator');nv.replaceChildren();for(let n=0;n<120;n++)nv.append(makeOption(n,'Navigator #'+n));nv.value='0';
  const rules=$('t53Rule');rules.replaceChildren();for(let i=0;i<RULES.length;i++)rules.append(makeOption(i,RULES[i].pc+' · '+RULES[i].status));rules.value='0';
  refreshAll();
 }
 function currentPort(){return rangeInt(Number($('t53Port').value),0,99,'Port ID');}
 function refreshQuote(){if(!loaded())return;let p=currentPort(),g=Number($('t53Good').value),at=quoteAt(p,g);$('t53Quote').value=String(read16(at));$('t53QuoteAddr').value=hx(at);$('t53GoodStock').textContent=GOODS[g]+' · approved four-month producer stock cap '+(STOCK_CAPS[g]??'not recorded')+'. This is a design reference, not an editable ROM stock counter.';}
 function refreshEconomy(){if(!loaded())return;const at=economyAt(currentPort(),Number($('t53Offer').value));$('t53Economy').value=String(read8(at)*10);$('t53EconAddr').value=hx(at);}
 function refreshShip(){if(!loaded())return;const id=Number($('t53Ship').value),at=shipAt(id);$('t53Tack').value=String(read8(at+2));$('t53Sail').value=String(read8(at+3));$('t53Capacity').value=String(read16(at+6));$('t53ShipInfo').textContent='Model record '+hx(at)+' · draft/approved model data should be checked against the V8v4 workbook before editing.';}
 function refreshPort(){if(!loaded())return;const at=portAt(currentPort());$('t53Geo').value=String(read8(at+33));$('t53Yard').value=String(read8(at+34));}
 function itemId(p){return read8(portAt(p)+32);}
 function refreshRare(){if(!loaded())return;const a=Number($('t53RareFrom').value),b=Number($('t53RareTo').value);$('t53RareInfo').textContent='Source #'+a+': special item ID '+itemId(a)+'; destination #'+b+': '+itemId(b)+' (255 = empty).';}
 function refreshFace(){if(!loaded())return;const at=faceAt(Number($('t53Navigator').value)),raw=read16(at);$('t53Face').value=String(raw);$('t53FaceAddr').value=hx(at);$('t53FaceCurrent').textContent='Raw little-endian portrait reference: '+raw+' ('+read8(at)+', '+read8(at+1)+'). '+(raw>127?'This is a composed/extended reference. Enter a 0–127 standard portrait to replace both bytes.':'This is a standard face reference.');}
 function refreshRule(){const r=RULES[Number($('t53Rule').value)]||RULES[0];$('t53RuleInfo').textContent=r.pc+': '+r.implemented_choices+'; '+r.status+'; native bytes '+r.after_hex+'. Reference only: the runtime generator encoding is a separate subsystem.';}
 function refreshAll(){refreshStatus();refreshQuote();refreshEconomy();refreshShip();refreshPort();refreshRare();refreshFace();refreshRule();}
 function checkRare(){
  let counts1=new Map(),counts2=new Map();
  for(let p=0;p<100;p++){
   const original=baseline[portAt(p)+32],item=itemId(p);
   if(original!==255)counts1.set(original,(counts1.get(original)||0)+1);
   if(item!==255){counts2.set(item,(counts2.get(item)||0)+1);
    for(let s=29;s<=31;s++)if(item===baseline[portAt(p)+s])throw Error('Duplicate equipment item at port '+p+'.');
   }
  }
  const normalized=x=>JSON.stringify([...x.entries()].sort((a,b)=>a[0]-b[0]));
  if(normalized(counts1)!==normalized(counts2))throw Error('Rare item frequencies changed; use the swap control.');
 }
 function stageQuoted(){stage16(quoteAt(currentPort(),Number($('t53Good').value)),rangeInt(Number($('t53Quote').value),0,65535,'Quote'));refreshAll();}
 function stageEconomy(){const v=rangeInt(Number($('t53Economy').value),0,2550,'Economy');if(v%10)throw Error('Economy gate must be a multiple of 10.');stage8(economyAt(currentPort(),Number($('t53Offer').value)),v/10);refreshAll();}
 function stageShip(){const at=shipAt(Number($('t53Ship').value));const tack=rangeInt(Number($('t53Tack').value),0,255,'Tacking'),sail=rangeInt(Number($('t53Sail').value),0,255,'Sailing'),capacity=rangeInt(Number($('t53Capacity').value),0,65535,'Capacity');stage8(at+2,tack);stage8(at+3,sail);stage16(at+6,capacity);refreshAll();}
 function stagePort(){const at=portAt(currentPort());const geo=rangeInt(Number($('t53Geo').value),0,12,'Geographic region'),yard=rangeInt(Number($('t53Yard').value),0,10,'A–K yard index');stage8(at+33,geo);stage8(at+34,yard);refreshAll();}
 function stageFace(){stage16(faceAt(Number($('t53Navigator').value)),rangeInt(Number($('t53Face').value),0,127,'Fixed-face ID'));refreshAll();}
 function swapRare(){assertLoaded();const a=Number($('t53RareFrom').value),b=Number($('t53RareTo').value);if(a===b)throw Error('Choose two different ports.');const x=itemId(a),y=itemId(b);if(x===255)throw Error('Source has no special item.');stage8(portAt(a)+32,y);stage8(portAt(b)+32,x);try{checkRare();}catch(err){stage8(portAt(a)+32,x);stage8(portAt(b)+32,y);throw err;}refreshAll();}
 function resetRare(){assertLoaded();for(let p=0;p<100;p++)stage8(portAt(p)+32,baseline[portAt(p)+32]);refreshAll();}
 function resetPair(fields){assertLoaded();for(const at of fields)stage8(at,baseline[at]);refreshAll();}
 function snapshot(){return loaded()?{expectedSha256:SOURCE_SHA,byteEdits:[...staged].sort((a,b)=>a[0]-b[0])}:null;}
 function projectImport(src){
  if(!src)return;assertLoaded();if(src.expectedSha256!==SOURCE_SHA)throw Error('Project Test53 baseline SHA mismatch.');
  if(!Array.isArray(src.byteEdits)||src.byteEdits.length>validOffsets.size)throw Error('Invalid Test53 project edit list.');
  const incoming=new Map();for(const pair of src.byteEdits){
   if(!Array.isArray(pair)||pair.length!==2)throw Error('Malformed Test53 edit');
   const [at,val]=pair;rangeInt(at,0,baseline.length-1,'Address');rangeInt(val,0,255,'Value');
   if(!validOffsets.has(at)||incoming.has(at))throw Error('Unsafe or duplicate Test53 edit '+hx(at));
   if(baseline[at]!==val)incoming.set(at,val);
  }
  const previous=staged;staged=incoming;try{checkRare();}catch(err){staged=previous;throw err;}refreshAll();
 }
 async function load(input,label){
  const inspected=UWIdentityCore.inspect(input),rom=inspected.body;
  if(rom.length!==0x400000)throw Error('Test53 requires an exact headerless 4 MiB US SNES ROM.');
  const hash=await uwSHA256(rom);if(hash!==SOURCE_SHA)throw Error('This is not Test53. Expected '+SOURCE_SHA+'; received '+hash+'.');
  baseline=rom.slice();originLabel=label;staged=new Map();validOffsets=makeValidSet();
  uwIdLoad(input,label,true);
  // The clean-2MiB terrain exporter is not compatible with this ROM. Disable
  // all its write controls and leave its map and ship views as previews only.
  sourceROM=null;sourceWorld=null;sourceROMName='';shipLoadFromROM(input,true);
  for(const id of ['shipApply','shipReset','shipV5','shipResetAll','portApply','portUndo','portReset','exportRom','riverApply','riverApplyAll','riverWaypoints'])$(id).disabled=true;
  setTool('pan');for(const el of $('tools').querySelectorAll('button'))el.disabled=!['pan','pick'].includes(el.dataset.tool);
  document.body.dataset.uw44Readonly='1';for(const el of $('shipFields').querySelectorAll('input'))el.disabled=true;
  $('status').textContent='Test 53 · guarded 4 MiB editing workspace';
  $('warnmain').textContent='Test53 project loaded. Original 2 MiB map exporter is DISABLED. Use Test53 ROM/IPS buttons below.';
  portCatalog=uwReadPorts(input);discoveryCatalog=uwReadDiscoveries(input);portMoves={};portHistory=[];refreshPortList();refreshSupplyList();refreshDiscoveryList();
  try{const dec=new UWNHMapDecoder(rom.subarray(0,0x200000)).decode();world=dec.map.slice();refreshMap();fit();}catch(err){console.warn('Test53 map preview not available',err);}
  fillUI();
  if(window.__uw53ProjectPending){projectImport(window.__uw53ProjectPending);window.__uw53ProjectPending=null;}
  notice('Exact Test53 loaded and SHA-256 verified. Only allowed project-table bytes can be edited; original map exporter disabled.',false,8500);
  return {hash,bytes:rom.length};
 }
 async function bundled(){
  if(!window.DecompressionStream)throw Error('Modern Chrome or Edge with DecompressionStream is required.');
  const enc=base64ToBytes($('test53-rom-bundle').textContent.trim());
  if(!enc.length)throw Error('No private ROM bundle here; use Choose exact Test53 ROM.');
  const stream=new Blob([enc]).stream().pipeThrough(new DecompressionStream('deflate'));
  const rom=new Uint8Array(await new Response(stream).arrayBuffer());
  return load(rom,'UWNH_Test53_EXACT_PROJECT_BASE.smc');
 }
 function buildOutput(){assertLoaded();checkRare();
  const identity=uwIdExportROM(baseline),out=identity.slice();
  if(out.length!==baseline.length)throw Error('Identity module changed ROM size.');
  const allowed=new Set([...staged.keys(),...CK]);
  for(const [at,v] of staged)out[at]=v;
  if(staged.size||!identity.every((v,i)=>v===baseline[i]))uwChecksum(out);
  for(let i=0;i<out.length;i++)if(!allowed.has(i)&&out[i]!==identity[i])throw Error('Unexpected write beyond staged table addresses: '+hx(i));
  for(const [at,v] of staged)if(out[at]!==v)throw Error('ROM stage did not round-trip at '+hx(at));
  const sum=out.reduce((a,v)=>(a+v)&65535,0),stored=out[0xffde]|out[0xffdf]<<8,complement=out[0xffdc]|out[0xffdd]<<8;
  if(sum!==stored||(stored^complement)!==65535)throw Error('SNES checksum/complement verification failed.');
  const changed=out.reduce((a,v,i)=>a+(v!==baseline[i]),0);
  return {out,changed};
 }
 function makeIPS(source,target){
  const blocks=[new Uint8Array([80,65,84,67,72])];let n=source.length;
  for(let i=0;i<n;){
   if(source[i]===target[i]){i++;continue;}
   const pos=i;while(i<n&&source[i]!==target[i]&&i-pos<65535)i++;
   const size=i-pos,head=new Uint8Array([(pos>>>16)&255,(pos>>>8)&255,pos&255,(size>>>8)&255,size&255]);blocks.push(head,target.slice(pos,i));
  }
  blocks.push(new Uint8Array([69,79,70]));let total=blocks.reduce((a,b)=>a+b.length,0),out=new Uint8Array(total),off=0;
  for(const b of blocks){out.set(b,off);off+=b.length;}return out;
 }
 function replayIPS(src,ips){
  let a=src.slice(),i=5;while(i<ips.length-3){const pos=(ips[i]<<16)|(ips[i+1]<<8)|ips[i+2],len=(ips[i+3]<<8)|ips[i+4];i+=5;if(len===0)throw Error('Unexpected RLE IPS');a.set(ips.slice(i,i+len),pos);i+=len;}return a;
 }
 async function exportFile(kind){
  const {out,changed}=buildOutput(),hash=await uwSHA256(out);
  let suffix='';if(kind==='ips'){
   const ips=makeIPS(baseline,out),replayed=replayIPS(baseline,ips);
   if(!replayed.every((v,i)=>v===out[i]))throw Error('IPS roundtrip failure');
   suffix='IPS '+ips.length+' bytes; ';
   saveBlob(new Blob([ips],{type:'application/octet-stream'}),'UWNH_Test53_Beta58_Modified_from_Test53.ips');
  }else saveBlob(new Blob([out],{type:'application/octet-stream'}),'UWNH_Test53_Beta58_Modified_EXPERIMENTAL.smc');
  $('t53ExportInfo').textContent=suffix+changed+' changed bytes including any identity and checksum changes. Output SHA-256: '+hash+'\nExact Test53 source SHA-256: '+SOURCE_SHA+'\nStatic integrity PASS; gameplay NOT YET VERIFIED.';
  notice('Test53 '+(kind==='ips'?'IPS':'ROM')+' exported; '+changed+' modified byte(s), checksum PASS. Test in emulator.',false,9000);
  return {sha256:hash,changed};
 }
 function audit(){assertLoaded();const groups=new Map();for(const [at,v] of staged)groups.set(hx(at),baseline[at]+' → '+v);
  const sample=[...groups].sort((a,b)=>a[0].localeCompare(b[0])).slice(0,24).map(([k,v])=>k+': '+v).join('\n');
  $('t53ExportInfo').textContent=staged.size+' altered data byte(s) from exact Test53.\n'+(sample||'No changes staged.')+(staged.size>24?'\n… plus '+(staged.size-24)+' more':'')+'\nOnly selected known native table fields may be exported; identity is audited separately.';
 }
 function setup(){
  const handle=(fn)=>()=>{try{fn();}catch(err){notice('Test53 edit blocked: '+err.message,true,10000);}};
  $('t53Load').onclick=()=>bundled().catch(err=>notice('Test53 load failed: '+err.message,true,12000));
  $('t53Open').onclick=()=>{openMode='test53';$('file').click();};
  $('t53Port').onchange=()=>{refreshQuote();refreshEconomy();refreshPort();};
  $('t53Good').onchange=refreshQuote;$('t53Offer').onchange=refreshEconomy;$('t53Ship').onchange=refreshShip;
  $('t53RareFrom').onchange=refreshRare;$('t53RareTo').onchange=refreshRare;$('t53Navigator').onchange=refreshFace;$('t53Rule').onchange=refreshRule;
  $('t53QuoteApply').onclick=handle(stageQuoted);$('t53QuoteReset').onclick=handle(()=>{const at=quoteAt(currentPort(),Number($('t53Good').value));resetPair([at,at+1]);});
  $('t53EconApply').onclick=handle(stageEconomy);$('t53EconReset').onclick=handle(()=>resetPair([economyAt(currentPort(),Number($('t53Offer').value))]));
  $('t53ShipApply').onclick=handle(stageShip);$('t53ShipReset').onclick=handle(()=>{const at=shipAt(Number($('t53Ship').value));resetPair([at+2,at+3,at+6,at+7]);});
  $('t53PortApply').onclick=handle(stagePort);$('t53PortReset').onclick=handle(()=>{const at=portAt(currentPort());resetPair([at+33,at+34]);});
  $('t53RareSwap').onclick=handle(swapRare);$('t53RareReset').onclick=handle(resetRare);
  $('t53FaceApply').onclick=handle(stageFace);$('t53FaceReset').onclick=handle(()=>{const at=faceAt(Number($('t53Navigator').value));resetPair([at,at+1]);});
  $('t53Reset').onclick=handle(()=>{staged=new Map();refreshAll();});$('t53Audit').onclick=handle(audit);
  $('t53SaveEdits').onclick=handle(()=>{assertLoaded();saveBlob(new Blob([JSON.stringify(snapshot(),null,2)],{type:'application/json'}),'UWNH_Test53_Beta58_Editable_Settings.json');});
  $('t53OpenEdits').onclick=()=>{$('t53EditsFile').click();};
  $('t53EditsFile').onchange=async e=>{const file=e.target.files[0];if(!file)return;try{projectImport(JSON.parse(await file.text()));notice('Test53 settings loaded. No ROM written until export.');}catch(err){notice('Test53 settings refused: '+err.message,true,11000);}e.target.value='';};
  $('t53ExportRom').onclick=()=>exportFile('rom').catch(err=>notice('Test53 export blocked: '+err.message,true,12000));
  $('t53ExportIps').onclick=()=>exportFile('ips').catch(err=>notice('Test53 export blocked: '+err.message,true,12000));
 }
 return {setup,load,bundled,snapshot,projectImport,buildOutput,exportFile,verify:()=>({loaded:loaded(),expectedSha:SOURCE_SHA,stagedBytes:staged.size})};
})();
UW53Core.setup();
