import serial
import datetime
import os
import sys
from datetime import date

serialPort = '/dev/ttyACM1'

def setClockfromGGA(serialport):
    try:
        with serial.Serial(port=serialport, baudrate=115200, bytesize=8,
                           timeout=2, stopbits=serial.STOPBITS_ONE) as ser:
            while True:
                line = ser.readline().decode('ascii', errors='replace')
                if line.startswith("$GNGGA"):
                    try:
                        # Extract time from GGA sentence
                        gga_time_str = line.split(',')[1]
                        timestr = datetime.datetime.strptime(gga_time_str, '%H%M%S.%f').time().strftime("%H:%M:%S")
                        
                        # Update system time
                        os.system(f"timedatectl set-time {timestr}")
                        print(f'System Time Changed to {timestr}')
                        break  # Exit after setting the time
                    except ValueError as ve:
                        print(f"Error parsing time from GGA sentence: {ve}")
                    except Exception as e:
                        print(f"Unexpected error: {e}")
    except serial.SerialException as se:
        print(f"Error opening serial port: {se}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    setClockfromGGA(serialPort)
