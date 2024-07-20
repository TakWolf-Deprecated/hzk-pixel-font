import math
import os

from tools.configs import path_define


class DumpConfig:
    def __init__(self, font_name: str, font_type: str, glyph_width: int, glyph_height: int):
        self.font_name = font_name
        self.font_file_path = os.path.join(path_define.fonts_dir, font_name)
        self.dump_dir = os.path.join(path_define.dump_dir, font_name)
        self.font_type = font_type

        self.glyph_width = glyph_width
        self.glyph_height = glyph_height
        self.glyph_col_bytes_length = math.ceil(glyph_width / 8)
        self.glyph_bytes_length = self.glyph_col_bytes_length * glyph_height
        self.glyph_last_col_byte_bit_stop = glyph_width % 8
        if self.glyph_last_col_byte_bit_stop == 0:
            self.glyph_last_col_byte_bit_stop = 8
