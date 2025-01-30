from typing import Literal, get_args

from tools.configs.dump import DumpConfig
from tools.configs.font import FontConfig

version = '1.7.0'
version_time = '2025-01-30'

dump_configs = [
    DumpConfig(
        font_name='ASC12',
        font_type='asc',
        font_size=12,
    ),
    DumpConfig(
        font_name='ASC16',
        font_type='asc',
        font_size=16,
    ),
    DumpConfig(
        font_name='ASC48',
        font_type='asc',
        font_size=48,
    ),
    DumpConfig(
        font_name='HZK12',
        font_type='hzk',
        font_size=12,
    ),
    DumpConfig(
        font_name='HZK14',
        font_type='hzk',
        font_size=14,
    ),
    DumpConfig(
        font_name='HZK16',
        font_type='hzk',
        font_size=16,
    ),
    DumpConfig(
        font_name='HZK16F',
        font_type='hzk',
        font_size=16,
    ),
    DumpConfig(
        font_name='HZK16S',
        font_type='hzk',
        font_size=16,
    ),
    DumpConfig(
        font_name='HZK24F',
        font_type='hzk',
        font_size=24,
    ),
    DumpConfig(
        font_name='HZK24H',
        font_type='hzk',
        font_size=24,
    ),
    DumpConfig(
        font_name='HZK24K',
        font_type='hzk',
        font_size=24,
    ),
    DumpConfig(
        font_name='HZK24S',
        font_type='hzk',
        font_size=24,
    ),
    DumpConfig(
        font_name='HZK32',
        font_type='hzk',
        font_size=32,
    ),
    DumpConfig(
        font_name='HZK40',
        font_type='hzk',
        font_size=40,
    ),
    DumpConfig(
        font_name='HZK48',
        font_type='hzk',
        font_size=48,
    ),
]

font_configs = [
    FontConfig(
        font_size=12,
        ascent=9,
        descent=-3,
        x_height=6,
        cap_height=8,
        source_names=['ASC12', 'HZK12'],
    ),
    FontConfig(
        font_size=16,
        ascent=12,
        descent=-4,
        x_height=7,
        cap_height=10,
        source_names=['ASC16', 'HZK16'],
    ),
]

type FontFormat = Literal['otf', 'ttf', 'woff2', 'bdf', 'pcf']
font_formats = list[FontFormat](get_args(FontFormat.__value__))
