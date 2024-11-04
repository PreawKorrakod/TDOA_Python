import serial
import time
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication  
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
from sympy import symbols, Eq, sqrt, solve
import struct

COM_PORT = '/dev/ttyACM0'
BAUD_RATE = 1000000

Y_MIN, Y_MAX = 0, 3
mic1_data, mic2_data, mic3_data = [], [], []
MAX_DATA_POINTS = 200

v = 343

x1, y1 = 0.035, 0.025
x2, y2 = 0.21, 0.26
x3, y3 = 0.38, 0.025

class DataThread(QThread):
    data_signal = pyqtSignal(int, int, int)  

    def run(self):
        with serial.Serial(COM_PORT, BAUD_RATE, timeout=1) as ser:
            cursor = 0
            buffer = bytearray(34)
            data = bytearray(13)
            while True:
                while True:
                    if ser.in_waiting > 0:
                        byte_data = ser.read() 
                        buffer[cursor] = byte_data[0]

                        if cursor == 0 and buffer[cursor] != 35:  
                            break

                        # print(byte_data)


                        if (buffer[cursor - 16] == 35 and buffer[cursor - 15] == 102 and buffer[cursor - 1] == 13 and buffer[cursor] == 10): 

                            j = 14
                            for i in range(0, 13):
                                data[i] = buffer[cursor - j]
                                j -=1
                        
                            unpacked_data = struct.unpack('>BiiI', data)
                            mic1 = unpacked_data[1]
                            mic2 = unpacked_data[2]
                            mic3 = unpacked_data[3]
                            # print(unpacked_data)
                            self.data_signal.emit(mic1, mic2, mic3) 
                            cursor = 0
                            break
                        else:
                            cursor += 1  
                            if cursor >= 34: 
                                cursor = 0 
                  

class MainApp:
    def __init__(self):
        self.app = QApplication([])
        self.win = pg.GraphicsLayoutWidget(show=True, title="Real-Time Data Plot")
        self.win.resize(800, 600)
        self.win.setWindowTitle("Real-Time Mic Data")

        self.p1 = self.win.addPlot(title="Microphon:1")
        self.p1.setYRange(Y_MIN, Y_MAX)
        self.mic1_curve = self.p1.plot(pen='b')

        self.win.nextRow()
        self.p2 = self.win.addPlot(title="Microphon:2")
        self.p2.setYRange(Y_MIN, Y_MAX)
        self.mic2_curve = self.p2.plot(pen='g')

        self.win.nextRow()
        self.p3 = self.win.addPlot(title="Microphon:3")
        self.p3.setYRange(Y_MIN, Y_MAX)
        self.mic3_curve = self.p3.plot(pen='r')

        self.data_thread = DataThread()
        self.data_thread.data_signal.connect(self.update_data)
        self.data_thread.start()  
        self.st = 0
        self.t1 = 0
        self.t2 = 0
        self.t3 = 0
        self.debounce = False
        self.debounceTime = 0
        self.p1 = 0
        self.p2 = 0
        self.p3 = 0


    def calculatePosition(self, t:list):
        
        del_12 = (t[1] - t[0]) * 1e-6
        del_13 = (t[2] - t[0]) * 1e-6

        print(del_12, del_13)
        x, y = symbols('x y')


        eq1 = Eq(sqrt(x**2 + y**2) - sqrt((x - x2)**2 + (y - y2)**2), del_12)
        eq2 = Eq(sqrt(x**2 + y**2) - sqrt((x - x3)**2 + (y - y3)**2), del_13)

        solution = solve((eq1, eq2), (x,y))

        return solution
    

    def update_data(self, mic1, mic2, mic3):
        global mic1_data, mic2_data, mic3_data

        # print(mic1, mic2, mic3)

        if (mic1 != self.p1 and mic2 != self.p2 and mic3 != self.p3) and not self.debounce:
            t = [mic1, mic2, mic3]
            position = self.calculatePosition(t)
            print(position)
            
            # if len(position) == 2:
            #    print(position[0], position[1])
    
            self.debounce = True
            self.debounceTime = time.time()

        if self.debounce:
            if time.time() - self.debounceTime >= 0.5:
                self.p1 = mic1
                self.p2 = mic2
                self.p3 = mic3
                self.debounce = False
                print("reset.....")

def main():
    app = MainApp()
    app.app.exec_()  

if __name__ == "__main__":
    main()
