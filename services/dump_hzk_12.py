import logging
import os
import png
from utils import gb2312_util

logger = logging.getLogger('dump-hzk-12')

font_file_path = 'assets/hzk-fonts/HZK12'
outputs_dir = 'outputs/png/hzk/12/'
hzk_glyph_bytes_length = 16 * 12 // 8


def _iter_gb2312(font_file, zone_start, zone_stop):
    count = 0
    for zone_1 in range(zone_start, zone_stop):
        for zone_2 in range(1, 95):
            try:
                c = gb2312_util.query_chr(zone_1, zone_2)
                uni_hex_name = f'{ord(c):04X}'
                hzk_offset = ((zone_1 - 1) * 94 + (zone_2 - 1)) * hzk_glyph_bytes_length
                font_file.seek(hzk_offset)
                glyph_bytes = font_file.read(hzk_glyph_bytes_length)
                bitmap = []
                for row_index in range(12):
                    row = []
                    for byte_index in range(2):
                        byte = glyph_bytes[row_index * 2 + byte_index]
                        for bit_index in range(8 if byte_index == 0 else 4):
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
                logger.info(f'* gene png 12*12px {c} - {uni_hex_name}')
                count += 1
            except UnicodeDecodeError:
                pass
    return count


def run():
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
    with open(font_file_path, 'rb') as font_file:
        logger.info('----> dump hzk 12')
        assert _iter_gb2312(font_file, 1, 10) == 682
        assert _iter_gb2312(font_file, 16, 56) == 3755
        assert _iter_gb2312(font_file, 56, 88) == 3008
