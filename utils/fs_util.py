import os
import shutil


def delete_dir(path: str):
    if os.path.exists(path):
        if not os.path.isdir(path):
            raise Exception(f"Path not a directory: '{path}'")
        shutil.rmtree(path)


def make_dirs(path: str):
    if os.path.exists(path):
        if not os.path.isdir(path):
            raise Exception(f"Path exists but not a directory: '{path}'")
    else:
        os.makedirs(path)
