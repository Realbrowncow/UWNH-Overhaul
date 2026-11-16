"""Show exact 8-frame NPC animation rows from supplied Snes9x town VRAM."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from inspect_snes9x_states import ROOT, STEM, blocks


def tile_bytes_to_indices(vram: bytes, pos: int):
    source = vram[pos:pos + 32]
    pixels = []
    for y in range(8):
        for x in range(8):
            b = 7 - x
            pixels.append(sum(((source[k + y * 2 + (16 if k > 1 else 0) - (2 if k > 1 else 0)] >> b) & 1) << k for k in range(4)))
    return pixels


def frame(state, t, palette=6):
    vram = state['VRA']
    ppu = state['PPU']
    im = Image.new('RGBA', (16, 16))
    for dy in range(2):
        for dx in range(2):
            tile = tile_bytes_to_indices(vram, 0x2000 + (t + dx + 16 * dy) * 32)
            for y in range(8):
                for x in range(8):
                    idx = tile[y * 8 + x]
                    if not idx:
                        continue
                    cgram_idx = 128 + 16 * palette + idx
                    rgb555 = int.from_bytes(ppu[0x40 + 2 * cgram_idx:0x42 + 2 * cgram_idx], 'big')
                    rgb = tuple(((rgb555 >> shift) & 31) * 255 // 31 for shift in (0, 5, 10))
                    im.putpixel((dx * 8 + x, dy * 8 + y), rgb + (255,))
    return im


def make(state_name, title, groups):
    state = blocks(ROOT / (STEM + '.' + state_name))
    fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
    small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
    cell_w, cell_h = 125, 176
    canvas = Image.new('RGB', (1110, 48 + len(groups) * cell_h), '#101d27')
    draw = ImageDraw.Draw(canvas)
    draw.text((20, 12), title, fill='white', font=fnt)
    for row, (caption, first, pal) in enumerate(groups):
        y = 45 + row * cell_h
        draw.text((12, y), caption, fill='#cfeafc', font=small)
        for i in range(8):
            x = 90 + i * cell_w
            im = frame(state, first + 2*i, pal).resize((96, 96), Image.Resampling.NEAREST)
            canvas.paste(im, (x, y + 29), im)
            draw.text((x + 32, y + 128), f'${first + 2*i:02X}', fill='#d0dded', font=small)
    out = Path(__file__).parent / 'state_artwork' / f'{state_name}_full_npc_direction_rows.png'
    canvas.save(out)
    print(out)


if __name__ == '__main__':
    make('000', 'African port — exact animation rows (page 1 VRAM)', [
        ('Spear-holder', 0x00, 6), ('Next NPC', 0x20, 6), ('Third NPC', 0x40, 6),
    ])
    make('001', 'Indian port — exact animation rows (page 1 VRAM)', [
        ('Headscarf', 0x00, 6), ('Woman', 0x20, 6), ('Next NPC', 0x40, 6),
    ])
