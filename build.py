import logging

import configs
from configs import path_define
from services import dump_service, font_service, image_service
from utils import fs_util

logging.basicConfig(level=logging.DEBUG)


def main():
    fs_util.delete_dir(path_define.build_dir)

    for dump_config in configs.dump_configs:
        dump_service.dump_font(dump_config)

    for font_config in configs.font_configs:
        character_mapping, glyph_file_infos = font_service.collect_glyph_files(font_config)
        font_service.make_font_files(font_config, character_mapping, glyph_file_infos)
        image_service.make_preview_image_file(font_config)


if __name__ == '__main__':
    main()
