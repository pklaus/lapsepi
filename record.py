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

def main():
    parser = argparse.ArgumentParser(description='Record movies with RPi camera module.')
    parser.add_argument('path', help='File path where for the video recording.')
    parser.add_argument('--duration', '-d', type=int, help='Duration of the video in seconds', default=-1)
    parser.add_argument('--resolution', '-r', help='Resolution of the images to capture', default='1920x1080')
    parser.add_argument('--framerate', '-f', type=int, help='Frames per second', default=30)
    parser.add_argument('--bitrate', '-b', type=int, help='Bitrate of encoded stream in Bit/s', default=10000000)
    parser.add_argument('--verbosity', '-v', type=str, help='Verbosity (choose from DEBUG, INFO, WARNING, ERROR).', default='')
    args = parser.parse_args()
    resolution = RESOLUTIONS.get(args.resolution)
    if not resolution:
        parser.error("Resolution should be one of " + ', '.join(list(RESOLUTIONS.keys())))
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=getattr(logging, args.verbosity, logging.WARNING))
    logging.info("Starting to record video for {} seconds.".format(args.duration))
    logging.info("The movie will be saved as {}.".format(args.path))
    try:
        camera = picamera.PiCamera()
        camera.resolution = resolution
        camera.framerate = args.framerate
        #camera.start_preview()
        camera.start_recording(args.path, quality=20, bitrate = args.bitrate)
        camera.wait_recording(args.duration)
        camera.stop_recording()
    except KeyboardInterrupt:
        logging.info("Ctrl-C pressed. Stopping...")
    finally:
        camera.close()

if __name__ == "__main__":
    main()

