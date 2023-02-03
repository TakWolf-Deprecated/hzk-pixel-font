from configs.dump_config import DumpConfig
from configs.font_config import FontConfig
from configs.git_deploy_config import GitDeployConfig

dump_configs = [
    DumpConfig(
        font_name='ASC12',
        font_type='asc',
        glyph_width=6,
        glyph_height=12,
    ),
    DumpConfig(
        font_name='ASC16',
        font_type='asc',
        glyph_width=8,
        glyph_height=16,
    ),
    DumpConfig(
        font_name='ASC48',
        font_type='asc',
        glyph_width=24,
        glyph_height=48,
    ),
    DumpConfig(
        font_name='HZK12',
        font_type='hzk',
        glyph_width=12,
        glyph_height=12,
    ),
    DumpConfig(
        font_name='HZK14',
        font_type='hzk',
        glyph_width=14,
        glyph_height=14,
    ),
    DumpConfig(
        font_name='HZK16',
        font_type='hzk',
        glyph_width=16,
        glyph_height=16,
    ),
    DumpConfig(
        font_name='HZK16F',
        font_type='hzk',
        glyph_width=16,
        glyph_height=16,
    ),
    DumpConfig(
        font_name='HZK16S',
        font_type='hzk',
        glyph_width=16,
        glyph_height=16,
    ),
    DumpConfig(
        font_name='HZK24F',
        font_type='hzk',
        glyph_width=24,
        glyph_height=24,
    ),
    DumpConfig(
        font_name='HZK24H',
        font_type='hzk',
        glyph_width=24,
        glyph_height=24,
    ),
    DumpConfig(
        font_name='HZK24K',
        font_type='hzk',
        glyph_width=24,
        glyph_height=24,
    ),
    DumpConfig(
        font_name='HZK24S',
        font_type='hzk',
        glyph_width=24,
        glyph_height=24,
    ),
    DumpConfig(
        font_name='HZK32',
        font_type='hzk',
        glyph_width=32,
        glyph_height=32,
    ),
    DumpConfig(
        font_name='HZK40',
        font_type='hzk',
        glyph_width=40,
        glyph_height=40,
    ),
    DumpConfig(
        font_name='HZK48',
        font_type='hzk',
        glyph_width=48,
        glyph_height=48,
    ),
]

font_configs = [
    FontConfig(
        px=12,
        box_origin_y_px=9,
        x_height_px=6,
        cap_height_px=8,
        source_names=['ASC12', 'HZK12'],
    ),
    FontConfig(
        px=16,
        box_origin_y_px=12,
        x_height_px=7,
        cap_height_px=10,
        source_names=['ASC16', 'HZK16'],
    ),
]

font_formats = ['otf', 'woff2', 'ttf']

git_deploy_configs = [GitDeployConfig(
    'git@github.com:TakWolf/hzk-pixel-font.git',
    'github',
    'gh-pages',
)]
