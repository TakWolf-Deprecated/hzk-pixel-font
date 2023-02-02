import logging
import os
import png

from configs import path_define
from utils import fs_util

logger = logging.getLogger('dump-asc-12')

font_file_path = os.path.join(path_define.fonts_dir, 'ASC12')
dump_dir = os.path.join(path_define.dump_dir, str(12), 'asc')
glyph_bytes_length = 8 * 12 // 8


def _iter_ascii(font_file, num_start, num_stop):
    count = 0
    for num in range(num_start, num_stop):
        c = chr(num)
        uni_hex_name = f'{num:04X}'
        glyph_offset = num * glyph_bytes_length
        font_file.seek(glyph_offset)
        glyph_bytes = font_file.read(glyph_bytes_length)
        bitmap = []
        for row_index in range(12):
            row = []
            byte = glyph_bytes[row_index]
            for bit_index in range(6):
                row.append(0)
                row.append(0)
                row.append(0)
                if 0b1 << (7 - bit_index) & byte:
                    row.append(255)
                else:
                    row.append(0)
            bitmap.append(row)
        image = png.from_array(bitmap, 'RGBA')
        image_file_path = os.path.join(dump_dir, f'{uni_hex_name}.png')
        image.save(image_file_path)
        logger.info(f'dump png 6*12px {c if c.isprintable() else " "} - {uni_hex_name}')
        count += 1
    return count


def run():
    fs_util.make_dirs_if_not_exists(dump_dir)
    with open(font_file_path, 'rb') as font_file:
        logger.info('--> dump asc 12')
        assert _iter_ascii(font_file, 32, 127) == 95
