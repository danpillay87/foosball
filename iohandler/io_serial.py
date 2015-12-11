import pygame
import time
import serial
import glob
from iohandler.io_base import IOBase

class IOSerial(IOBase):

    ser = None

    def reader_thread(self):
        while True:
            if not self.ser:
                self.open_serial()
            try:
                line = self.ser.readline().strip()
                pygame.fastevent.post(pygame.event.Event(pygame.USEREVENT, event_type='input_command', source='serial', value=line))
            except serial.SerialException:
                self.open_serial()

    def writer_thread(self):
        while True:
            if not self.ser:
                time.sleep(1)
                continue
            if len(self.write_queue):
                self.write_lock.acquire()
                line = self.write_queue.pop(0)
                self.write_lock.release()
                self.ser.write(line)
            else:
                time.sleep(1)

    def open_serial(self):
        while True:
            tty_list = glob.glob("/dev/ttyUSB[0-9]")
            if not len(tty_list):
                print("No ttyUSB device available")
                time.sleep(1)
            else:
                self.ser = serial.Serial(tty_list[0], 115200)
                return




    def writer_thread(self):
        fifo_file = "/tmp/foos-debug.out"
        try:
            os.mkfifo(fifo_file)
        except:
            pass
        while True:
            f = open(fifo_file, "a")
            if not f:
                print("Error opening fifo file " + fifo_file)
                time.sleep(5)
                continue
            while True:
                if len(self.write_queue):
                    self.write_lock.acquire()
                    line = self.write_queue.pop(0)
                    self.write_lock.release()
                    f.write(line)
                    f.flush()
                else:
                    time.sleep(0.1)
