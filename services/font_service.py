import logging
import os

from pixel_font_builder import FontBuilder, Glyph, StyleName, SerifMode, WidthMode
from pixel_font_builder.opentype import Flavor

from configs import path_define, FontConfig
from utils import fs_util, glyph_util

logger = logging.getLogger('font-service')


def collect_glyph_files(font_config: FontConfig) -> tuple[dict[int, str], dict[str, str]]:
    character_mapping = {}
    glyph_file_paths = {}

    glyphs_dirs = [os.path.join(path_define.glyphs_dir, str(font_config.size))]
    for source_name in font_config.source_names:
        glyphs_dirs.append(os.path.join(path_define.dump_dir, source_name))

    for glyphs_dir in reversed(glyphs_dirs):
        for glyph_file_dir, glyph_file_name in fs_util.walk_files(glyphs_dir):
            if not glyph_file_name.endswith('.png'):
                continue
            glyph_file_path = os.path.join(glyph_file_dir, glyph_file_name)
            if glyph_file_name == 'notdef.png':
                glyph_file_paths['.notdef'] = glyph_file_path
            else:
                code_point = int(glyph_file_name.removesuffix('.png'), 16)
                glyph_name = f'uni{code_point:04X}'
                character_mapping[code_point] = glyph_name
                glyph_file_paths[glyph_name] = glyph_file_path

    return character_mapping, glyph_file_paths


def _create_builder(font_config: FontConfig, character_mapping: dict[int, str], glyph_file_paths: dict[str, str]) -> FontBuilder:
    builder = FontBuilder(
        font_config.size,
        font_config.box_origin_y,
        font_config.box_origin_y - font_config.size,
        font_config.x_height,
        font_config.cap_height,
    )

    builder.character_mapping.update(character_mapping)

    for glyph_name, glyph_file_path in glyph_file_paths.items():
        glyph_data, glyph_width, glyph_height = glyph_util.load_glyph_data_from_png(glyph_file_path)
        offset_y = font_config.box_origin_y + (glyph_height - font_config.size) // 2 - glyph_height
        builder.add_glyph(Glyph(
            name=glyph_name,
            advance_width=glyph_width,
            offset=(0, offset_y),
            data=glyph_data,
        ))

    builder.meta_infos.version = FontConfig.VERSION
    builder.meta_infos.family_name = f'{FontConfig.FAMILY_NAME} {font_config.size}px'
    builder.meta_infos.style_name = StyleName.REGULAR
    builder.meta_infos.serif_mode = SerifMode.SANS_SERIF
    builder.meta_infos.width_mode = WidthMode.MONOSPACED
    builder.meta_infos.description = FontConfig.DESCRIPTION
    builder.meta_infos.vendor_url = FontConfig.VENDOR_URL

    return builder


def make_font_files(font_config: FontConfig, character_mapping: dict[int, str], glyph_file_paths: dict[str, str]):
    fs_util.make_dirs(path_define.outputs_dir)

    builder = _create_builder(font_config, character_mapping, glyph_file_paths)

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
