#!/usr/bin/env python3

#from ev3dev import *
import time
from ev3dev.core import LargeMotor, Sensor
from time import sleep

file=open('test.txt','r')
calibration=file.readlines()
file.close()
North   =int(calibration[0])
green   =int(calibration[1])
black   =int(calibration[2])
far     =float(calibration[3])
near    =float(calibration[4])

transition=(green+black)/2

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

def Reset_Motors():
    left_mot.reset()
    right_mot.reset()
    mid_mot.reset()

def clamp(val, minimum, maximum):
    if val>maximum:
        return maximum
    elif val<minimum:
        return minimum
    else:
        return val

def Light():
    return light.value(0)

def isBlack():
    return Light()<transition
 
def Set_Motors(left=0, right=0,stop_mode='brake'):
    left=left/100*1050
    right=right/100*1050
    if left!=0: 
        left_mot.run_forever(speed_sp = clamp(left,-left_mot.max_speed,left_mot.max_speed))
    else:
        left_mot.stop_action=stop_mode
        left_mot.stop()
    if right!=0:
        right_mot.run_forever(speed_sp = clamp(right,-right_mot.max_speed,right_mot.max_speed))
    else:
        right_mot.stop_action=stop_mode
        right_mot.stop()

def Set_Mid_Motor(mid = 0,stop_mode='brake'):
    mid=mid/100*1050
    if mid!=0:
        mid_mot.run_forever(speed_sp = clamp(mid,-mid_mot.max_speed, mid_mot.max_speed))
    else:
        mid_mot.stop_action=stop_mode
        mid_mot.stop()

def N():
    return (compass.value(0)-North+540)%360-180

def NormSeeker():
    if seeker.value(0)==0:
        return -1 
    else:
        return seeker.value(0)-5

def Distance():
    seek_val=[]
    for i in range(seeker.num_values):
        seek_val.append(seeker.value(i))
    return -1 if seek_val[0]==0 else seek_val[1+seek_val[0]//2]

def isFar():
    return Distance()<far

def isCatch():
    return Distance()>far and abs(NormSeeker())<2

# def Touch():
#     return touch.value(0)

def TurnSector():
    if N()>0:
        q=-1
    else:
        q=1
    Set_Motors(30*q, 30*(-q))
    while abs(N())>7:
        continue
    Set_Motors()
     
#def Bit():
#   mid_mot.run_to_rel_pos(70)
#  sleep(0.7)
# mid_mot.run_to_rel_pos(-70)
#sleep(0.7)

            
def Find(u):
    u=u*35
    Set_Motors(u,-u)

def Proportional_Reg(u,left_koeff=1,right_koeff=1):
    u=u*50
    left=(65+u)*left_koeff
    right=(65-u)*right_koeff
    Set_Motors(left,right)
    
# def GoBack():
#     TurnSector()
#     Set_Motors(-40, -40)
#     while not Touch() and not isBlack():
#         continue
#     Set_Motors(60, 60)
#     sleep(0.4)
#     Set_Motors()

try:
    print ("Programm started")
    while True:
        Set_Mid_Motor(100)
        if isFar() and not isCatch():
            Proportional_Reg(NormSeeker())
        else:
            if isCatch():
                while isCatch():
                    Proportional_Reg(N()/180*100)
                Proportional_Reg(NormSeeker()*0.5)
            
    print('Programm ended')
except :
    Reset_Motors()
    print(Exception.with_traceback())