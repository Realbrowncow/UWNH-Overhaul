// New Horizons World, Ship & Fleet Studio Beta 5.9 · Original-ROM-to-Test54c upgrade.
// Only the verified 2 MiB US original is accepted; the cumulative IPS is hashed,
// applied locally, and checked against the exact Test54c target SHA-256.
const UW54Upgrade = (() => {
 const CLEAN_SHA='64bc4707f422661a66618088887e2363a5f896ea683c58984fffd96dd21ab5f0';
 const PATCH_SHA='b92debc2c64dc10a0570f6da9eca182565b35e13de2caeef125bf4b3eb149286';
 const TARGET_SHA='924ee53c49d125aa0cd23059d9bbfec42ede83cda50c36f6235431bb0db63a01';
 const CLEAN_LENGTH=0x200000, TARGET_LENGTH=0x400000;
 const PATCH_ID='test54c-retail-upgrade-ips';
 let active=false;

 function parseAndApplyIPS(clean, ips){
  if(ips.length<11 || String.fromCharCode(...ips.subarray(0,5))!=='PATCH')throw Error('Invalid IPS header.');
  const out=new Uint8Array(TARGET_LENGTH);
  out.set(clean);
  let p=5, records=0, eof=false;
  while(p<ips.length){
   if(p+3>ips.length)throw Error('Truncated IPS address.');
   if(ips[p]===69 && ips[p+1]===79 && ips[p+2]===70){p+=3;eof=true;break;}
   if(p+5>ips.length)throw Error('Truncated IPS record header.');
   const offset=ips[p]*65536 + ips[p+1]*256 + ips[p+2];
   const length=ips[p+3]*256 + ips[p+4];
   p+=5;
   if(length){
    if(offset+length>TARGET_LENGTH || p+length>ips.length)throw Error('IPS data record is outside the expected ROM or patch.');
    out.set(ips.subarray(p,p+length),offset);
    p+=length;
   }else{
    if(p+3>ips.length)throw Error('Truncated IPS RLE record.');
    const count=ips[p]*256 + ips[p+1], value=ips[p+2];
    p+=3;
    if(offset+count>TARGET_LENGTH)throw Error('IPS RLE record is outside the expected ROM.');
    out.fill(value,offset,offset+count);
   }
   records++;
   if(records>100000)throw Error('Too many IPS records.');
  }
  if(!eof)throw Error('IPS end marker missing.');
  // The original-to-Test54c patch explicitly expands the ROM from 2 to 4 MiB.
  if(p+3!==ips.length)throw Error('Unexpected IPS trailing bytes.');
  const finalLength=ips[p]*65536 + ips[p+1]*256 + ips[p+2];
  if(finalLength!==TARGET_LENGTH)throw Error('IPS does not declare a 4 MiB target.');
  return {out, records};
 }

 async function upgradeBytes(original){
  const clean=original instanceof Uint8Array ? original : new Uint8Array(original);
  if(clean.length!==CLEAN_LENGTH)throw Error('Choose the exact 2 MiB headerless US original. 512-byte headers, already-patched ROMs and other sizes are refused.');
  if(await uwSHA256(clean)!==CLEAN_SHA)throw Error('The ROM SHA-256 does not match the verified clean US original. No upgrade was made.');
  const patchTag=$(PATCH_ID);
  if(!patchTag || !patchTag.textContent.trim())throw Error('The cumulative Test54c IPS is missing from this editor.');
  const ips=base64ToBytes(patchTag.textContent.trim());
  if(await uwSHA256(ips)!==PATCH_SHA)throw Error('The embedded IPS hash is wrong. Upgrade aborted.');
  const {out,records}=parseAndApplyIPS(clean,ips);
  const targetHash=await uwSHA256(out);
  if(targetHash!==TARGET_SHA)throw Error('Upgraded ROM does not match the exact Test54c target hash. Nothing was saved.');
  return {rom:out, sha256:targetHash, records};
 }

 function setStatus(message, isError=false){
  const el=$('upgradeOriginalStatus');
  if(!el)return;
  el.textContent=message;
  el.style.borderLeftColor=isError?'#df8585':'#87bd89';
 }
 function setup(){
  const fileInput=$('upgradeOriginalFile'), button=$('upgradeOriginalButton');
  if(!fileInput || !button)throw Error('Original ROM upgrade panel not present.');
  fileInput.addEventListener('change',()=>{
   button.disabled=active || !fileInput.files || fileInput.files.length!==1;
   const f=fileInput.files&&fileInput.files[0];
   setStatus(f ? 'Ready to verify '+f.name+' ('+f.size.toLocaleString()+' bytes). No files have been modified.' : 'Select an original ROM to begin.');
  });
  button.addEventListener('click',async()=>{
   const selected=fileInput.files&&fileInput.files[0];
   if(active || !selected)return;
   active=true;button.disabled=true;
   try{
    setStatus('Verifying the selected clean ROM, applying the IPS and checking the final image locally…');
    const source=new Uint8Array(await selected.arrayBuffer());
    const result=await upgradeBytes(source);
    saveBlob(new Blob([result.rom],{type:'application/octet-stream'}),'UWNH_Test54c_from_Clean_US_Verified.smc');
    setStatus('PASS — verified original and embedded IPS.\nPASS — exact 4 MiB Test54c output.\nSHA-256: '+result.sha256+'\n'+result.records+' IPS records applied. Download requested; the original file is untouched.');
    notice('Verified Test54c ROM created. Please test it in your emulator.',false,9500);
   }catch(err){
    setStatus('Upgrade refused: '+err.message,true);
    notice('Original ROM upgrade refused: '+err.message,true,12000);
   }finally{active=false;button.disabled=!(fileInput.files&&fileInput.files.length===1);}
  });
 }
 return {setup,upgradeBytes,parseAndApplyIPS,identity:()=>({clean:CLEAN_SHA,ips:PATCH_SHA,target:TARGET_SHA})};
})();
UW54Upgrade.setup();
