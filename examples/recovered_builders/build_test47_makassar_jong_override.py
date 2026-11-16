from pathlib import Path
import zipfile, hashlib, struct, json, csv
ROOT=Path('/mnt/data')
source_zip=ROOT/'UWNH_Test47_V8v4_25Ships_V4_64Fleets_416Start_JeparaJong_TEST_2026-11-15.zip'
source_name='UWNH_Test47_V8v4_25Ships_V4_64Fleets_416Start_JeparaJong_TEST_2026-11-15.smc'
output_name='UWNH_Test47_V8v4_V4_Makassar_Jong_Exclusive_CapitalFix_TEST_2026-11-15'
output_dir=ROOT/output_name
output_dir.mkdir(exist_ok=True)
sha=lambda x:hashlib.sha256(x).hexdigest()
with zipfile.ZipFile(source_zip) as z:
    src=z.read(source_name)
    prev_manifest=json.loads(z.read('STATIC_INTEGRITY_AUDIT.json'))
assert len(src)==4194304
assert sha(src)==prev_manifest['output_rom_sha256']=='61ca922362516e5593ee13e7ddb4056281412b359bcab3900d38c46f39232dd3'
assert int.from_bytes(src[0xffdc:0xffde],'little') ^ int.from_bytes(src[0xffde:0xffe0],'little') == 0xffff
assert (sum(src) & 65535)==int.from_bytes(src[0xffde:0xffe0],'little')
perm=0x219200
reg=0x08DA7F
pc_port_base=reg
j=33;m=77;jong=11
ja=perm+j*25+jong
ma=perm+m*25+jong
assert src[ja]==1 and src[ma]==0
assert src[reg+j*37+34]==src[reg+m*37+34]==7
assert [x for x in range(25) if src[perm+j*25+x]]==[2,11,12]
assert [x for x in range(25) if src[perm+m*25+x]]==[2,12]
assert struct.unpack_from('<H',src,0x219E00+11*2)[0]==950
assert struct.unpack_from('<H',src,reg+j*37+4)[0]==730
assert struct.unpack_from('<H',src,reg+m*37+4)[0]==450
rom=bytearray(src)
rom[ja]=0;rom[ma]=1
res=bytes(rom)
assert [x for x in range(25) if res[perm+j*25+x]]==[2,12]
assert [x for x in range(25) if res[perm+m*25+x]]==[2,11,12]
assert [i for i in range(100) if res[perm+i*25+jong]]==[77]
assert sum(src)==sum(res) # 1 ->0 and 0 ->1, exact byte-sum conservation
assert res[0xffdc:0xffe0]==src[0xffdc:0xffe0] # unchanged, valid ROM header checksums
assert sum(res)&65535==int.from_bytes(res[0xffde:0xffe0],'little')
changes=[i for i,(a,b) in enumerate(zip(src,res)) if a!=b]
assert changes==sorted([ja,ma])
ips=b'PATCH'+ja.to_bytes(3,'big')+b'\0\1\0'+ma.to_bytes(3,'big')+b'\0\1\1'+b'EOF'
# manual strict IPS reapply
out=bytearray(src);i=5
while ips[i:i+3]!=b'EOF':
    off=int.from_bytes(ips[i:i+3],'big'); ln=int.from_bytes(ips[i+3:i+5],'big');i+=5
    assert ln==1
    out[off:off+ln]=ips[i:i+ln];i+=ln
