import logging
import os
from typing import IO

from character_encoding_utils import gb2312
from character_encoding_utils.gb2312 import GB2312Exception

from configs import DumpConfig
from utils import fs_util, glyph_util

logger = logging.getLogger('dump-service')


def _dump_glyph(dump_config: DumpConfig, c: str, glyph_bytes: bytes):
    glyph_data = []
    for row_index in range(dump_config.glyph_height):
        glyph_data_row = []
        for col_index in range(dump_config.glyph_col_bytes_length):
            b = glyph_bytes[row_index * dump_config.glyph_col_bytes_length + col_index]
            for bit_index in range(dump_config.glyph_last_col_byte_bit_stop if col_index == dump_config.glyph_col_bytes_length - 1 else 8):
                if 0b1 << (7 - bit_index) & b:
                    glyph_data_row.append(1)
                else:
                    glyph_data_row.append(0)
        glyph_data.append(glyph_data_row)
    hex_name = f'{ord(c): 04X}'
    file_path = os.path.join(dump_config.dump_dir, f'{hex_name}.png')
    glyph_util.save_glyph_data_to_png(glyph_data, file_path)
    logger.info('Dump %s %d*%d %s - %s', dump_config.font_name, dump_config.glyph_width, dump_config.glyph_height, c if c.isprintable() else ' ', hex_name)


def _dump_font_ascii(dump_config: DumpConfig, file: IO, num_start: int, num_end: int):
    for num in range(num_start, num_end + 1):
        c = chr(num)
        glyph_offset = num * dump_config.glyph_bytes_length
        file.seek(glyph_offset)
        glyph_bytes = file.read(dump_config.glyph_bytes_length)
        if len(glyph_bytes) == 0:
            break
        _dump_glyph(dump_config, c, glyph_bytes)


def _dump_font_gb2312(dump_config: DumpConfig, file: IO, row_start: int, row_end: int):
    count = 0
    for row in range(row_start, row_end + 1):
        for col in range(1, 94 + 1):
            try:
                c = gb2312.query_chr(row, col)
                glyph_offset = ((row - 1) * 94 + (col - 1)) * dump_config.glyph_bytes_length
                file.seek(glyph_offset)
                glyph_bytes = file.read(dump_config.glyph_bytes_length)
                _dump_glyph(dump_config, c, glyph_bytes)
                count += 1
            except GB2312Exception:
                pass
    return count


def dump_font(dump_config: DumpConfig):
    fs_util.make_dirs(dump_config.dump_dir)

    with open(dump_config.font_file_path, 'rb') as file:
        if dump_config.font_type == 'asc':
            _dump_font_ascii(dump_config, file, 0, 255)
        elif dump_config.font_type == 'hzk':
            assert _dump_font_gb2312(dump_config, file, 1, 9) == gb2312.get_other_count()
            assert _dump_font_gb2312(dump_config, file, 16, 55) == gb2312.get_level_1_count()
            assert _dump_font_gb2312(dump_config, file, 56, 87) == gb2312.get_level_2_count()
        else:
            raise Exception(f"Unknown font type: '{dump_config.font_type}'")
