"""this script when run will set the system clock from the NMEA GGA data streaming over the identified serial port"""
import serial
import datetime
import os, sys
from datetime import date

serialPort = '/dev/ttyACM1'

def setClockfromGGA(serialport):
    with serial.Serial(port=serialport, baudrate=115200, bytesize=8,
                       timeout=2, stopbits=serial.STOPBITS_ONE) as ser:
        while True:
            line = ser.readline().decode('ascii', errors='replace')  # first read the line

            if line.startswith("$GNGGA"):
                # set my pi clock to GGA string (assume correct day)
                timestr = datetime.datetime.strptime(line.split(',')[1], '%H%M%S.%f').time().strftime("%H:%M:%S")
                os.system(f"timedatectl set-time {timestr}")
                sys.exit()
                git s
if name == "__main__":
    setClockfromGGA(serialPort)