import os
import sys
import time
import logging

import kkrieger_test
from kkrieger_test.kkgame import KKriegerGame
from kkrieger_test.kkgame import KG_MENU, KG_RUN, KG_LOST
from kkrieger_test import utils
from kkrieger_test.utils import PresentMon, PerfomanceTracker


def main():
    kkrieger_test.run()
    print('Test started.')

    kg = KKriegerGame()
    kg.start_game()
    pm = PresentMon(kg.process_name)
    pt = PerfomanceTracker()

    while True:
        kg.read_gamestate()
        if kg.GAME_STATE == KG_MENU or kg.GAME_STATE == KG_LOST:
            utils.press_key('enter')
            logging.info('[TEST] Main menu')

        elif kg.GAME_STATE == KG_RUN:
            logging.info('[TEST] Game runing')

            time.sleep(1)

            utils.screenshot('start')
            # запуск снятия статистики
            pm.start()
            pt.start(kg.process.pid)

            utils.press_key('W', press_sec=3)     
            utils.screenshot('end')
            
            utils.press_key('esc')
            time.sleep(2)
            
            # остановка снятия статистики
            pm.stop()
            pt.stop()
            
            kg.exit_game()
            break
        else:
            logging.warning(f'[TEST] Wrong gamemode: {kg.GAME_STATE}')
            break
        time.sleep(0.5)
        
    logging.info('Test finished!')
    print('Test finished!')


if __name__ == '__main__':
    import ctypes
    
    if os.name != 'nt':
        print('This script supports only Windows os.')
        sys.exit(1)
    elif ctypes.windll.shell32.IsUserAnAdmin() != 1:
        print('Run this script as andmin.')
        sys.exit(1)

    main()
    