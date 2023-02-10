import logging
import os

from PIL import Image, ImageFont, ImageDraw

from configs import path_define
from utils import fs_util

logger = logging.getLogger('image-service')


def make_preview_image_file(font_config):
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    font = ImageFont.truetype(os.path.join(path_define.outputs_dir, f'{font_config.output_name}.woff2'), font_config.px)

    image = Image.new('RGBA', (font_config.px * 35, font_config.px * 11), background_color)
    draw = ImageDraw.Draw(image)
    draw.text((font_config.px, font_config.px), '汉字库像素字体 / HZK Pixel Font', fill=text_color, font=font)
    draw.text((font_config.px, font_config.px * 3), '我们每天度过的称之为日常的生活，其实是一个个奇迹的连续也说不定。', fill=text_color, font=font)
    draw.text((font_config.px, font_config.px * 5), 'THE QUICK BROWN FOX JUMPS OVER A LAZY DOG.', fill=text_color, font=font)
    draw.text((font_config.px, font_config.px * 7), 'the quick brown fox jumps over a lazy dog.', fill=text_color, font=font)
    draw.text((font_config.px, font_config.px * 9), '0123456789', fill=text_color, font=font)
    image = image.resize((image.width * 2, image.height * 2), Image.NEAREST)

    fs_util.make_dirs_if_not_exists(path_define.outputs_dir)
    image_file_path = os.path.join(path_define.outputs_dir, font_config.preview_image_file_name)
    image.save(image_file_path)
    logger.info(f'make {image_file_path}')
