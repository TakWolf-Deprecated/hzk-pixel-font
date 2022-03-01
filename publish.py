import logging
import os
import shutil
import time

import git

logging.basicConfig(level=logging.DEBUG)

outputs_dir = 'outputs/'
docs_dir = 'docs/'
releases_dir = 'releases/'
www_static_dir = 'assets/www-static/'
www_dir = 'www/'

git_url = 'git@github.com:TakWolf/hzk-pixel-font.git'
git_remote_name = 'origin'
git_branch_name = 'gh-pages'


def _copy_files(file_names, from_dir, to_dir):
    for file_name in file_names:
        shutil.copy(os.path.join(from_dir, file_name), os.path.join(to_dir, file_name))


def _publish_docs():
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
    _copy_files([
        'preview-12px.png',
        'preview-16px.png',
    ], outputs_dir, docs_dir)


def _publish_releases():
    if os.path.exists(releases_dir):
        shutil.rmtree(releases_dir)
    os.makedirs(releases_dir)
    _copy_files([
        'hzk-pixel-12px.otf',
        'hzk-pixel-12px.woff2',
        'hzk-pixel-12px.ttf',
        'hzk-pixel-16px.otf',
        'hzk-pixel-16px.woff2',
        'hzk-pixel-16px.ttf',
    ], outputs_dir, releases_dir)


def _publish_www():
    if os.path.exists(www_dir):
        shutil.rmtree(www_dir)
    shutil.copytree(www_static_dir, www_dir)
    _copy_files([
        'hzk-pixel-12px.woff2',
        'hzk-pixel-16px.woff2',
    ], outputs_dir, www_dir)

    repo = git.Repo.init(www_dir)
    repo.git.add(all=True)
    repo.git.commit(m=f'deployed at {time.strftime("%Y-%m-%d %H-%M-%S")}')
    repo.git.remote('add', git_remote_name, git_url)
    current_branch_name = repo.git.branch(show_current=True)
    repo.git.push(git_remote_name, f'{current_branch_name}:{git_branch_name}', '-f')


def main():
    _publish_docs()
    _publish_releases()
    _publish_www()


if __name__ == '__main__':
    main()
