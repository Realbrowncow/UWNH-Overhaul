#!/usr/bin/env node
// Independent code-level browser-core test when Chromium sandbox blocks launch.
import fs from 'node:fs';
import vm from 'node:vm';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const filename=process.argv[2] ? path.resolve(process.argv[2]) : path.join(here,'deliverables/New_Horizons_World_Ship_Fleet_Studio_Beta_5_9_Test54c_Integrated.html');
const html=fs.readFileSync(filename,'utf8');
const romPath=process.argv[3] ? path.resolve(process.argv[3]) : path.join(here,'../outputs/uwnh_test54c_rimbo_bio_20261116/UWNH_Test54c_Rimbo_Biography_IntroText_EXPERIMENTAL_2026-11-16.smc');
const original=fs.readFileSync(romPath);
const exact=new Uint8Array(original);
assert.equal(exact.length,0x400000);
assert.equal(crypto.createHash('sha256').update(exact).digest('hex'),'924ee53c49d125aa0cd23059d9bbfec42ede83cda50c36f6235431bb0db63a01');
assert.equal(html.match(/id="test54cSection"/g)?.length,1);
assert.equal(html.match(/id="test44Section"/g)?.length,1);
assert(html.includes("openMode==='test54c'"));
assert(html.includes('test54cEdits:UW54Core.snapshot()'));
const start=html.indexOf('const UW54Core=(()=>{');
const end=html.indexOf('\nUW54Core.setup();',start);
assert(start>0&&end>start);
const core=html.slice(start,end);
new vm.Script(core,{filename:'beta59_core.js'});

const elements=new Map(), downloads=[];
function elem(id){
 if(!elements.has(id))elements.set(id,{
  id,value:'',textContent:'',checked:false,disabled:false,style:{},dataset:{},
  items:[],onclick:null,onchange:null,
  append(...values){this.items.push(...values);},replaceChildren(...values){this.items=[...values];},
  querySelectorAll(){return [];},
 });
 return elements.get(id);
}
const context={
 console,window:{DecompressionStream},document:{body:{dataset:{}},createElement:()=>({value:'',textContent:''})},
 $:elem, Blob,Response,DecompressionStream,Uint8Array,Map,Set,
 base64ToBytes:(b)=>new Uint8Array(Buffer.from(b,'base64')),
 UWIdentityCore:{inspect:(a)=>({body:a})},
 uwSHA256:async (a)=>crypto.createHash('sha256').update(a).digest('hex'),
 uwIdLoad:()=>{},uwIdExportROM:(a)=>a.slice(),
 uwChecksum:(a)=>{let sum=0;for(const b of a)sum=(sum+b)&65535;a[0xffdc]=~sum&255;a[0xffdd]=~sum>>>8&255;a[0xffde]=sum&255;a[0xffdf]=sum>>>8&255;},
 uwReadPorts:()=>Array.from({length:130},(_,i)=>({name:'Native Port '+i})),
 shipLoadFromROM:()=>{},setTool:()=>{},
 sourceROM:null,sourceWorld:null,sourceROMName:'',
 portCatalog:[],discoveryCatalog:[],portMoves:{},portHistory:[],
 uwReadDiscoveries:()=>[],refreshPortList:()=>{},refreshSupplyList:()=>{},refreshDiscoveryList:()=>{},
 UWNHMapDecoder:class {decode(){return {map:new Uint8Array(1024)}}},
 world:null,refreshMap:()=>{},fit:()=>{},
 notice:(message)=>{if(message.startsWith('Test54c edit blocked:'))throw Error(message)},
 saveBlob:(blob,name)=>downloads.push({blob,name}),
};
vm.createContext(context);
vm.runInContext(core+'\nthis.UW54Core=UW54Core;',context);
context.UW54Core.setup();
const verify=context.UW54Core.verify;
await context.UW54Core.load(exact,'test54c.smc');
assert(verify().loaded);
// Exercise exactly the browser-facing compressed-ROM load path too.
const bundled=html.match(/<script id="test54c-rom-bundle" type="text\/plain">([\s\S]*?)<\/script>/);
assert(bundled);
const oldElem=elem('test54c-rom-bundle');oldElem.textContent=bundled[1];
await context.UW54Core.bundled();
assert(verify().loaded);
assert.equal(elem('t54cPort').items.length,100);
assert.equal(elem('t54cGood').items.length,46);
assert.equal(elem('t54cShip').items.length,25);
assert.equal(elem('t54cRule').items.length,63);
assert.equal(elem('t54cNavigator').items.length,120);
const unedited=context.UW54Core.buildOutput();
assert.equal(unedited.changed,0);
assert.deepEqual(Buffer.from(unedited.out),original);

// Change one port-by-good quote; verify exact address and no collateral edits.
const quoteAddress=0x240000+128*33;
const oldQuote=exact[quoteAddress]+(exact[quoteAddress+1]<<8);
elem('t54cQuote').value=String(oldQuote+1);
elem('t54cQuoteApply').onclick();
let edited=context.UW54Core.buildOutput();
assert.equal(edited.out[quoteAddress]+(edited.out[quoteAddress+1]<<8),oldQuote+1);
for(let i=0;i<exact.length;i++){
 if(exact[i]!==edited.out[i])assert([quoteAddress,quoteAddress+1,0xffdc,0xffdd,0xffde,0xffdf].includes(i));
}
const saved=context.UW54Core.snapshot();
assert(saved.byteEdits.length>0);
elem('t54cReset').onclick();
assert.equal(verify().stagedBytes,0);
context.UW54Core.projectImport(saved);
assert.equal(verify().stagedBytes,saved.byteEdits.length);
elem('t54cQuoteReset').onclick();
assert.equal(verify().stagedBytes,0);

