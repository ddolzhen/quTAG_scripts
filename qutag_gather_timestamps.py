# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 10:13:40 2020

@author: Denis

This script gathers data over exposure time (expTime) for several exposures (numExposures)
Files are saved under file_path + file_name + "_X.bin"

"""

# -*- coding: utf-8 -*-






import numpy as np
#import matplotlib as mpl
import matplotlib.pyplot as plt
import time
import QuTAG


devID = 1 # quTAG ID is 1
expTime = 60000 # in ms
numExposures = 70 #number of times to loop exposures

file_path = "E:/2021-02-03/hour_run_MZ/"  #Set path for files here
file_name = "Motorized_10sStep_60min"   #Prefix for the filenames
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

for i in range(numExposures):
    qutag.writeTimestamps(file_path+file_name +"_{}.bin".format(i),qutag.FILEFORMAT_BINARY) 
    time.sleep(expTime/1000)
    qutag.writeTimestamps('',qutag.FILEFORMAT_NONE)
    print(i)

print('Deinitializing quTag...')
qutag.deInitialize()
