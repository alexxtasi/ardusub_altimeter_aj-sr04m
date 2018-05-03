#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program reads distance values from AJ-SR04M ultrasonic sensor and sends to QGC using the Pymavlink module.
# Is intented to run on an ArduSub's Companion Computer (tested on Raspberry Pi 3 model B with the Companion Software installed).
#  - placed in /home/pi/altimeter/altimeter.py
#  - SONAR_MIN and SONAR_MAX variables set to 0 (depth hold mode)
#
# Copyright (C) 2018  Alex Tasikas <alextasikas@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
This program reads distance values from AJ-SR04M ultrasonic sensor and sends to QGC using the Pymavlink module.
Is intented to run on an ArduSub's Companion Computer (tested on Raspberry Pi 3 model B with the Companion Software installed).
    - placed in /home/pi/altimeter/altimeter.py
    - SONAR_MIN and SONAR_MAX variables set to 0 (depth hold mode)
"""

from pymavlink import mavutil
import time
import RPi.GPIO as GPIO

# set max and min sensor values in cm
# these are for AJ-SR04M sensor
SONAR_MIN = 0   # SONAR_MIN = 20
SONAR_MAX = 0   # SONAR_MAX = 800

# select GPIO pins to use
GPIO_TRIGGER = 23
GPIO_ECHO    = 24

def setup():
    # use the BCM GPIO numbering
    GPIO.setmode(GPIO.BCM)
    # set GPIO_TRIGGER to OUTPUT mode
    GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
    # set GPIO_ECHO to INPUT mode
    GPIO.setup(GPIO_ECHO,GPIO.IN)
    # DEBUG:
    print(setup.__name__ + " : GPIO set.")

def sonar():
    # distance measurements in cm
    # set GPIO_TRIGGER to LOW
    GPIO.output(GPIO_TRIGGER, False)
    # let the sensor settle for a while
    #print "Waiting For Sensor To Settle"
    time.sleep(0.5)     # time.sleep(2)
    # send 10 microsecond pulse to GPIO_TRIGGER
    GPIO.output(GPIO_TRIGGER, True) # GPIO_TRIGGER -> HIGH
    time.sleep(0.00001) # wait 10 microseconds
    GPIO.output(GPIO_TRIGGER, False) # GPIO_TRIGGER -> LOW
    # create variable start and give it current time
    start = time.time()
    # refresh start value until GPIO_ECHO goes HIGH, so until the wave is send
    while GPIO.input(GPIO_ECHO)==0:
        start = time.time()
    # assign the actual time to stop variable until GPIO_ECHO goes back from HIGH to LOW
    while GPIO.input(GPIO_ECHO)==1:
        stop = time.time()
    # time it took the wave to travel there and back
    measuredTime = stop - start
    # calculate the travel distance by multiplying the measured time by speed of sound
    distanceBothWays = measuredTime * 33112 # cm/s in 20 degrees Celsius
    # divide the distance by 2 to get the actual distance from sensor to obstacle
    distance = distanceBothWays / 2

    # TODO: extend code to "calibrate" distance calculatation (temperature ...)
    '''
        distance = pulse_duration * 17150        #Calculate distance
        distance = round(distance, 2)            #Round to two decimal points
        if distance > SONAR_MIN and distance < SONAR_MAX:     #Is distance within range
            print "Distance:",distance - 0.5,"cm"  #Distance with calibration
        else:
            print "Out Of Range"                   #display out of range
    '''

    # TODO: print messages to a log file ???
    # print the distance
    #print("Distance : {0:5.1f}cm".format(distance))

    return distance

def main():
    # TODO: function setup_mavlink() to set the mavlink parameters
    # Connect to the default listening port for
    # mavproxy on Blue Robotics companion computer
    # This endpoint is created with the
    # '--out udpin:localhost:9000' option with MAVProxy
    # ckeck in companion's http://192.168.2.2:2770/mavlink
    master = mavutil.mavlink_connection('udpout:localhost:9000')
    # Configure the autopilot to use mavlink rangefinder, the autopilot
    # will need to be rebooted after this to use the updated setting
    master.mav.param_set_send(
        1,
        1,
        "RNGFND_TYPE",
        10, # "MAVLink"
        mavutil.mavlink.MAV_PARAM_TYPE_INT8)

    min = SONAR_MIN # minimum valid measurement that the autopilot should use
    max = SONAR_MAX # maximum valid measurement that the autopilot should use
    type = mavutil.mavlink.MAV_DISTANCE_SENSOR_UNKNOWN
    id = 1
    orientation = mavutil.mavlink.MAV_SENSOR_ROTATION_PITCH_270 # downward facing
    covariance = 0

    # DEBUG:
    print(main.__name__ + " : MAVLink parameters set.")
    #print(main.__name__ + " : " + master)

    # TODO: why is that ??
    tstart = time.time()
    while True:
        time.sleep(0.5)
        # calculate distance
        distance = sonar()
        # TODO: send data to mavproxy
        master.mav.distance_sensor_send(
            (time.time() - tstart) * 1000,
            min,
            max,
            distance,
            type,
            id,
            orientation,
            covariance)


if __name__ == '__main__':
    # setup gpio
    setup()
    # run main forever
    try:
        main()
    except KeyboardInterrupt:
        # stop on Ctrl+C
        # DEBUG:
        print("Keyboard Interrupt!")
    except:
        # unexpected error
        # DEBUG:
        print("Unexpected Error!")
    finally:
        # Reset GPIO settings
        # DEBUG:
        print("GPIO cleanup ... exiting")
        GPIO.cleanup()
