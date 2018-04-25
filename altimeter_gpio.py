#!/usr/bin/python

# Import required Python libraries
import time               # library for time reading time
import RPi.GPIO as GPIO   # library to control Rpi GPIOs

def main():
    # We will be using the BCM GPIO numbering
    GPIO.setmode(GPIO.BCM)

    # Select which GPIOs you will use
    GPIO_TRIGGER = 23
    GPIO_ECHO    = 24

    # Set TRIGGER to OUTPUT mode
    GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
    # Set ECHO to INPUT mode
    GPIO.setup(GPIO_ECHO,GPIO.IN)

    '''
    while True:

        GPIO.output(TRIG, False)                 #Set TRIG as LOW
        print "Waiting For Sensor To Settle"
        time.sleep(2)
    '''

    # Set TRIGGER to LOW
    GPIO.output(GPIO_TRIGGER, False)

    # Let the sensor settle for a while
    time.sleep(0.5)

    # Send 10 microsecond pulse to TRIGGER
    GPIO.output(GPIO_TRIGGER, True) # set TRIGGER to HIGH
    time.sleep(0.00001) # wait 10 microseconds
    GPIO.output(GPIO_TRIGGER, False) # set TRIGGER back to LOW

    # Create variable start and give it current time
    start = time.time()
    # Refresh start value until the ECHO goes HIGH = until the wave is send
    while GPIO.input(GPIO_ECHO)==0:
        start = time.time()

    # Assign the actual time to stop variable until the ECHO goes back from HIGH to LOW
    while GPIO.input(GPIO_ECHO)==1:
        stop = time.time()

    # Calculate the time it took the wave to travel there and back
    measuredTime = stop - start
    # Calculate the travel distance by multiplying the measured time by speed of sound
    distanceBothWays = measuredTime * 33112 # cm/s in 20 degrees Celsius
    # Divide the distance by 2 to get the actual distance from sensor to obstacle
    distance = distanceBothWays / 2
    '''
        distance = pulse_duration * 17150        #Calculate distance
        distance = round(distance, 2)            #Round to two decimal points
        if distance > 20 and distance < 400:     #Is distance within range
            print "Distance:",distance - 0.5,"cm"  #Distance with calibration
        else:
            print "Out Of Range"                   #display out of range
    '''

    # Print the distance
    print("Distance : {0:5.1f}cm".format(distance))

    # Reset GPIO settings
    GPIO.cleanup()

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
