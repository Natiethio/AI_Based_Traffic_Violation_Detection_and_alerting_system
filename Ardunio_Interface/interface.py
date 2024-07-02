import serial
import time


arduino_port = "COM11"  
baud_rate = 9600 

ser = serial.Serial(arduino_port, baud_rate, timeout=1)

time.sleep(2)

print("Connected to Arduino port:", arduino_port)

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            print("Received from Arduino:", line)
except KeyboardInterrupt:
    print("Exiting program")

ser.close()
