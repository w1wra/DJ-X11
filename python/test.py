import serial
import time

ser=serial.Serial('/dev/ttyUSB0' , 57600 , rtscts=True) 

print "Alinco DJ-X11T settings..."
print" "
print "Frequncy of Main VFO."

ser.write('AL~FR0\r')
dj_main_out = ser.read(20) 
print dj_main_out
print " "

time.sleep(1)

print "Frequncy of Sub VFO."
ser.write('AL~FR1\r')
dj_sub_out = ser.read(20) 
print dj_sub_out

# try setting frequcy of sub vfo
print "Changing sub vfo..."
ser.write('AL~FW10446000000\r')
time.sleep(1)

print "New Frequncy of Sub VFO."
ser.write('AL~FR1\r')
time.sleep(1)
dj_sub_out = ser.read(45)
print dj_sub_out

ser.close()
