import logging
import os

from PIL import Image, ImageFont, ImageDraw

from tools.configs import FontConfig
from tools.configs import path_define
from tools.utils import fs_util

logger = logging.getLogger('image-service')


def make_preview_image_file(font_config: FontConfig):
    font = ImageFont.truetype(os.path.join(path_define.outputs_dir, f'{font_config.outputs_name}.woff2'), font_config.size)
    text_color = (0, 0, 0, 255)

    image = Image.new('RGBA', (font_config.size * 27, font_config.size * 11), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((font_config.size, font_config.size), '汉字库像素字体 / HZK Pixel Font', fill=text_color, font=font)
    draw.text((font_config.size, font_config.size * 3), '我们度过的每个平凡的日常，也许就是连续发生的奇迹。', fill=text_color, font=font)
    draw.text((font_config.size, font_config.size * 5), 'THE QUICK BROWN FOX JUMPS OVER A LAZY DOG.', fill=text_color, font=font)
    draw.text((font_config.size, font_config.size * 7), 'the quick brown fox jumps over a lazy dog.', fill=text_color, font=font)
    draw.text((font_config.size, font_config.size * 9), '0123456789', fill=text_color, font=font)
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.NEAREST)

    fs_util.make_dirs(path_define.outputs_dir)
    file_path = os.path.join(path_define.outputs_dir, font_config.preview_image_file_name)
    image.save(file_path)
    logger.info("Make preview image file: '%s'", file_path)
