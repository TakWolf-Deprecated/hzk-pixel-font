from typing import Final


class FontConfig:
    VERSION: Final[str] = '1.4.0'
    FAMILY_NAME: Final[str] = 'HZK Pixel'
    DESCRIPTION: Final[str] = 'HZK pixel font.'
    VENDOR_URL: Final[str] = 'https://hzk-pixel-font.takwolf.com'

    def __init__(self, size: int, ascent: int, descent: int, x_height: int, cap_height: int, source_names: list[str]):
        self.size = size
        self.ascent = ascent
        self.descent = descent
        self.x_height = x_height
        self.cap_height = cap_height
        self.source_names = source_names

        self.outputs_name = f'{FontConfig.FAMILY_NAME.lower().replace(" ", "-")}-{size}px'
        self.preview_image_file_name = f'preview-{size}px.png'
