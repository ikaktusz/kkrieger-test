import os
import sys
import time
import logging

from kkrieger_test.kkgame import KKriegerGame
from kkrieger_test.kkgame import KG_MENU, KG_RUN, KG_LOST
from kkrieger_test.utils import (
    PresentMon,
    PerfomanceTracker,
    start_cli,
    take_screenshot,
    press_key
    )


def main():
    start_cli()
    print('Test started.')

    kg = KKriegerGame()
    kg.start_game()
    pm = PresentMon(kg.process_name)
    pt = PerfomanceTracker()

    while True:
        kg.read_gamestate()
        if kg.GAME_STATE == KG_MENU or kg.GAME_STATE == KG_LOST:
            press_key('enter', 0.1)
            logging.info('Main menu')
        elif kg.GAME_STATE == KG_RUN:
            logging.info('Game runing')

            time.sleep(1)

            take_screenshot('start')
            # запуск снятия статистики
            pm.start()
            pt.start(kg.process.pid)
            press_key('W', 3)     
            take_screenshot('end')
            
            time.sleep(1)
            
            # остановка снятия статистики
            pm.stop()
            pt.stop()
            
            kg.exit_game()
            break
        else:
            logging.warn(f'Wrong gamemode: {kg.GAME_STATE}')
            continue
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
    