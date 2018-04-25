# Import mavutil
from pymavlink import mavutil
import time

# set max and min sensor values in cm
# these are for AJ-SR04M sensor
SONAR_MIN = 20
SONAR_MAX = 800

# Connect to the default listening port for
# mavproxy on Blue Robotics companion computer
# This endpoint is created with the
# '--out udpin:localhost:9000' option with MAVProxy
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

distance = 300 # You will need to supply the distance measurement in cm

type = mavutil.mavlink.MAV_DISTANCE_SENSOR_UNKNOWN
id = 1
orientation = mavutil.mavlink.MAV_SENSOR_ROTATION_PITCH_270 # downward facing
covariance = 0

tstart = time.time()
while True:
    time.sleep(0.5)
    master.mav.distance_sensor_send(
        (time.time() - tstart) * 1000,
        min,
        max,
        distance,
        type,
        id,
        orientation,
        covariance)
