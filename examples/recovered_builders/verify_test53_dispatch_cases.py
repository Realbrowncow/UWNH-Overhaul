"""Static 65816 instruction-path smoke test for Test53's guarded dispatcher.

This checks the emitted machine bytes, branch targets, A-width transitions and
source/destination stack arguments. It is not a substitute for SNES gameplay.
"""

from pathlib import Path

ROM=Path(__file__).parent/'output53/UWNH_Test53_Rimbo_Spear_Asmira_IndianWoman_Walkers_EXPERIMENTAL_2026-11-16.smc'
CODE_PC=0x250140


def simulate(bank:int, offset:int, dest:int=0x2345):
    b=ROM.read_bytes()[CODE_PC:CODE_PC+45]
    dp={0x56:offset,0x58:bank,0x54:dest}
    a=0; wide=True; pc=0; zero=False; stack=[]
    for step in range(60):
        op=b[pc]
        if op==0xC2: # REP #imm
            if b[pc+1]&0x20:wide=True
            pc+=2
        elif op==0xE2: # SEP #imm
            if b[pc+1]&0x20:wide=False
            pc+=2
        elif op==0xA5: # LDA direct page
            value=dp.get(b[pc+1],0)
            a=value if wide else (a&0xff00)|(value&0xff)
            zero=(a& (0xffff if wide else 0xff))==0
            pc+=2
        elif op==0xC9: # CMP imm
            value=int.from_bytes(b[pc+1:pc+(3 if wide else 2)],'little')
            zero=(a& (0xffff if wide else 0xff))==value
            pc+=3 if wide else 2
        elif op==0xD0: # BNE relative
            disp=b[pc+1];disp=disp-256 if disp>=128 else disp
            pc+=2+(disp if not zero else 0)
        elif op==0x3B: # TSC; representative stack pointer
            a=0x1fff
            pc+=1
        elif op==0x85: # STA DP
            dp[b[pc+1]]=a& (0xffff if wide else 0xff)
            pc+=2
        elif op==0xA9: # LDA immediate
            n=2 if wide else 1
            value=int.from_bytes(b[pc+1:pc+1+n],'little')
            a=value if wide else (a&0xff00)|value
            pc+=1+n
        elif op==0x48: # PHA 16- or 8-bit
            stack.append(a & (0xffff if wide else 0xff))
            pc+=1
        elif op==0x5C: # JML absolute long
            target=int.from_bytes(b[pc+1:pc+4],'little')
            return {'bank':bank,'source':offset,'target':target,'a':a,
                    'wide':wide,'stack':stack,'dp':dp}
        else:
            raise AssertionError((step,pc,hex(op)))
    raise AssertionError('dispatcher never JMLed')


def main():
    # Exact Hans selected and no source-bank RAM mutation; two words pushed.
    hans=simulate(0xDC,0x5CB3)
    assert hans['target']==0xC0A0C2 and (hans['a']&255)==0xDB
    assert hans['stack']==[0xCBD6,0x2345] and not hans['wide']
    assert hans['dp'][0x58]==0xDC
    # Every non-Hans combination goes to the intact Test52 hook, which
    # already contains the user's gameplay-PASS Rimbo source rewrite.
    for bank,offset in ((0xDB,0xE5F2),(0xDB,0x5CB3),(0xDC,0xE5F2),
                        (0xDB,0x8D33),(0xDC,0x5CB4)):
        path=simulate(bank,offset)
        assert path['target']==0xE50100 and path['stack']==[],path
    rom=ROM.read_bytes()
    assert rom[0xA0C2:0xA0C8]==bytes.fromhex('20 4C A2 C2 20 60')
    assert rom[0xA0C8:0xA0D5]==bytes.fromhex('A5 54 48 A5 58 E2 20 20 4C A2 C2 20 60')
    print('PASS — Hans bank + source pointer selects Indian-woman packet only.')
    print('PASS — Direct JML/JSR trampoline preserves the original native stack layout.')
    print('PASS — Test52 fallback and C0:A0C8 continuation preserved.')


if __name__=='__main__':main()
