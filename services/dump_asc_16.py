import logging
import os
import png

logger = logging.getLogger('dump-asc-16')

font_file_path = 'assets/hzk-fonts/ASC16'
outputs_dir = 'outputs/png/asc/16/'
asc_glyph_bytes_length = 8 * 16 // 8


def _iter_ascii(font_file, num_start, num_stop):
    count = 0
    for num in range(num_start, num_stop):
        c = chr(num)
        uni_hex_name = f'{num:04X}'
        asc_offset = num * asc_glyph_bytes_length
        font_file.seek(asc_offset)
        glyph_bytes = font_file.read(asc_glyph_bytes_length)
        bitmap = []
        for row_index in range(16):
            row = []
            byte = glyph_bytes[row_index]
            for bit_index in range(8):
                row.append(0)
                row.append(0)
                row.append(0)
                if 0b1 << (7 - bit_index) & byte:
                    row.append(255)
                else:
                    row.append(0)
            bitmap.append(row)
        image = png.from_array(bitmap, 'RGBA')
        image.save(f'{outputs_dir}{uni_hex_name}.png')
        logger.info(f'* gene png 8*16px {c if c.isprintable() else " "} - {uni_hex_name}')
        count += 1
    return count


def run():
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
    with open(font_file_path, 'rb') as font_file:
        logger.info('----> dump asc 16')
        assert _iter_ascii(font_file, 0, 256) == 256