// Exercise ship, region, Economy producer gate, fixed-face reference controls.
for(const [name,button,max] of [
 ['t54cTack','t54cShipApply',255],['t54cYard','t54cPortApply',10],
 ['t54cEconomy','t54cEconApply',255],['t54cFace','t54cFaceApply',127],
]){
 const value=+elem(name).value;
 elem(name).value=String(name==='t54cEconomy'?(((value/10+1)%256)*10):((value+1)%(max+1)));
 elem(button).onclick();
 assert(verify().stagedBytes>0,name);
}
edited=context.UW54Core.buildOutput();
assert(edited.changed>=4);
elem('t54cReset').onclick();

// Composed navigator portraits have a nonzero high byte. A standard face must
// clear BOTH native bytes (+26 and +27), then restore both on reset.
elem('t54cNavigator').value='8';elem('t54cNavigator').onchange();
const faceAt=0x0881f3+50*8+26;
assert(exact[faceAt+1]!==0);
elem('t54cFace').value='113';elem('t54cFaceApply').onclick();
edited=context.UW54Core.buildOutput();
assert.equal(edited.out[faceAt],113);
assert.equal(edited.out[faceAt+1],0);
elem('t54cFaceReset').onclick();
assert.equal(verify().stagedBytes,0);

// Special items: choose two compatible nonempty offers, swap, then restore.
const portAt=id=>0x08da7f+37*id;
let pair=null;
for(let a=0;a<100&&!pair;a++)for(let b=a+1;b<100;b++){
 const x=exact[portAt(a)+32],y=exact[portAt(b)+32];
 const ordA=[29,30,31].map(i=>exact[portAt(a)+i]);
 const ordB=[29,30,31].map(i=>exact[portAt(b)+i]);
 if(x!==255&&y!==255&&x!==y&&!ordA.includes(y)&&!ordB.includes(x)){pair=[a,b];break;}
}
assert(pair,'Need a valid special-item test pair');
elem('t54cRareFrom').value=String(pair[0]);elem('t54cRareTo').value=String(pair[1]);
elem('t54cRareSwap').onclick();
edited=context.UW54Core.buildOutput();
assert.equal(edited.out[portAt(pair[0])+32],exact[portAt(pair[1])+32]);
assert.equal(edited.out[portAt(pair[1])+32],exact[portAt(pair[0])+32]);
elem('t54cRareReset').onclick();
assert.equal(verify().stagedBytes,0);

// Unsafe imported settings and mismatching ROMs are rejected without mutation.
assert.throws(()=>context.UW54Core.projectImport({expectedSha256:verify().expectedSha,byteEdits:[[0x100000,0x23]]}),/Unsafe/);
assert.equal(verify().stagedBytes,0);
const bad=exact.slice();bad[0x123456]^=1;
await assert.rejects(()=>context.UW54Core.load(bad,'tampered.smc'),/not Test54c/);
assert.equal(verify().stagedBytes,0);

// Export IPS, replay it on the exact base, and compare to the ROM export.
elem('t54cQuote').value=String(oldQuote+1);elem('t54cQuoteApply').onclick();
const expected=context.UW54Core.buildOutput().out;
await context.UW54Core.exportFile('ips');
assert(downloads.at(-1).name.endsWith('.ips'));
const ips=new Uint8Array(await downloads.at(-1).blob.arrayBuffer());
assert.equal(Buffer.from(ips.slice(0,5)).toString(),'PATCH');
assert.equal(Buffer.from(ips.slice(-3)).toString(),'EOF');
const reconstructed=exact.slice();let cursor=5;
while(cursor<ips.length-3){
 const at=(ips[cursor]<<16)|(ips[cursor+1]<<8)|ips[cursor+2];
 const length=(ips[cursor+3]<<8)|ips[cursor+4];cursor+=5;
 reconstructed.set(ips.slice(cursor,cursor+length),at);cursor+=length;
}
assert.deepEqual(Buffer.from(reconstructed),Buffer.from(expected));
await context.UW54Core.exportFile('rom');
assert(downloads.at(-1).name.endsWith('.smc'));
assert.deepEqual(Buffer.from(new Uint8Array(await downloads.at(-1).blob.arrayBuffer())),Buffer.from(expected));
assert.deepEqual(Buffer.from(exact),original,'Baseline must be immutable');

console.log(JSON.stringify({result:'PASS',sourceSHA256:verify().expectedSha,
 panels:['Test54c','Test44','legacy map'],tested:['bundled Test54c decompression','source roundtrip','trade quote isolated',
 'ship stats','Economy gate','port regions','face index','special-item swap',
 'project settings','unsafe-edit rejection','wrong-source rejection','IPS/ROM roundtrip'],
 specialSwapPair:pair,outputFiles:downloads.map(x=>x.name),browserPreview:'BLOCKED by environment socket sandbox'},null,2));

