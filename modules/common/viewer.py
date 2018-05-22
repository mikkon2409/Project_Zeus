#!/usr/bin/env python3

from ev3dev.core import LargeMotor, Sensor
from time import sleep
import sys, os

##########################################################################
########################### MOTORS INITIALIZING ##########################
##########################################################################

left_mot    = LargeMotor('outB')
assert      left_mot.connected, "B Motor not connected"
left_mot.polarity = 'inversed'
left_mot.stop_action = 'brake'

right_mot   = LargeMotor('outC')
assert      right_mot.connected, "C Motor not connected"
right_mot.polarity = 'inversed'
right_mot.stop_action= 'brake'

mid_mot     = LargeMotor('outA')
assert      mid_mot.connected, "D Motor not connected"
mid_mot.polarity = 'inversed'
mid_mot.stop_action = 'brake'

##########################################################################
########################### SENSORS INITIALIZING #########################
##########################################################################

seeker      = Sensor(address='in1:i2c8', driver_name = 'ht-nxt-ir-seek-v2')
assert      seeker.connected, "Seeker not connected to IN1"
seeker.mode = 'AC-ALL'

compass     = Sensor(address='in2:i2c1', driver_name = 'ht-nxt-compass')
assert      compass.connected, "Compass not connected to IN2"
compass.mode= 'COMPASS'

light       = Sensor(address='in3', driver_name = 'lego-nxt-light')
assert      light.connected, "Light not connected to IN3"
light.mode  = 'REFLECT'

##################################################################
##################################################################
##################################################################

def Distance():
    seek_val=[]
    for i in range(seeker.num_values):
        seek_val.append(seeker.value(i))
    return -1 if seek_val[0]==0 else seek_val[1+seek_val[0]//2]

while True:
    seek=[]
    for i in range(seeker.num_values):
        seek.append(seeker.value(i))
    sys.stdout.write('SeekerDIS:'+str(Distance())+'\n')
    sys.stdout.write('Seeker :  '+str(seek)+'\n')
    sys.stdout.write('Compass : '+str(compass.value(0))+'\n')
    sys.stdout.write('Light :   '+str(light.value(0))+'\n')
#     sys.stdout.write('Sonar :   '+str(touch.value(0))+'\n')
    sys.stdout.write('Motor :   '+str(mid_mot.position)+'\n')
    sys.stdout.write('===============================================\n')
    sys.stdout.flush()
    seek.clear()
    sleep(0.3)
    os.system(['clear', 'cls'][os.name == os.sys.platform])
