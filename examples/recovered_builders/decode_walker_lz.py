"""Read-only port of UWNHRando Compressor.decompress for packet investigation.

Provenance: user-provided UWNHRando-main.zip (UWNHRando.java, class Compressor).
The packet uses separate control bytes, interleaved literals and a 16-bit bit
reservoir for copy lengths/backward distances. This script never writes a ROM.
"""

from __future__ import annotations

from pathlib import Path
import sys


ROM = Path(__file__).parent / 'output50' / 'UWNH_Test50_Rimbo_Test5_Asmira_Face113_AllViews_EXPERIMENTAL_2026-11-15.smc'


def signed16(x: int) -> int:
    return (x & 65535) - (65536 if x & 32768 else 0)


class Decoder:
    def __init__(self, data: bytes, start: int, limit: int = 20000):
        self.rom = data
        self.src = start
        self.start = start
        self.limit = limit
        self.data = signed16(data[start] | data[start + 1] << 8)
        self.shifted = self.data
        self.src += 2
        self.bytes_left = 0
        self.x = 0
        self.pbits = 0
        self.dest = bytearray()
        self.commands = 0
        self.traces = []

    def table(self, at: int) -> int:
        return self.rom[at - 512]

    def mask(self, bits: int) -> int:
        at = 41685 - 512 + bits * 2
        return self.rom[at] | self.rom[at + 1] << 8

    def shift16(self, x: int) -> None:
        bits_to_shift = x // 2
        a = signed16(self.shifted << bits_to_shift)
        self.shifted = a
        if self.bytes_left < bits_to_shift:
            remaining = bits_to_shift - self.bytes_left
            a = signed16((self.data & self.mask(self.bytes_left)) << remaining)
            self.shifted = signed16(self.shifted | a)
            if (self.shifted & -4) != 508:
                self.data = signed16(self.rom[self.src] | self.rom[self.src + 1] << 8)
            self.src += 2
            self.bytes_left = 16
            bits_to_shift = remaining
        self.bytes_left -= bits_to_shift
        a = self.data >> self.bytes_left
        a &= self.mask(bits_to_shift)
        self.shifted = signed16(a | self.shifted)

    @staticmethod
    def xba(a: int) -> int:
        return signed16(((a & 255) << 8) | ((a >> 8) & 255))

    @staticmethod
    def rol(a: int, count: int, carry_in: bool) -> int:
        carry = 1 if carry_in else 0
        for _ in range(count):
            carry_out = (a & 32768) != 0
            a = signed16((a << 1) | carry)
            carry = 1 if carry_out else 0
        return a

    def decompress(self) -> tuple[bytes, int]:
        while len(self.dest) < self.limit:
            self.commands += 1
            self.x -= 1
            if self.x < 0:
                self.pbits = self.rom[self.src]
                self.src += 1
                self.x = 7
            saved_x = self.x
            copy_literal = bool(self.pbits & 128)
            self.pbits = (self.pbits << 1) & 255
            if copy_literal:
                self.dest.append(self.rom[self.src])
                self.src += 1
                continue

            a = self.shifted
            if a & 32768:
                amount = 1
            else:
                a = signed16(a >> 1)
                a = self.xba(a)
                y = a & 255
                if y != 0:
                    if y < 8:
                        a = self.xba(a)
                        shift_count = self.table(41711 + 127 + y) // 2
                        a = signed16(a >> shift_count)
                    else:
                        a = self.table(41711 + y)
                    amount = a
                    shift_count = self.table(41711 + 64 + y)
                    self.shift16(shift_count)
                    # Java's shift16 mutates the *field* `a`, not just shiftedData.
                    a = self.shifted
                else:
                    a = self.xba(a)
                    a = signed16(a >> 1) | 128
                    if a == 255:
                        return bytes(self.dest), self.src - self.start
                    amount = a
                    shift_count = self.table(41711 + 64 + y)
                    self.shift16(shift_count)
                    a = self.shifted

            a = signed16(a << 1)
            if 0 <= a < 24576:
                a = signed16(a << 1)
                a = self.xba(a)
                y = a & 255
                shift_group = y >> 4
                a = self.table(41711 + 135 + y)
                shift_count = self.table(41711 + 327 + shift_group)
            else:
                old_carry = a < 0
                a = signed16(a << 1)
                a = self.rol(a, 3, old_carry)
                y = a & 7
                a = (self.shifted & 4095) | 4096
                a >>= self.table(41711 + 336 + y) // 2
                shift_count = self.table(41711 + 341 + y)

            backward_distance = a + 1
            self.shift16(shift_count)
            self.traces.append((len(self.dest), self.src, amount + 1, backward_distance,
                                self.shifted & 65535))
            if backward_distance > len(self.dest) or amount < 0:
                raise ValueError(f'Invalid backref at src={self.src:#x}, '
                                 f'dst={len(self.dest):#x}: back={backward_distance} copy={amount+1}')
            source_index = len(self.dest) - backward_distance
            for _ in range(amount + 1):
                self.dest.append(self.dest[source_index])
                source_index += 1
                if len(self.dest) >= self.limit:
                    break
            self.x = saved_x
        raise ValueError(f'Decompression exceeded output limit {self.limit}, src={self.src:#x}')


if __name__ == '__main__':
    rom = ROM.read_bytes()
    for arg in sys.argv[1:] or ['0x1BE5F2','0x1BE5F1','0x1BE5F3']:
        start = int(arg, 0)
        try:
            decoded, n = Decoder(rom, start, limit=2048).decompress()
            print(f'start={start:#x} compressed={n} decompressed={len(decoded)} first={decoded[:48].hex()}')
        except Exception as exc:
            print(f'start={start:#x} {type(exc).__name__}: {exc}')
