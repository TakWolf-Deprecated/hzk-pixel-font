import logging
import os

import png
from character_encoding_utils import gb2312
from character_encoding_utils.gb2312 import GB2312Exception

from utils import fs_util

logger = logging.getLogger('dump-service')


def _dump_glyph(dump_config, c, glyph_bytes):
    uni_hex_name = f'{ord(c):04X}'
    bitmap = []
    for row_index in range(dump_config.glyph_height):
        bitmap_row = []
        for col_index in range(dump_config.glyph_col_bytes_length):
            byte = glyph_bytes[row_index * dump_config.glyph_col_bytes_length + col_index]
            for bit_index in range(dump_config.glyph_last_col_byte_bit_stop if col_index == dump_config.glyph_col_bytes_length - 1 else 8):
                bitmap_row.append(0)
                bitmap_row.append(0)
                bitmap_row.append(0)
                if 0b1 << (7 - bit_index) & byte:
                    bitmap_row.append(255)
                else:
                    bitmap_row.append(0)
        bitmap.append(bitmap_row)
    image = png.from_array(bitmap, 'RGBA')
    image_file_path = os.path.join(dump_config.dump_dir, f'{uni_hex_name}.png')
    image.save(image_file_path)
    logger.info(f'dump {dump_config.font_name} {dump_config.glyph_width}*{dump_config.glyph_height} {c if c.isprintable() else " "} - {uni_hex_name}')


def _dump_font_ascii(dump_config, font_file, num_start, num_stop):
    for num in range(num_start, num_stop):
        c = chr(num)
        glyph_offset = num * dump_config.glyph_bytes_length
        font_file.seek(glyph_offset)
        glyph_bytes = font_file.read(dump_config.glyph_bytes_length)
        if len(glyph_bytes) == 0:
            break
        _dump_glyph(dump_config, c, glyph_bytes)


def _dump_font_gb2312(dump_config, font_file, zone_start, zone_stop):
    count = 0
    for row in range(zone_start, zone_stop):
        for col in range(1, 95):
            try:
                c = gb2312.query_chr(row, col)
                glyph_offset = ((row - 1) * 94 + (col - 1)) * dump_config.glyph_bytes_length
                font_file.seek(glyph_offset)
                glyph_bytes = font_file.read(dump_config.glyph_bytes_length)
                _dump_glyph(dump_config, c, glyph_bytes)
                count += 1
            except GB2312Exception:
                pass
    return count


def dump_font(dump_config):
    fs_util.make_dirs_if_not_exists(dump_config.dump_dir)

    with open(dump_config.font_file_path, 'rb') as font_file:
        if dump_config.font_type == 'asc':
            _dump_font_ascii(dump_config, font_file, 0, 256)
        elif dump_config.font_type == 'hzk':
            assert _dump_font_gb2312(dump_config, font_file, 1, 10) == gb2312.get_other_count()
            assert _dump_font_gb2312(dump_config, font_file, 16, 56) == gb2312.get_level_1_count()
            assert _dump_font_gb2312(dump_config, font_file, 56, 88) == gb2312.get_level_2_count()
        else:
            raise Exception(f"Unknown font type: '{dump_config.font_type}'")
