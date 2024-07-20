import re
import shutil

from loguru import logger

from tools.configs import path_define


def update_docs():
    for file_dir, _, file_names in path_define.outputs_dir.walk():
        for file_name in file_names:
            if re.match(r'preview-.*px\.png', file_name) is None:
                continue
            path_from = file_dir.joinpath(file_name)
            path_to = path_define.docs_dir.joinpath(path_from.relative_to(path_define.outputs_dir))
            path_to.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path_from, path_to)
            logger.info("Copy file: '{}' -> '{}'", path_from, path_to)
