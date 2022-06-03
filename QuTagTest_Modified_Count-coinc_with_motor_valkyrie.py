# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 10:13:40 2020

@author: Denis
"""

# -*- coding: utf-8 -*-
import numpy as np
import time
import QuTAG
import serial

#import os



#os.add_dll_directory("C:/Program Files (x86)/quTools/Daisy@quTAG/userlib/lib")

devID = 1 # quTAG ID is 1
expTime = 60000 # in ms
numExposures = 30#50 #number of times to loop exposures

numExposures_pause=5
file_path = "E:/QuantAstro/20220529/long/"
motorStepsPerExposure= 12
#initialize qutag
qutag = QuTAG.QuTAG()
devType = qutag.getDeviceType()
    
if (devType == qutag.DEVTYPE_QUTAG):
    print("found quTAG!")
else:
    print("no suitable device found - demo mode activated")
	
print("Device timebase:" + str(qutag.getTimebase()))



#set exposure time
qutag.setExposureTime(expTime)


qutag.setSignalConditioning(1, qutag.SIGNALCOND_MISC, True, 0.1)
qutag.setSignalConditioning(2, qutag.SIGNALCOND_MISC, True, 0.1)
qutag.setSignalConditioning(3, qutag.SIGNALCOND_MISC, True, 0.1)
qutag.setSignalConditioning(4, qutag.SIGNALCOND_MISC, True, 0.1)




    #stop writing Timestamps
qutag.writeTimestamps('',qutag.FILEFORMAT_NONE)

#Setup Serial Link
ser=serial.Serial('COM4',115200,timeout=5)

# Step 1. Move motor 2 forward 10 um at a time 

#With 1 exposure being 1 minute, this allows for 6 motor steps of 10 um each separated by 10 sec


#Currently 2.5 um a step, steps every second for 6 minutes

ser.write(b'setMotor 2\r\n')
for i in range(numExposures):
    qutag.writeTimestamps(file_path+"ArLamp_30min_sweep_2Lamps_{}.bin".format(i),qutag.FILEFORMAT_BINARY)
    
    for j in range(motorStepsPerExposure):  
        time.sleep(expTime/1000/motorStepsPerExposure)
        ser.write(b'steps -32\r\n')
    qutag.writeTimestamps('',qutag.FILEFORMAT_NONE)
    print("Step 1. file num:", i)
    
# Step 1.5  Wait for numExposures_pause exposures between stages    
for i in range (numExposures_pause):
    qutag.writeTimestamps(file_path+"ArLamp_30min_sweep_2Lamps_{}.bin".format(i+numExposures),qutag.FILEFORMAT_BINARY)
    time.sleep(expTime/1000)
    qutag.writeTimestamps('',qutag.FILEFORMAT_NONE)
    print("Pause after step 1. file num:", i+numExposures)


# Step 2. Same as step 1 but now with motor 1    
ser.write(b'setMotor 1\r\n')    
for i in range (numExposures):
    qutag.writeTimestamps(file_path+"ArLamp_30min_sweep_2Lamps_{}.bin".format(i+numExposures+numExposures_pause),qutag.FILEFORMAT_BINARY)
    
    for j in range(motorStepsPerExposure):  
        time.sleep(expTime/1000/motorStepsPerExposure)
        ser.write(b'steps -32\r\n')
    qutag.writeTimestamps('',qutag.FILEFORMAT_NONE)
    print("Step 2. file num:", i+numExposures+numExposures_pause)
    
# Step 2.5  Wait for numExposures_pause exposures after all the stages 
for i in range (numExposures_pause):
    qutag.writeTimestamps(file_path+"ArLamp_30min_sweep_2Lamps_{}.bin".format(i+numExposures*2+numExposures_pause),qutag.FILEFORMAT_BINARY)
    time.sleep(expTime/1000)
    qutag.writeTimestamps('',qutag.FILEFORMAT_NONE)
    print("Pause after step 2. file num:", i+numExposures*2+numExposures_pause)
    
    

#Step 3 Move Motors back

ser.write(b'setMotor 1\r\n')
time.sleep(1)
ser.write(b'steps 11520\r\n')

time.sleep(2)

ser.write(b'setMotor 2\r\n')
time.sleep(1)
ser.write(b'steps 11520\r\n')

ser.close()

print('Deinitializing quTag...')
qutag.deInitialize()