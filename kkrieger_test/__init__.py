import os
import sys
import logging

import yaml
from yaml import Loader


with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=Loader)

def _logging_run():
    output_path = cfg['output_path']

    logging.basicConfig(
        format='%(asctime)s %(levelname)s:%(message)s',
        datefmt='%m/%d/%Y %H:%M:%S',
        filename=os.path.join(output_path, cfg['logger']['output_file']),
        filemode='w',
        encoding='utf-8',
        level=logging.DEBUG
        )
    logging.info('Start logging.')

def run():
    if len(sys.argv) == 4 and sys.argv[2] == '-o':
        cfg['game_path'] = sys.argv[1]
        cfg['output_path'] = sys.argv[3]
        if not os.path.isdir(sys.argv[3]):
            os.mkdir(sys.argv[3])
            os.mkdir(os.path.join(sys.argv[3], 'screenshots'))

        _logging_run()
        logging.info(f'Set game_path: {sys.argv[1]}')
        logging.info(f'Set output_path: {sys.argv[3]}')
        return

    print('Help:\nUsage example: python3 main.py game_path -o output_path')
    sys.exit(1)
        