#!/usr/bin/env python

import argparse
import time
import picamera
from datetime import datetime, timedelta
import os
import logging

def wait(seconds):
    # Calculate the delay to the start of the next hour
    next = (datetime.now() + timedelta(seconds=seconds)).replace(microsecond=0)
    diff = next - datetime.now()
    delay = diff.seconds + diff.microseconds / 1000000.
    logging.debug("Sleeping for {:f} seconds".format(delay))
    time.sleep(delay)

def main():
    parser = argparse.ArgumentParser(description='Take snapshots with RPi camera module every x seconds.')
    parser.add_argument('path', help='Path where your images should be stored')
    parser.add_argument('--seconds', '-s', type=int, help='Capture image every X seconds', default=60)
    parser.add_argument('--verbosity', '-v', type=str, help='Verbosity (choose from DEBUG, INFO, WARNING, ERROR).', default='')
    args = parser.parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=getattr(logging, args.verbosity, logging.WARNING))
    filename_template = os.path.join(args.path, 'img{timestamp:%Y-%m-%d-%H-%M-%S}.jpg')
    logging.info("Taking pictures every {} seconds.".format(args.seconds))
    logging.info("They will be stored as {}.".format(filename_template))
    try:
        with picamera.PiCamera() as camera:
            #camera.start_preview()
            wait(1)
            for filename in camera.capture_continuous(filename_template):
                logging.info('Captured %s' % filename)
                wait(args.seconds)
    except KeyboardInterrupt:
        logging.info("Ctrl-C pressed. Stopping...")

if __name__ == "__main__":
    main()
