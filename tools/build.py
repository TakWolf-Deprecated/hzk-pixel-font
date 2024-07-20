import shutil

from tools import configs
from tools.configs import path_define
from tools.services import dump_service, font_service, image_service


def main():
    if path_define.build_dir.exists():
        shutil.rmtree(path_define.build_dir)

    for dump_config in configs.dump_configs:
        dump_service.dump_font(dump_config)

    for font_config in configs.font_configs:
        character_mapping, glyph_sequence = font_service.collect_glyph_files(font_config)
        font_service.make_fonts(font_config, character_mapping, glyph_sequence)
        image_service.make_preview_image(font_config)

    shutil.copy(path_define.www_static_dir.joinpath('index.html'), path_define.outputs_dir.joinpath('index.html'))


if __name__ == '__main__':
    main()
