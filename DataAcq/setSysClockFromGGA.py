import serial
import datetime
import os, sys
from datetime import date
import time


def setClockfromGGA(serialport, serialPort='/dev/ttyACM1', tryCount=100, sleepTimeMin=1):
    """this function will set the system clock from the NMEA GGA data streaming over the identified serial port.

    Args:
        tryCount: how many times it will try (default =100)
        sleepTimeMin: how long to wait between each try (default=1 min)
        serialPort: a string describin the serialPort on the device over which to expect the GGA                strings

    Returns:
        None
    """

    # first turn off the auto time sync function (it has nothing to time sync to)
    os.system("systemctl stop systemd-timesyncd.service")
    with serial.Serial(port=serialport, baudrate=115200, bytesize=8,
                       timeout=2, stopbits=serial.STOPBITS_ONE) as ser:

       for i in range(tryCount):
            line = ser.readline().decode('ascii', errors='replace')  # first read the line
            if line.startswith("$GNGGA"):
                try:
                    #first parse
                    timestr = datetime.datetime.strptime(line.split(',')[1], '%H%M%S.%f').time().strftime("%H:%M:%S.%f")
                    # set my rasp-pi clock to GGA string (assume correct day)
                    os.system(f"timedatectl set-time {timestr}")
                    print(f'System Time Changed to {timestr}')
                    break

                except:
                    print(f'failed {line}')
                    print(f'sleeping for {sleepTimeMin} minutes')
                    time.sleep(sleepTimeMin*60)

                    continue




if __name__ == "__main__":
    setClockfromGGA(serialPort)
