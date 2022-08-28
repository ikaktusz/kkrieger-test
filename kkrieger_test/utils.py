import os
import csv
import time
import glob
import logging
import statistics
import subprocess
import threading

from mss import mss
import keyboard
import psutil
from psutil import NoSuchProcess

from kkrieger_test import cfg


class PresentMon:

    def __init__(self, process_to_record):
        self.name = type(self).__name__
        self.exe_file = glob.glob('PresentMon-*.*.*.exe')
        self.PM_EXISTS = False

        if not self.exe_file:
            logging.warn(f'[{self.name}]: Cant find executable file, fps record not avalible!')
        else:
            self.output_path = cfg['output_path']
            self.out_file_name = cfg['presentmon']['output_file']
            self.output_pm = os.path.join(self.output_path, self.out_file_name)
            self.exe_path = os.path.join(os.getcwd(), self.exe_file[0])
            self.process_to_record = process_to_record.pid
            self.PM_EXISTS = True
            self.process = None # Main process.

    def start(self):
        if self.PM_EXISTS:
            cmd = [
                self.exe_path,
                '-no_top',
                '-output_file',
                self.output_pm,
                '-process_id',
                f'{self.process_to_record}'
            ]
            self.process = subprocess.Popen(cmd, shell=False)
            logging.info(f'[{self.name}]: recording started.')

    def stop(self):
        if self.PM_EXISTS:
            cmd = [
                self.exe_path,
                '-terminate_existing'
            ]
            subprocess.Popen(cmd, shell=False)
            self.process.communicate() # Wait untill PresentMon finishes.
            logging.info(f'[{self.name}]: recording stopped.')
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

        logging.info(f'[{self.name}]: write avg framerate to file: {out_file}')


class PerfomanceTracker:

    def __init__(self, process_to_record):
        self.name = type(self).__name__
        self.output_path = cfg['output_path']
        self.out_file_name = cfg['perfomance_tracker']['output_file']
        self.file_path = os.path.join(self.output_path, self.out_file_name)
        self.cpu_count = psutil.cpu_count()
        self.running = False
        self.pid = process_to_record.pid

    def _collect_data(self):
        with self.proc.oneshot():
            row = {
                'proc_name': self.proc.name(),
                'mem_usage': self.proc.memory_info().rss,
                'cpu_usage': self.proc.cpu_percent() / self.cpu_count,
                'threads_num': self.proc.num_threads(),
            }
        return row

    def _start(self):
        try:
            self.proc = psutil.Process(pid=self.pid)

            with open(self.file_path, 'w', newline='') as output:
                fieldnames = ['proc_name', 'mem_usage', 'cpu_usage', 'threads_num']
                writer = csv.DictWriter(
                    output,
                    delimiter=',',
                    fieldnames=fieldnames
                    )
                writer.writeheader()

                while self.running:
                    writer.writerow(self._collect_data())
                    time.sleep(0.05)

        except NoSuchProcess as err:
            logging.warning(err)
            self.running = False
            return

    def start(self):
        logging.info(f'[{self.name}]: started')
        self.running = True
        thread = threading.Thread(target=self._start)
        thread.start()

    def stop(self):
        if self.running:
            self.running = False
            logging.info(f'[{self.name}]: stoped')
            logging.info(f'[{self.name}]: write data to: {self.file_path}')


def screenshot(out_file_name):
    output_path = os.path.join(cfg['output_path'], 'screenshots')
    with mss() as sct:  
        file_path = os.path.join(output_path, out_file_name + '.png')
        sct.shot(output=file_path)
        logging.info(f'Screenshot saved: {file_path}')

def press_key(key, press_sec = 0.1):
    keyboard.press(key)
    time.sleep(press_sec)
    keyboard.release(key)