## ArduSub Altimeter using the AJ-SR04M Ultrasonic Ranging Module
This repo contains scripts and Fritzing sketch for using the AJ-SR04M Ultrasonic
Ranging Module on the ArduSub's Companion Computer, as an altimeter.

The ```altimeter.py``` program reads distance values from AJ-SR04M ultrasonic sensor and sends to QGC using the Pymavlink module.
Is intented to run on an ArduSub's Companion Computer (tested on Raspberry Pi 3 model B with the Companion Software installed).
* placed in companion's ```/home/pi/altimeter/``` directory
* ```SONAR_MIN``` and ```SONAR_MAX``` variables set to 0 (depth hold mode)

A service is created (systemd), so the altimeter provides continuous data to the QGC.

### Use
* copy altimeter.py in ```/home/pi/altimeter``` directory and make it executable:
```
chmod +x /home/pi/altimeter/altimeter.py
```
* copy altimeter.service unit file in ```/etc/systemd/system/``` directory and start the service:
```
sudo chown root:root /etc/systemd/system/altimeter.service
sudo chmod 644 /etc/systemd/system/altimeter.service
sudo systemctl daemon-reload
sudo systemctl enable altimeter.service
sudo systemctl start altimeter.service
```

### TODO
- [ ] use functions in python code
- [ ] perform GPIO cleanup when the service is stopped
- [x] MAVLink parameters RNGFND_MIN and RNGFND_MAX __should not__ be used for depth hold mode
- [ ] evaluate sensor's (AJ-SR04M) underwater accuracy (temperature ?)

<!-- info for the articles I used -->
## Based on
1. [Ultrasonic Distance Measurement Using Python – Part 1](https://www.raspberrypi-spy.co.uk/2012/12/ultrasonic-distance-measurement-using-python-part-1/#prettyPhoto)
1. [Raspberry Pi Computing: Ultrasonic Distance Measurement](https://leanpub.com/rpcultra/read#ultrasonic) by [Malcolm Maclean](https://twitter.com/d3noob)
1. [Measuring distance with JSN-SR04T and Raspberry](http://www.bambusekd.cz/dev/raspberry-measure-distance-JSN-SR04T)
1. [What is the difference between BOARD and BCM for GPIO pin numbering?](https://raspberrypi.stackexchange.com/questions/12966/what-is-the-difference-between-board-and-bcm-for-gpio-pin-numbering#12967)
1. [HC-SR04 Ultrasonic Ranging Sensor Module](https://www.elecrow.com/wiki/index.php?title=Ultrasonic_Ranging_Sensor_Module)
1. [AJ-SR04M Integration Ultrasonic Ranging Module](https://www.aliexpress.com/item/AJ-SR04M-Integration-Ultrasonic-Ranging-Module-Reversing-Radar-Waterproof-Ultrasonic-Square-Wave-TTL-Serial-interface-20cm/32822088448.html)
1. [Understanding Systemd Units and Unit Files](https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files)
1. [How to run a script as a service in Raspberry Pi - Raspbian Jessie](http://www.diegoacuna.me/how-to-run-a-script-as-a-service-in-raspberry-pi-raspbian-jessie/)
---
## ArduSub GitBook references
1. [Altimeters](https://www.ardusub.com/operators-manual/altimeters.html)
1. [Pymavlink](https://www.ardusub.com/developers/pymavlink.html)
1. [ArduSub Parameters](https://www.ardusub.com/operators-manual/full-parameter-list.html)
---
## General notes on MAVLink, Underwater Ranging and Acoustics
1. [Notes on Underwater Ranging](https://www.maxbotix.com/tutorials5/126-notes-on-underwater-ranging.htm)
1. [Design of a Low-Cost, Underwater Acoustic Modem for Short-Range Sensor Networks](https://cseweb.ucsd.edu/~kastner/papers/oceans10-low_cost_modem.pdf)
1. [MAVLink Step by Step](https://discuss.ardupilot.org/t/mavlink-step-by-step/9629) by [Pedro Albuquerque](https://discuss.ardupilot.org/u/pedro_albuquerque/summary) on Ardupilot forums
---
> License: ![GNU GPLv3 Logo](https://www.gnu.org/graphics/gplv3-88x31.png) [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)
