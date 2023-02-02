from configs.font_config import FontConfig
from configs.git_deploy_config import GitDeployConfig

font_configs = [
    FontConfig(
        px=12,
        box_origin_y_px=9,
        x_height_px=6,
        cap_height_px=8,
    ),
    FontConfig(
        px=16,
        box_origin_y_px=12,
        x_height_px=7,
        cap_height_px=10,
    ),
]

font_formats = ['otf', 'woff2', 'ttf']

git_deploy_configs = [GitDeployConfig(
    'git@github.com:TakWolf/hzk-pixel-font.git',
    'github',
    'gh-pages',
)]
