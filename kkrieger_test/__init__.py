import os
import sys
import json
import logging
import threading
import xml.etree.ElementTree as xml

import yaml
from yaml import Loader


with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=Loader)


class DxDiag:

    args_system = (
        'Time',
        'MachineName',
        'OperatingSystem',
        'SystemManufacturer',
        'SystemModel',
        'Processor',
        'Memory',
        'DirectXVersion',
        )
    args_display = (
        'CardName',
        'Manufacturer',
        'ChipType',
        'DisplayMemory',
        'SharedMemory',
        'DedicatedMemory'
        )
    
    def __init__(self):
        self.name = type(self).__name__
        self.output_path = os.path.join(cfg['output_path'], 'DxDiag.xml')
        self.output = {}

        thread = threading.Thread(target=self._run)
        thread.start()
    
    def _run(self):
        os.system(f'dxdiag /whql:off /x {self.output_path}')
        self._parse_sysinfo()

    def _parse_sysinfo(self):
        syst = {}
        disp = {}
        root = xml.parse(self.output_path).getroot()
        sysinfo = root.find('SystemInformation')
        display = root.find('DisplayDevices').find('DisplayDevice')

        for arg in self.args_system:
            syst[arg] = sysinfo.find(arg).text

        for arg in self.args_display:
            disp[arg] = display.find(arg).text

        self._write_json(syst, disp)
        os.remove(self.output_path)

    def _write_json(self, syst, disp):
        json_output = os.path.join(cfg['output_path'], 'DxDiag.json')
        self.output['System'] = syst
        self.output['Display'] = disp
        with open(json_output, 'w') as f:
            f.write(json.dumps(self.output, indent=4))
        logging.info(f'[{self.name}]: Write sysinfo to: {json_output}')


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
        DxDiag() # Write sysinfo to file.
        logging.info(f'Set game_path: {sys.argv[1]}')
        logging.info(f'Set output_path: {sys.argv[3]}')
        return

    print('Help:\nUsage example: python3 main.py game_path -o output_path')
    sys.exit(1)
        