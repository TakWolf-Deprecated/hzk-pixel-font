import logging
import os
import shutil

import configs
from configs import path_define
from utils import fs_util

logger = logging.getLogger('publish-service')


def _copy_file(file_name: str, from_dir: str, to_dir: str):
    from_path = os.path.join(from_dir, file_name)
    to_path = os.path.join(to_dir, file_name)
    shutil.copyfile(from_path, to_path)
    logger.info("Copy from '%s' to '%s'", from_path, to_path)


def update_docs():
    fs_util.make_dirs(path_define.docs_dir)
    for font_config in configs.font_configs:
        _copy_file(font_config.preview_image_file_name, path_define.outputs_dir, path_define.docs_dir)
