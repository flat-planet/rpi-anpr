# rpi-anpr
Running ANPR on an RPi

## Getting started
I'd recommend building the OpenANPR from source, as I had more then a few issues with the Raspbian packages, and compatibility issues with the package version vs. the pip version of the python bindings.


## Sample Output
```
2020-05-12 08:53:14,324 - ANPR Capture - INFO - Initialising ALPR library
2020-05-12 08:53:16,456 - ANPR Capture - INFO - Initialising Camera
2020-05-12 08:53:16,563 - ANPR Capture - INFO - Capturing initial image for calibration
2020-05-12 08:53:17,603 - ANPR Capture - DEBUG - Image captured at 20200512-085317
2020-05-12 08:53:18,218 - ANPR Capture - DEBUG - No licence plates recognised
2020-05-12 08:53:23,758 - ANPR Capture - DEBUG - Image captured at 20200512-085323
2020-05-12 08:53:24,575 - ANPR Capture - DEBUG - No licence plates recognised
...
2020-05-12 08:54:27,680 - ANPR Capture - INFO - Plate: 3DIJI detected with confidence of: 82.974052
2020-05-12 08:54:27,680 - ANPR Capture - DEBUG - Moving /run/ANPR/latest.jpg to /run/ANPR/IMG_20200512-085426
2020-05-12 08:54:27,681 - ANPR Capture - DEBUG - Writing json outputs
2020-05-12 08:54:27,682 - ANPR Capture - INFO - Saving image and analysis
...
2020-05-12 10:53:44,985 - ANPR Capture - INFO - Shutting down
```
## Inspired By
[ANPR CARP SPY](https://magpi.raspberrypi.org/articles/anpr-car-spy-raspberry-pi)
