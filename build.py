import logging
import os
import shutil

from services import dump_asc_12, dump_asc_16, dump_hzk_16, dump_hzk_12, make_font

logging.basicConfig(level=logging.DEBUG)

outputs_dir = 'outputs/'


def main():
    if os.path.exists(outputs_dir):
        shutil.rmtree(outputs_dir)
    dump_asc_12.run()
    dump_asc_16.run()
    dump_hzk_12.run()
    dump_hzk_16.run()
    make_font.run()


if __name__ == '__main__':
    main()
