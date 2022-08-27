import os
import time
import logging
import subprocess

from ReadWriteMemory import ReadWriteMemory
from ReadWriteMemory import ReadWriteMemoryError
from kkrieger_test.utils import press_key

# Game states.
KG_RUN = 0
KG_PAUSED = 1 # unused
KG_MENU = 6
KG_LOST = 5
KG_CREDITS = 7 # unused

rwm = ReadWriteMemory()

class GameExeNotExist(Exception):
    def __init__(self, message):
        super().__init__(message)
        logging.warning(message)


class KKriegerGame:

    kkrieger_base = (0x7c0000)
    gm_buffer_pointer = (0x00398594)
    gm_off = [0x8, 0x1348, 0x4, 0x4, 0x1C]

    process_name = 'pno0001.exe'

    def __init__(self):
        self.GAME_STATE = None
        self.GAME_RUNNING = False

        self._path_to_exe = os.environ['GAME_PATH']
        if not os.path.exists(self._path_to_exe):
            raise GameExeNotExist(f'Cant find game exe on {self._path_to_exe}')

    def _wait_loading(self):
        while self.GAME_RUNNING:
            if self.GAME_STATE != KG_MENU:
                logging.info('Wait for main menu..')
                press_key('enter', 0.1)

                self.gm_pointer = self.process.get_pointer(
                    self.kkrieger_base + self.gm_buffer_pointer,
                    offsets=self.gm_off
                    )
                self.read_gamestate()

            elif self.GAME_STATE == KG_MENU:
                logging.info('Game loaded. Main menu')
                break
            time.sleep(1)

    def read_gamestate(self):
        self.GAME_STATE = self.process.read(self.gm_pointer)

    def start_game(self):
        subprocess.Popen(self._path_to_exe, shell=True, stdout=subprocess.DEVNULL)

        while True:
            logging.info('Waiting for process to start...')
            try:
                self.process = rwm.get_process_by_name(self.process_name)
                self.process.open()
            except ReadWriteMemoryError as err:
                logging.info(err)
                time.sleep(1)
            else:
                self.GAME_RUNNING = True
                logging.info('Process found!')
                break

        self._wait_loading()

    def exit_game(self):
        if self.GAME_RUNNING:
            logging.info('Exit game.')
            cmd = f'taskkill /f /im {self.process_name}'
            subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL)
            self.GAME_RUNNING = False
            logging.info('Game process killed.')
        else:
            logging.info('Game not running!')