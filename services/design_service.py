import logging
import os

from configs import path_define

logger = logging.getLogger('design-service')


def collect_glyph_files(font_config):
    alphabet = set()
    glyph_file_paths = {}
    glyphs_dirs = [
        os.path.join(path_define.dump_dir, str(font_config.px)),
        os.path.join(path_define.glyphs_dir, str(font_config.px)),
    ]
    for glyphs_dir in glyphs_dirs:
        if not os.path.isdir(glyphs_dir):
            continue
        for glyph_file_dir, _, glyph_file_names in os.walk(glyphs_dir):
            for glyph_file_name in glyph_file_names:
                if not glyph_file_name.endswith('.png'):
                    continue
                glyph_file_path = os.path.join(glyph_file_dir, glyph_file_name)
                if glyph_file_name == 'notdef.png':
                    glyph_file_paths['.notdef'] = glyph_file_path
                else:
                    uni_hex_name = glyph_file_name.removesuffix('.png').upper()
                    code_point = int(uni_hex_name, 16)
                    glyph_file_paths[code_point] = glyph_file_path
                    c = chr(code_point)
                    alphabet.add(c)
    alphabet = list(alphabet)
    alphabet.sort()
    return alphabet, glyph_file_paths
