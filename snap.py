#!/usr/bin/env python

import argparse
import time
import picamera
from datetime import datetime, timedelta
import os
import logging

# http://picamera.readthedocs.org/en/latest/fov.html#camera-modes
RESOLUTIONS = {
  '2592x1944': (2592, 1944),
  '1920x1080': (1920, 1080),
  '1296x972' : (1296,  972),
  '1296x730' : (1296,  730),
  '640x480'  : ( 640,  480),
}

def wait(until):
    # until should be a datetime
    diff = until - datetime.now()
    if diff.days < 0.0: return
    delay = max(0.0, diff.seconds + diff.microseconds / 1000000.)
    logging.debug("Sleeping for {:f} seconds".format(delay))
    time.sleep(delay)

def main():
    parser = argparse.ArgumentParser(description='Take snapshots with RPi camera module every x seconds.')
    parser.add_argument('path', help='Path where your images should be stored')
    parser.add_argument('--seconds', '-s', type=int, help='Capture image every X seconds', default=60)
    parser.add_argument('--resolution', '-r', help='Resolution of the images to capture', default='1296x972')
    parser.add_argument('--verbosity', '-v', type=str, help='Verbosity (choose from DEBUG, INFO, WARNING, ERROR).', default='')
    args = parser.parse_args()
    resolution = RESOLUTIONS.get(args.resolution)
    if not resolution:
        parser.error("Resolution should be one of " + ', '.join(list(RESOLUTIONS.keys())))
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=getattr(logging, args.verbosity, logging.WARNING))
    filename_template = os.path.join(args.path, 'img{timestamp:%Y-%m-%d-%H-%M-%S}.jpg')
    logging.info("Taking pictures every {} seconds.".format(args.seconds))
    logging.info("They will be stored as {}.".format(filename_template))
    try:
        camera = picamera.PiCamera()
        camera.resolution = resolution
        #camera.start_preview()
        wait((datetime.now() + timedelta(seconds=1)).replace(microsecond=0))
        until = (datetime.now() + timedelta(seconds=args.seconds)).replace(microsecond=0)
        for filename in camera.capture_continuous(filename_template):
            logging.info('Captured %s' % filename)
            wait(until)
            until = (datetime.now() + timedelta(seconds=args.seconds)).replace(microsecond=0)
    except KeyboardInterrupt:
        logging.info("Ctrl-C pressed. Stopping...")
    finally:
        camera.close()

if __name__ == "__main__":
    main()
