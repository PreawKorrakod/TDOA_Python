import serial
import time
import struct

COM_PORT = '/dev/ttyACM0'  
BAUD_RATE = 1000000



def main():
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


                    if (buffer[cursor - 16] == 35 and buffer[cursor - 15] == 102 and buffer[cursor - 1] == 13 and buffer[cursor] == 10): 

                        j = 14
                        for i in range(0, 13):
                            data[i] = buffer[cursor - j]
                            j -=1
                       
                        unpacked_data = struct.unpack('>BiiI', data)

                        
                        print(unpacked_data)
                        cursor = 0
                        break
                    else:
                        cursor += 1  
                        if cursor >= 34: 
                            cursor = 0

                

if __name__ == "__main__":
    main()
