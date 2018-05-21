#!/usr/bin/env python3

import statistics as stat
from time import sleep
from ev3dev.ev3 import Button
from ev3dev.core import LargeMotor, Sensor

button = Button()
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

def Distance():
    seek_val=[]
    for i in range(seeker.num_values):
        seek_val.append(seeker.value(i))
    return -1 if seek_val[0]==0 else seek_val[1+seek_val[0]//2]

try:
    file=open('test.txt','w')
##############НАПРАВЛЕНИЕ ВРАЖЕСКИХ ВОРОТ№####################################   
    sleep(0.7)
    print('GATE')
    while not button.enter:
        continue
    file.write(str(compass.value(0))+'\n')#Записал НАПРАВЛЕНИЕ ВРАЖЕСКИХ ВОРОТ
    print('GATE WROTE')
##############ВРАТАРСКАЯ ЗОНА#################################################   
    sleep(0.7)
    print('GREEN')
    while not button.enter:
        continue
    file.write(str(light.value(0))+'\n')#записал ВРАТАРСКУЮ ЗОНУ
    print('GREEN WROTE'+str(light.value(0)))
##################ЛИНИЯ ВРАТАРСКОЙ ЗОНЫ#######################################    
    sleep(0.7)
    print('BLACK')
    while not button.enter:
        continue
    file.write(str(light.value(0))+'\n')#ЗАПИСАЛ ШТРАФНУЮ ЛИНИУ
    print('BLACK WROTE'+str(light.value(0)))
###################ДАЛЬНЕЕ ЗНАЧЕНИЕ МЯЧА###################################### 
    sleep(0.7)
    print('FAR')
    while not button.enter:
        continue
    seek=[]
    for i in range(200):
        seek.append(Distance())
        sleep(0.025)
    file.write(str(stat.mean(seek))+'\n')#ЗАПИСАЛ ДАЛЬНЕЕ ЗНАЧЕНИЕ МЯЧА
    print('FAR WROTE'+str(stat.mean(seek)))
#######################БЛИЖНЕЕ ЗНАЧЕНИЕ МЯЧА###################################
    sleep(0.7)
    print('NEAR')
    while not button.enter:
        continue
    seek=[]
    for i in range(200):
        seek.append(Distance())
        sleep(0.025)
    file.write(str(stat.mean(seek))+'\n')#ЗАПИСАЛ БЛИЖНЕЕ ЗНАЧЕНИЕ МЯЧА
    print('NEAR WROTE'+str(stat.mean(seek)))
######################КАЛИБРОВКА ОКОНЧЕНА#####################################   
    file.close()
except:
    file.close()