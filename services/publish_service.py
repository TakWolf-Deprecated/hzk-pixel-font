import datetime
import logging
import os
import shutil

import git

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


def update_www():
    fs_util.delete_dir(path_define.www_dir)
    shutil.copytree(path_define.www_static_dir, path_define.www_dir)
    for font_config in configs.font_configs:
        _copy_file(f'{font_config.outputs_name}.woff2', path_define.outputs_dir, path_define.www_dir)


def deploy_www():
    repo = git.Repo.init(path_define.www_dir)
    repo.git.add(all=True)
    repo.git.commit(m=f'deployed at {datetime.datetime.now(datetime.UTC).isoformat()}')
    current_branch_name = repo.git.branch(show_current=True)
    for git_deploy_config in configs.git_deploy_configs:
        repo.git.remote('add', git_deploy_config.remote_name, git_deploy_config.url)
        repo.git.push(git_deploy_config.remote_name, f'{current_branch_name}:{git_deploy_config.branch_name}', '-f')
