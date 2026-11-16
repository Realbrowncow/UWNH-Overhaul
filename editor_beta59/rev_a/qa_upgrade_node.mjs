#!/usr/bin/env node
// Independent Node VM regression: clean 2 MiB source -> exact Test54c 4 MiB ROM.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {Script, createContext} from 'node:vm';

if(process.argv.length!==5){
 console.error('Usage: node qa_upgrade_node.mjs editor.html clean_us.smc exact_test54c.smc');
 process.exit(2);
}
const [editorPath, sourcePath, targetPath]=process.argv.slice(2);
const html=readFileSync(editorPath,'utf8');
const orig=Uint8Array.from(readFileSync(sourcePath));
const target=Uint8Array.from(readFileSync(targetPath));
const hash=b=>createHash('sha256').update(b).digest('hex');
const match=html.match(/<script id="test54c-retail-upgrade-ips" type="text\/plain">([A-Za-z0-9+/=]+)<\/script>/);
assert(match,'IPS payload missing');
assert.equal(hash(Buffer.from(match[1],'base64')),'b92debc2c64dc10a0570f6da9eca182565b35e13de2caeef125bf4b3eb149286');
assert(html.includes('id="originalUpgradeSection"'),'Upgrade panel missing');
const moduleStart=html.indexOf('const UW54Upgrade = (() => {');
const moduleEnd=html.indexOf('UW54Upgrade.setup();',moduleStart);
assert(moduleStart>=0 && moduleEnd>=0,'Upgrade module missing');
const js=html.slice(moduleStart,moduleEnd);
const tags={'test54c-retail-upgrade-ips':{textContent:match[1]}};
const context=createContext({
 Uint8Array, Error, String, Number, console,
 base64ToBytes:b64=>Uint8Array.from(Buffer.from(b64,'base64')),
 uwSHA256:async bytes=>hash(bytes),
 $:id=>tags[id],
});
const script=new Script(js+'\nthis.__mod=UW54Upgrade;');
script.runInContext(context);
const mod=context.__mod;
assert.equal(orig.length,0x200000);
assert.equal(target.length,0x400000);
const cleanOriginalHash=hash(orig);
const result=await mod.upgradeBytes(orig);
assert.equal(result.rom.length,0x400000);
assert.equal(result.sha256,hash(target));
assert.deepEqual(Buffer.from(result.rom),Buffer.from(target),'Exact IPS replay must match Test54c byte-for-byte');
assert.equal(hash(orig),cleanOriginalHash,'Original input must not be altered');
assert(result.records>0,'IPS needs data records');

async function rejects(bytes, expected){
 let rejected=false;
 try{await mod.upgradeBytes(bytes);}catch(e){
  rejected=true;assert(String(e.message).includes(expected),`Unexpected error: ${e.message}`);
 }
 assert(rejected,`Input should reject: ${expected}`);
}
const tampered=orig.slice();tampered[12]^=0x01;
await rejects(tampered,'does not match');
await rejects(new Uint8Array(0x200200),'headerless');
await rejects(target,'headerless');
const patch=Uint8Array.from(Buffer.from(match[1],'base64'));
let refusedPatch=false;
try{mod.parseAndApplyIPS(orig,patch.subarray(0,patch.length-1));}catch(e){refusedPatch=true;}
assert(refusedPatch,'Truncated IPS must be rejected');

// Check every executable inline script parses (data scripts are excluded).
for(const m of html.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/g)){
 if(m[1].includes('type="text/plain"'))continue;
 new Script(m[2]);
}
console.log(JSON.stringify({status:'PASS',cleanSha256:hash(orig),ipsSha256:hash(patch),test54cSha256:result.sha256,records:result.records,sourceUntouched:true,wrongInputsRefused:true,inlineJsSyntax:'PASS'},null,2));
