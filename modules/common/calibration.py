#!/usr/bin/env python3

import statistics as stat
from time import sleep
from ev3dev.ev3 import Button
from ev3dev.core import LargeMotor, Sensor

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

button      = Button()
##################################################################
##################################################################
##################################################################

def Distance():
    seek_val=[]
    for i in range(seeker.num_values):
        seek_val.append(seeker.value(i))
    return -1 if seek_val[0]==0 else seek_val[1+seek_val[0]//2]

try:
    file=open('test.txt','w')
##############РќРђРџР РђР’Р›Р•РќР�Р• Р’Р РђР–Р•РЎРљР�РҐ Р’РћР РћРўв„–####################################   
    sleep(0.7)
    print('GATE')
    while not button.enter:
        continue
    file.write(str(compass.value(0))+'\n')#Р—Р°РїРёСЃР°Р» РќРђРџР РђР’Р›Р•РќР�Р• Р’Р РђР–Р•РЎРљР�РҐ Р’РћР РћРў
    print('GATE WROTE')
##############Р’Р РђРўРђР РЎРљРђРЇ Р—РћРќРђ#################################################   
    sleep(0.7)
    print('GREEN')
    while not button.enter:
        continue
    file.write(str(light.value(0))+'\n')#Р·Р°РїРёСЃР°Р» Р’Р РђРўРђР РЎРљРЈР® Р—РћРќРЈ
    print('GREEN WROTE'+str(light.value(0)))
##################Р›Р�РќР�РЇ Р’Р РђРўРђР РЎРљРћР™ Р—РћРќР«#######################################    
    sleep(0.7)
    print('BLACK')
    while not button.enter:
        continue
    file.write(str(light.value(0))+'\n')#Р—РђРџР�РЎРђР› РЁРўР РђР¤РќРЈР® Р›Р�РќР�РЈ
    print('BLACK WROTE'+str(light.value(0)))
###################Р”РђР›Р¬РќР•Р• Р—РќРђР§Р•РќР�Р• РњРЇР§Рђ###################################### 
    sleep(0.7)
    print('FAR')
    while not button.enter:
        continue
    seek=[]
    for i in range(200):
        seek.append(Distance())
        sleep(0.025)
    file.write(str(stat.mean(seek))+'\n')#Р—РђРџР�РЎРђР› Р”РђР›Р¬РќР•Р• Р—РќРђР§Р•РќР�Р• РњРЇР§Рђ
    print('FAR WROTE'+str(stat.mean(seek)))
#######################Р‘Р›Р�Р–РќР•Р• Р—РќРђР§Р•РќР�Р• РњРЇР§Рђ###################################
    sleep(0.7)
    print('NEAR')
    while not button.enter:
        continue
    seek=[]
    for i in range(200):
        seek.append(Distance())
        sleep(0.025)
    file.write(str(stat.mean(seek))+'\n')#Р—РђРџР�РЎРђР› Р‘Р›Р�Р–РќР•Р• Р—РќРђР§Р•РќР�Р• РњРЇР§Рђ
    print('NEAR WROTE'+str(stat.mean(seek)))
######################РљРђР›Р�Р‘Р РћР’РљРђ РћРљРћРќР§Р•РќРђ#####################################   
    file.close()
except:
    file.close()