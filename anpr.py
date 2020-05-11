#!/usr/bin/python3

import locale
locale.setlocale(locale.LC_ALL, 'C')
from openalpr import Alpr
from picamera import PiCamera

import json
import logging, sys
import time
import shutil


def main():
    # Setup logging
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    mainLogger = logging.getLogger('ANPR Capture')
    # We append to the log if it already exists, if not create the file
    fh = logging.FileHandler('ANPR_Capture_'+timestamp+'.log', mode='a+')
    # Set the log level going to the file
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    mainLogger.addHandler(fh)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    mainLogger.addHandler(ch)
    mainLogger.propagate = False

    # Initialise Alpr to be EU based, using Ireland as the region
    mainLogger.info('Initialising ALPR library')
    alpr = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
    alpr.set_default_region('ie')
    mainLogger.info('Initialising Camera')
    camera=PiCamera()
    mainLogger.info('Capturing initial image for calibration')
    camera.capture('/home/pi/ScriptStartup.jpg')

    snapshot = '/run/ANPR/latest.jpg'
    dataStore = '/run/ANPR/'
    # Declaring this outside of the loop initially
    captureTS = time.strftime("%Y%m%d-%H%M%S")


    try:
        while True:
            captureTS = time.strftime("%Y%m%d-%H%M%S")
            camera.capture(snapshot)
            mainLogger.debug('Image captured at %s' % captureTS)

            # Lets see what the analysis thinks
            analysis = alpr.recognize_file(snapshot)
            if len(analysis['results']) == 0:
                mainLogger.debug('No licence plates recognised')
            else:
                mainLogger.info('Plate: %s detected with confidence of: %s' % ( analysis['results'][0]['plate'], analysis['results'][0]['confidence'] ) )
                fName = dataStore + '/IMG_' + captureTS
                mainLogger.debug('Moving %s to %s' % (snapshot, fName) )
                shutil.move(snapshot, fName + '.jpg')
                with open(fName+'.json') as results: 
                    mainLogger.debug('Writing json outputs')
                    json.dumps(analysis, results, indent=4)
                mainLogger.info('Saving image and analysis')
            
            # Pause loop for 5 seconds
            time.sleep(5)
    except KeyboardInterrupt:
        mainLogger.info('Shutting down')
        alpr.unload()



                

if __name__ == "__main__":
    main()