import logging

import configs
from configs import path_define
from services import dump_service
from utils import fs_util

logging.basicConfig(level=logging.DEBUG)


def main():
    fs_util.delete_dir(path_define.dump_dir)

    for dump_config in configs.dump_configs:
        dump_service.dump_font(dump_config)


if __name__ == '__main__':
    main()
