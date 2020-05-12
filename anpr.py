#!/usr/bin/python3

# Hackey but needed to stop the underlying dependenices from bombing out
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
    camera.rotation = 90
    camera.capture('/home/pi/ScriptStartup.jpg')

    # Store the latest snapshot in a tmpfs / RAM FS to save wear on the SDCARD
    snapshot = '/run/ANPR/latest.jpg'
    # Eventually move this to a more permenent location, but again saving wear on the SDCARD
    dataStore = '/run/ANPR/'
    # Declaring this outside of the loop initially
    captureTS = time.strftime("%Y%m%d-%H%M%S")


    try:
        while True:
            # Refrest the timestamp
            captureTS = time.strftime("%Y%m%d-%H%M%S")
            # Take a snap
            camera.capture(snapshot)
            mainLogger.debug('Image captured at %s' % captureTS)

            # Lets see what the analysis thinks
            analysis = alpr.recognize_file(snapshot)
            if len(analysis['results']) == 0:
                # We didn't recognise any licence plates in the current snapshot
                mainLogger.debug('No licence plates recognised')
            else:
                # Maybe we got something
                mainLogger.info('Plate: %s detected with confidence of: %s' % ( analysis['results'][0]['plate'], analysis['results'][0]['confidence'] ) )
                fName = dataStore + 'IMG_' + captureTS

                # Since I don't trust this library to reliable detect licence plates yet, I'm using this as a chance to capture potential matches, as
                # well as the analysis, to improve the training of the model
                # So I save the jpg and the original analysis results
                #
                # Once it is reliable (>0.95), the goal would be to have it feed this information to other platforms to allow for analysis and alerting
                mainLogger.debug('Moving %s to %s' % (snapshot, fName) )
                shutil.move(snapshot, fName + '.jpg')
                with open(fName+'.json', "w+") as results: 
                    mainLogger.debug('Writing json outputs')
                    json.dump(analysis, results, indent=4)
                mainLogger.info('Saving image and analysis')
            
            # Pause loop for 5 seconds
            time.sleep(5)

    except KeyboardInterrupt:
        mainLogger.info('Shutting down')
        alpr.unload()



                

if __name__ == "__main__":
    main()
