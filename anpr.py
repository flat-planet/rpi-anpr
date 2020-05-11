#!/usr/bin/python3

import locale
locale.setlocale(locale.LC_ALL, 'C')
from openalpr import Alpr

import json

def main():
    alpr = Alpr("us", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
    results = alpr.recognize_file("/home/pi/ea7the.jpg")
    print(json.dumps(results, indent=4))

    alpr = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
    alpr.set_default_region('ie')
    results = alpr.recognize_file("/home/pi/IMG_20190423_163056.jpg")
    print(json.dumps(results, indent=4))
    

    alpr = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
    alpr.set_default_region('ie')
    results = alpr.recognize_file("/home/pi/IMG_20200511_191616.jpg")
    print(json.dumps(results, indent=4))




if __name__ == "__main__":
    main()