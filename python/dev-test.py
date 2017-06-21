# silly proof of concept script 
# proves I have control of DJ-X11
# w1wra v0.27


import serial
import time

ser=serial.Serial('/dev/ttyUSB0' , 57600 , rtscts=True , timeout=1) 

print "Alinco DJ-X11T settings..."
print "(All frequencies in MHz) "
print " "
print "Frequncy of Main VFO."

ser.write('AL~FR0\r')

dj_main_out = ser.readlines()
out = dj_main_out.pop()
print  out

print "Frequncy of Sub VFO."
ser.write('AL~FR1\r')
dj_sub_out = ser.readlines() 
out = dj_sub_out.pop()
print out 

# try setting frequcy of sub vfo
print "Changing sub vfo."
ser.write('AL~FW10444000000\r')

time.sleep(3)

print "New Frequncy of Sub VFO."
ser.write('AL~FR1\r')
#time.sleep(3)
dj_sub_out = ser.readlines()
out = dj_sub_out.pop()
print out 


ser.close()
