import serial
import datetime
import os
import sys
import logging
from datetime import date

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
                        logging.info(f'System Time Changed to {timestr}')
                        break  # Exit after setting the time
                    except ValueError:
                        logging.error("Failed to parse time from GGA sentence")
    except serial.SerialException as e:
        logging.error(f'Serial port error: {e}')
    except Exception as e:
        logging.error(f'Unexpected error: {e}')
