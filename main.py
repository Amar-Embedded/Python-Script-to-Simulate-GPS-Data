import pynmea2 as p
import keyboard as k
import time
import sys
import argparse


def parse_file(pass_file):
    if args.debug:
        print("Inside the file")
    file = pass_file
    cnt = 1
    jason_format = {}
    flag = False
    for line in file:
        if k.is_pressed('q'):
            flag = True
            break
        signal = p.parse(line)
        if repr(signal).find("GGA") == 1:
            jason_format['count'] = cnt
            jason_format['app'] = 'group18'
            jason_format['timestamp'] = int(time.time())
            jason_format['latitude'] = f"{signal.latitude:.6f}"
            jason_format['longitude'] = f"{signal.longitude:.6f}"
            print(jason_format)
            cnt = cnt + 1
            previous_time = time.time()
            while time.time() - previous_time < args.wait:
                if k.is_pressed('q'):
                    flag = True
                    break
            if flag:
                break
    file.close()
    if args.debug:
        print("Closing File......")
        print("File Closed successfully")
    sys.exit()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--debug', type=int, default=0, help="to enable debug messages")
    ap.add_argument('-v', '--version', action='store_true', help="to get python version")
    ap.add_argument('-w', '--wait', type=int, default=1, help="waiting time between two signals to read")
    args = ap.parse_args()

    k.add_hotkey('q', lambda: sys.exit())

    if args.version:
        print(sys.version)
        exit()

    elif args.debug:
        try:
            f = open('trip.nmea', 'r')
            print('File Open Successfully')
            print('Reading the File...')
            parse_file(f)
            f.close()
            print('Closing the file gracefully')
            print('File closed Successfully')
        except FileNotFoundError as e:
            print(f"File 'trip.nmea' not found error: {e}")

    else:
        try:
            f = open('trip.nmea', 'r')
            parse_file(f)
            f.close()
        except FileNotFoundError as e:
            print(f"File 'trip.nmea' not found error: {e}")
