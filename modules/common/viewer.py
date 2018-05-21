#!/usr/bin/env python3

from ev3dev.core import LargeMotor, Sensor
from time import sleep
import sys, os

North=0

left_mot    = LargeMotor('outB')
left_mot.polarity = 'inversed'
left_mot.stop_action = 'brake'
right_mot   = LargeMotor('outC')
right_mot.polarity = 'inversed'
right_mot.stop_action= 'brake'
mid_mot     = LargeMotor('outA')
mid_mot.polarity = 'inversed'
mid_mot.stop_action = 'brake'

seeker      = Sensor(address='in1:i2c8', driver_name = 'ht-nxt-ir-seek-v2')
seeker.mode = 'AC-ALL'
compass     = Sensor(address='in2:i2c1', driver_name = 'ht-nxt-compass')
compass.mode= 'COMPASS'
light       = Sensor(address='in3', driver_name = 'lego-nxt-light')
light.mode  = 'REFLECT'
# touch       = TouchSensor('in4')
# touch.mode  = 'TOUCH'

assert left_mot.connected, "B Motor not connected"
assert right_mot.connected, "C Motor not connected"
assert mid_mot.connected, "D Motor not connected"

assert seeker.connected, "Seeker not connected"
assert compass.connected, "Compass not connected"
assert light.connected, "Light not connected"
# assert touch.connected, "Sonar net connected"

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
