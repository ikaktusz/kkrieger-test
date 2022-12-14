import os
import sys
import time
import logging

import kkrieger_test
from kkrieger_test import utils
from kkrieger_test.utils import PresentMon, PerfomanceTracker
from kkrieger_test.kkgame import KKriegerGame
from kkrieger_test.kkgame import KG_MENU, KG_RUN, KG_LOST


def main():
    kkrieger_test.run()
    print('Test started.')

    kg = KKriegerGame()
    pm = PresentMon(kg)
    pt = PerfomanceTracker(kg)

    while True:
        kg.read_gamestate()
        if kg.GAME_STATE == KG_MENU or kg.GAME_STATE == KG_LOST:
            utils.press_key('enter')
            logging.info('[TEST] Main menu')

        elif kg.GAME_STATE == KG_RUN:
            logging.info('[TEST] Game running')

            time.sleep(1)

            utils.screenshot('start')
            # Start recording statistics.
            pm.start()
            pt.start()

            utils.press_key('W', press_sec=3) # Duration of walking forward.
            utils.screenshot('end')
            
            utils.press_key('esc')
            time.sleep(2)
            
            # Stop recording statistics.
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
        print('Run this script as admin.')
        sys.exit(1)

    main()
    
