import os
import csv
import sys
import time
import glob
import logging
import statistics
import subprocess
import threading

from mss import mss
import keyboard
import psutil


class PresentMon:

    def __init__(self, process_to_record, out_file_name='presentmon.csv'):
        self.exe_file = glob.glob('PresentMon-*.*.*.exe')
        self.PM_EXISTS = False

        if not self.exe_file:
            logging.warn('[PresentMon]: Cant find executable file, fps record not avalible!')
        else:
            self.output_path = os.environ['OUTPUT_PATH']
            self.out_file_name = out_file_name
            self.output_pm = os.path.join(self.output_path, self.out_file_name)

            self.exe_path = os.path.join(os.getcwd(), self.exe_file[0])
            self.process_to_record = process_to_record

            self.PM_EXISTS = True
            self.process = None # Main process.

    def start(self):
        if self.PM_EXISTS:
            cmd = [
                self.exe_path,
                '-no_top',
                '-output_file',
                self.output_pm,
                '-process_name',
                self.process_to_record
            ]
            self.process = subprocess.Popen(cmd, shell=False)
            logging.info('[PresentMon]: recording started.')

    def stop(self):
        if self.PM_EXISTS:
            cmd = [
                self.exe_path,
                '-terminate_existing'
            ]
            subprocess.Popen(cmd, shell=False)
            self.process.communicate() # Wait untill PresentMon finished.
            logging.info('[PresentMon]: recording stopped.')
            self._calc_fps()

    def _calc_fps(self):
        fps = []
        with open(self.output_pm, newline='') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                fps.append(1000 / float(row['msBetweenPresents']))

        # os.remove(self.output_pm) # Remove original csv file.

        avg_fps = statistics.fmean(fps)
        
        out_file = os.path.join(self.output_path, 'fps.txt')
        with open(out_file, 'w') as output:
            output.write(f'Avg fps of session: {avg_fps:.2f}')

        logging.info(f'[PresentMon]: write avg framerate to file: {out_file}')


class PerfomanceTracker:

    def __init__(self):
        self.output_path = os.environ['OUTPUT_PATH']
        self.out_file_name = 'stat.csv'
        self.file_path = os.path.join(self.output_path, self.out_file_name)

        self.cpu_count = psutil.cpu_count()
        self.running = False  

    def _collect_data(self):
        with self.proc.oneshot():
            row = {
                'proc_name': self.proc.name(),
                'mem_usage': self.proc.memory_info().rss, #from psutil._common import bytes2human
                'cpu_usage': self.proc.cpu_percent() / self.cpu_count,
                'threads_num': self.proc.num_threads(),
            }
        return row

    def _start(self, pid):
        with open(self.file_path, 'w', newline='') as output:
            fieldnames = ['proc_name', 'mem_usage', 'cpu_usage', 'threads_num']
            writer = csv.DictWriter(
                output,
                delimiter=',',
                fieldnames=fieldnames
                )
            writer.writeheader()
            self.proc = psutil.Process(pid=pid)
            while self.running:
                writer.writerow(self._collect_data())
                time.sleep(0.05)

    def start(self, pid):
        logging.info('[PerfomanceTracker]: started')
        self.running = True
        thread = threading.Thread(target=self._start, args=(pid,))
        thread.start()

    def stop(self):
        self.running = False
        logging.info('[PerfomanceTracker]: stoped')
        logging.info(f'[PerfomanceTracker]: write data to: {self.file_path}')


def _logging_run():
    output_path = os.environ['OUTPUT_PATH']

    logging.basicConfig(
        format='%(asctime)s %(levelname)s:%(message)s',
        datefmt='%m/%d/%Y %H:%M:%S',
        filename=os.path.join(output_path, 'log.log'),
        filemode='w',
        encoding='utf-8',
        level=logging.DEBUG
        )
    logging.info('Start logging.')


def start_cli():
    if len(sys.argv) == 4 and sys.argv[2] == '-o':
        os.environ['GAME_PATH'] = sys.argv[1]
        os.environ['OUTPUT_PATH'] = sys.argv[3]
        if not os.path.isdir(sys.argv[3]):
            os.mkdir(sys.argv[3])
            # Folder for screenshots.
            os.mkdir(os.path.join(sys.argv[3], 'screenshots'))

        # Start logging to file.
        _logging_run()
        logging.info(f'Set game_path: {sys.argv[1]}')
        logging.info(f'Set output_path: {sys.argv[3]}')
        return

    print('Help:\nUsage example: python3 main.py game_path -o output_path')
    sys.exit(1)

def take_screenshot(out_file_name):
    output_path = os.path.join(os.environ['OUTPUT_PATH'], 'screenshots')
    with mss() as sct:  
        file_path = os.path.join(output_path, out_file_name + '.png')
        sct.shot(output=file_path)
        logging.info(f'Screenshot saved: {file_path}')

def press_key(key, press_sec):
    keyboard.press(key)
    time.sleep(press_sec)
    keyboard.release(key)