assert bytes(out)==res
# for integrity, digest large relevant blocks must match exactly
preserved={
'port_economy_and_stock_records_PC08DA7F_100x37':src[reg:reg+3700]==res[reg:reg+3700],
'25_ship_stats_PC08CE27_25x12':src[0x08CE27:0x08CE27+25*12]==res[0x08CE27:0x08CE27+25*12],
'25_industry_gates_PC219E00':src[0x219E00:0x219E00+50]==res[0x219E00:0x219E00+50],
'25_ship_prices_extended_PC3E8100':src[0x3E8100:0x3E8100+25*4]==res[0x3E8100:0x3E8100+25*4],
'63_npc_generation_rules_PC09EC4D':src[0x09EC4D:0x09EC4D+126]==res[0x09EC4D:0x09EC4D+126],
'64_npc_initial_fleets_PC089DB2':src[0x089DB2:0x089DB2+70*133]==res[0x089DB2:0x089DB2+70*133],
'rimbo_and_sultan_portraits_PC2BCB7':src[0x2BCB7:0x2BCB7+128*3]==res[0x2BCB7:0x2BCB7+128*3],
'jepara_and_makassar_shipyard_region':res[reg+j*37+34]==res[reg+m*37+34]==7,
'original_town_styles_palette_and_map':src[0xB353E:0xB353E+100]==res[0xB353E:0xB353E+100] and src[0xB35A7:0xB35A7+100]==res[0xB35A7:0xB35A7+100],
'all_other_shipbuilding_permissions': all(src[i]==res[i] for i in range(perm,perm+100*25) if i not in [ja,ma]),
'rom_checksum_and_complement_unchanged_and_valid':res[0xffdc:0xffe0]==src[0xffdc:0xffe0],
'rom_4MiB_no_header':len(res)==4194304,
'ips_exact_reconstruction':bytes(out)==res,
}
assert all(preserved.values())
manifest={
  'title':'Test47 corrective override: Jong exclusive to Makassar, not capital Jepara',
  'status':'STATIC INTEGRITY PASS; GAMEPLAY NOT YET TESTED',
  'user_override':'Makassar can build the Jong. Jepara does not. Capitals cannot accept investments.',
  'source_Test47_ROM_SHA256':sha(src),
  'output_Test47_ROM_SHA256':sha(res),
  'modified_bytes':2,
  'checksum_modified':False,
  'changes':[
    {'port':'Jepara','port_id':33,'ship':'Jong','ship_slot':11,'rom_pc':hex(ja),'old_permission':1,'new_permission':0},
    {'port':'Makassar','port_id':77,'ship':'Jong','ship_slot':11,'rom_pc':hex(ma),'old_permission':0,'new_permission':1},
  ],
  'shipyard':['Jepara ID33 remains H (7): Dhow + Lancaran only','Makassar ID77 remains H (7): Dhow + Lancaran + Jong'],
  'Industry_gate_Jong':950,
  'industry_start_Jepara':730,
  'industry_start_Makassar':450,
  'Makassar_industry_increase_needed':500,
  'capital_investment_rule':'Jepara is a capital and cannot accept investment: preserved, no changes to political/port-type flags',
  'Jong_authorized_ports_ids':[77],
  'preserved':preserved,
  'source_static_checks':'Inherited previous Test47 independently validated V8v4 stats, 64 NPC fleets, 416 ship positions and V4 generation rules; all their binary content preserved byte-identical',
  'download_zip':output_name+'.zip'
}
file=output_dir/(output_name+'.smc');file.write_bytes(res)
(output_dir/(output_name+'.ips')).write_bytes(ips)
(output_dir/'STATIC_INTEGRITY_AUDIT.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
with (output_dir/'SHIPYARD_CORRECTIONS.csv').open('w',newline='',encoding='utf8') as f:
    wr=csv.writer(f);wr.writerow(['Port ID','Port','Shipyard region','Allowed ships','Jong permission','Starting Industry','Jong gate','Investment status','Note'])
    wr.writerow([33,'Jepara','H','Dhow; Lancaran','NO',730,950,'Capital; cannot invest','Never offers Jong'])
    wr.writerow([77,'Makassar','H','Dhow; Lancaran; Jong','YES',450,950,'Investable','Jong available once Industry reaches 950'])
checklist=f'''# Test47 — Makassar-only Jong construction correction\n\n**Static PASS; gameplay NOT yet verified.** Use fresh SRAM/New Game for a meaningful test; do not load a saved old fleet state.\n\n## Corrected permissions\n- **Jepara** (port ID 33): capital, fixed starting Industry 730, Region H, **Dhow and Lancaran only**. No Jong under any Industry conditions. Capitals do not accept investment; this rule is unchanged.\n- **Makassar** (port ID 77): investable, starting Industry 450, Region H; Dhow and Lancaran, plus **Jong exclusive**. Jong still requires **Industry 950**, so it is initially locked. Invest 500 Industry points to meet gate; no immediate unlock without development.\n- No other port can construct Jong in ROM permission table.\n\n## Suggested quick checks\n1. Enter Jepara's shipyard: Dhow/Lancaran availability; **no Jong**. Test that the investment option for the capital is unavailable, if convenient.\n2. Enter Makassar shipyard at Industry450: Jong is correctly locked pending Industry950. If you use investment to raise Industry to950, Jong should then appear in New Ship construction.\n3. Check Rimbo's blue headwear, Sultan Trenggana's portrait and palace guard/ruler dialogue.\n4. Optionally inspect two V4 NPC fleet rosters and confirm their menus work without freezing.\n\n## Protection\nExactly two binary flag bytes changed from the preceding Test47 V8v4/V4 ROM; checksum remains valid without modification. No ship statistics, 63 rules, 416 startup ships, market/stock, portraits, town graphics, other shipyards, capitals or 100-port values changed.\n\nSource ROM SHA256: `{sha(src)}`\nNew ROM SHA256: `{sha(res)}`\n'''
(output_dir/'GAMEPLAY_CHECKLIST.md').write_text(checklist)
zip_path=ROOT/(output_name+'.zip')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(output_dir.iterdir()):
        if p.is_file(): z.write(p,arcname=p.name)
assert zipfile.ZipFile(zip_path).testzip() is None
print(json.dumps({'source_sha':sha(src),'new_sha':sha(res),'src_bytes':len(src),'changed_offsets':[hex(x) for x in changes], 'old_jepara':src[ja],'new_jepara':res[ja],'old_makassar':src[ma],'new_makassar':res[ma],'industry':[730,450], 'zip':str(zip_path),'audit':preserved},indent=2))
