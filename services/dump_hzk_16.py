import logging
import os
import png

from configs import path_define
from utils import gb2312_util, fs_util

font_name = 'HZK16'

logger = logging.getLogger(f'dump-{font_name}')

font_file_path = os.path.join(path_define.fonts_dir, font_name)
dump_dir = os.path.join(path_define.dump_dir, font_name)
glyph_bytes_length = int(16 * 16 / 8)


def _iter_gb2312(font_file, zone_start, zone_stop):
    count = 0
    for zone_1 in range(zone_start, zone_stop):
        for zone_2 in range(1, 95):
            try:
                c = gb2312_util.query_chr(zone_1, zone_2)
                uni_hex_name = f'{ord(c):04X}'
                glyph_offset = ((zone_1 - 1) * 94 + (zone_2 - 1)) * glyph_bytes_length
                font_file.seek(glyph_offset)
                glyph_bytes = font_file.read(glyph_bytes_length)
                bitmap = []
                for row_index in range(16):
                    row = []
                    for byte_index in range(2):
                        byte = glyph_bytes[row_index * 2 + byte_index]
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
                image_file_path = os.path.join(dump_dir, f'{uni_hex_name}.png')
                image.save(image_file_path)
                logger.info(f'dump png 16*16px {c} - {uni_hex_name}')
                count += 1
            except UnicodeDecodeError:
                pass
    return count


def run():
    fs_util.make_dirs_if_not_exists(dump_dir)
    with open(font_file_path, 'rb') as font_file:
        logger.info('--> dump hzk 16')
        assert _iter_gb2312(font_file, 1, 10) == gb2312_util.alphabet_other_count
        assert _iter_gb2312(font_file, 16, 56) == gb2312_util.alphabet_level_1_count
        assert _iter_gb2312(font_file, 56, 88) == gb2312_util.alphabet_level_2_count
