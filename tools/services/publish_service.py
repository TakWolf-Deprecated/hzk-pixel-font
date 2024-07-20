import shutil
from pathlib import Path

from loguru import logger

from tools import configs
from tools.configs import path_define


def _copy_file(file_name: str, from_dir: Path, to_dir: Path):
    from_path = from_dir.joinpath(file_name)
    to_path = to_dir.joinpath(file_name)
    shutil.copyfile(from_path, to_path)
    logger.info("Copy from '{}' to '{}'", from_path, to_path)


def update_docs():
    path_define.docs_dir.mkdir(exist_ok=True)
    for font_config in configs.font_configs:
        _copy_file(font_config.preview_image_file_name, path_define.outputs_dir, path_define.docs_dir)
