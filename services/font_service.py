import logging
import math
import os

from pixel_font_builder import FontBuilder, Glyph, StyleName, SerifMode, WidthMode
from pixel_font_builder.opentype import Flavor

from configs import path_define, FontConfig
from utils import fs_util, glyph_util

logger = logging.getLogger('font-service')


def collect_glyph_files(font_config: FontConfig) -> tuple[dict[int, str], list[tuple[str, str]]]:
    root_dirs = [os.path.join(path_define.glyphs_dir, str(font_config.size))]
    for source_name in font_config.source_names:
        root_dirs.append(os.path.join(path_define.dump_dir, source_name))

    registry = {}
    for root_dir in reversed(root_dirs):
        for glyph_file_dir, glyph_file_name in fs_util.walk_files(root_dir):
            if not glyph_file_name.endswith('.png'):
                continue
            glyph_file_path = os.path.join(glyph_file_dir, glyph_file_name)
            if glyph_file_name == 'notdef.png':
                code_point = -1
            else:
                code_point = int(glyph_file_name.removesuffix('.png'), 16)
            registry[code_point] = glyph_file_path

    sequence = list(registry.keys())
    sequence.sort()

    character_mapping = {}
    glyph_file_infos = []
    for code_point in sequence:
        if code_point == -1:
            glyph_name = '.notdef'
        else:
            glyph_name = f'uni{code_point:04X}'
            character_mapping[code_point] = glyph_name
        glyph_file_infos.append((glyph_name, registry[code_point]))

    return character_mapping, glyph_file_infos


def _create_builder(font_config: FontConfig, character_mapping: dict[int, str], glyph_file_infos: list[tuple[str, str]]) -> FontBuilder:
    builder = FontBuilder()

    builder.metrics.size = font_config.size
    builder.metrics.ascent = font_config.ascent
    builder.metrics.descent = font_config.descent
    builder.metrics.x_height = font_config.x_height
    builder.metrics.cap_height = font_config.cap_height

    builder.meta_infos.version = FontConfig.VERSION
    builder.meta_infos.family_name = f'{FontConfig.FAMILY_NAME} {font_config.size}px'
    builder.meta_infos.style_name = StyleName.REGULAR
    builder.meta_infos.serif_mode = SerifMode.SANS_SERIF
    builder.meta_infos.width_mode = WidthMode.MONOSPACED
    builder.meta_infos.description = FontConfig.DESCRIPTION
    builder.meta_infos.vendor_url = FontConfig.VENDOR_URL

    builder.character_mapping.update(character_mapping)

    for glyph_name, glyph_file_path in glyph_file_infos:
        glyph_data, glyph_width, glyph_height = glyph_util.load_glyph_data_from_png(glyph_file_path)
        offset_y = math.floor((font_config.ascent + font_config.descent - glyph_height) / 2)
        builder.glyphs.append(Glyph(
            name=glyph_name,
            advance_width=glyph_width,
            offset=(0, offset_y),
            data=glyph_data,
        ))

    return builder


def make_font_files(font_config: FontConfig, character_mapping: dict[int, str], glyph_file_infos: list[tuple[str, str]]):
    fs_util.make_dirs(path_define.outputs_dir)

    builder = _create_builder(font_config, character_mapping, glyph_file_infos)

    otf_file_path = os.path.join(path_define.outputs_dir, f'{font_config.outputs_name}.otf')
    builder.save_otf(otf_file_path)
    logger.info("Make font file: '%s'", otf_file_path)

    woff2_file_path = os.path.join(path_define.outputs_dir, f'{font_config.outputs_name}.woff2')
    builder.save_otf(woff2_file_path, flavor=Flavor.WOFF2)
    logger.info("Make font file: '%s'", woff2_file_path)

    ttf_file_path = os.path.join(path_define.outputs_dir, f'{font_config.outputs_name}.ttf')
    builder.save_ttf(ttf_file_path)
    logger.info("Make font file: '%s'", ttf_file_path)

    bdf_file_path = os.path.join(path_define.outputs_dir, f'{font_config.outputs_name}.bdf')
    builder.save_bdf(bdf_file_path)
    logger.info("Make font file: '%s'", bdf_file_path)
