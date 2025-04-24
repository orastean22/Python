# This is a sample Python script.
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from time import sleep

import bitstream
import datetime
import logging
import time
import pymeasure

#from pymeasure.instruments.siglent import SPD3303X
#from pymeasure.instruments.siglent import SDM3055
#from pymeasure.instruments.siglent import SDL1020X
#from pymeasure.instruments.siglent import SDG2042X
# from pymeasure.instruments.rigol import MSO5104
from pymeasure.instruments.rohdeschwarz import HMP4040
from pymeasure.instruments.tektronix import AFG3152C
# from pymeasure.instruments.lecroy import Lecroy_Waverunner
from pymeasure.experiment import Procedure, Results, Worker
from pymeasure.experiment import IntegerParameter, FloatParameter, Parameter
from pymeasure.log import log, console_log
#from pymeasure.instruments.rigol import M300


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
ch1 = logging.StreamHandler()
ch1.setLevel(logging.DEBUG)
ch1.setFormatter(CustomFormatter('%(asctime)s | %(name)10s | %(levelname)8s | %(filename)-10s:%(lineno)-8d '
                               '| %(message)-120s'))
log.addHandler(ch1)



class gettemp():
    def __init__(self):
        self.prev_val1 = None
        self.prev_val2 = None

    def gettemp(self):
        m300.init()
        time.sleep(1)
        m300.trigger()
        a = m300.fetch().split(',')
        if len(a) == 2:
            val1 = float(a[0])
            val2 = float(a[1])
            self.prev_val1 = val1
            self.prev_val2 = val2
            return val1, val2
        else:
            return self.prev_val1, self.prev_val2

class activity:
    def __init__(self):
        self.counter = 0
        self.counter_max = 4
        self.cycle_sym = ['-', '\\', '|', '/']
    def get(self):
        self.counter += 1
        if self.counter >= self.counter_max:
            self.counter = 0
        return f'[{self.cycle_sym[self.counter]}]'



if __name__ == '__main__':
    log.info('Started')
    '''m300 = M300('USB0::0x1AB1::0x0C80::MM3A252700282::INSTR')
    m300.reset()
    time.sleep(1)
    m300.abort()
    time.sleep(1)
    m300.config_temp('TC', 'K', '1','(@401,402)')
    m300.rout_scan('(@401:402)')
    m300.trigger_source('BUS')
    '''
    bs = bitstream.Bitstreamreader()
    doit_seconds = 1
    timeout_seconds = 5
    temp_meas_seconds = 1
    timestamp1 = datetime.datetime.now()
    timestamp1b = datetime.datetime.now()
    timestamp2 = datetime.datetime.now()
    timestamp2b = datetime.datetime.now()
    timestamp3 = datetime.datetime.now()
    temp_ldi = 0
    temp_igd = 0
    enable_ch1 = True
    enable_ch2 = False
    a=activity()
    t=gettemp()
    while True:
        if datetime.datetime.now() - timestamp3 > datetime.timedelta(seconds=temp_meas_seconds):
            #temp_ldi, temp_igd = t.gettemp()
            timestamp3 = datetime.datetime.now()

        if (telegram := bs.read_buffer('CH1')) and enable_ch1 is True:
            timestamp1b = datetime.datetime.now()
            if telegram.anyflag:
                log.warning(f'{a.get()} CH1: {telegram.flaglist} - {telegram.s_temp} - TEMP-LDI = {temp_ldi}, TEMP-IGD = {temp_igd}')
                timestamp1 = datetime.datetime.now()
            elif datetime.datetime.now() - timestamp1 > datetime.timedelta(seconds=doit_seconds):
                log.info(f'{a.get()} CH1: {telegram.flaglist} - {telegram.s_temp} - TEMP-LDI = {temp_ldi}, TEMP-IGD = {temp_igd}')
                timestamp1 = datetime.datetime.now()
        elif enable_ch1 is True:
            if datetime.datetime.now() - timestamp1b > datetime.timedelta(seconds=timeout_seconds):
                log.error(f'{a.get()} CH1: No Data - TEMP-LDI = {temp_ldi}, TEMP-IGD = {temp_igd}')
                timestamp1b = datetime.datetime.now()

        if (telegram := bs.read_buffer('CH2')) and enable_ch2 is True:
            timestamp2b = datetime.datetime.now()
            if telegram.anyflag:
                log.warning(f'{a.get()} CH2: {datetime.datetime.now().time()} - {telegram.flaglist} - {telegram.s_temp} - TEMP-LDI = {temp_ldi}, TEMP-IGD = {temp_igd}')
                timestamp2 = datetime.datetime.now()
            elif datetime.datetime.now() - timestamp2 > datetime.timedelta(seconds=doit_seconds):
                log.info(f'{a.get()} CH2: {telegram.flaglist} - {telegram.s_temp} - TEMP-LDI = {temp_ldi}, TEMP-IGD = {temp_igd}')
                timestamp2 = datetime.datetime.now()
        elif enable_ch2 is True:
            if datetime.datetime.now() - timestamp2b > datetime.timedelta(seconds=timeout_seconds):
                log.error(f'{a.get()} CH2: No Data - TEMP-LDI = {temp_ldi}, TEMP-IGD = {temp_igd}')
                timestamp2b = datetime.datetime.now()








