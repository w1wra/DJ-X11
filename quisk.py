# This is a quisk_conf.py configuration file for DJ-X11.

# Place this file in your home directory and name it .quisk_conf.py
# The hardware file is defined here as well. 
# It's based on the AR8600 sample
# Feel free to use it ;)
# Balthus 2012
#

from quisk_hardware_model import Hardware as BaseHardware
import serial
import time
import signal

class Hardware(BaseHardware):
  def __init__(self, app, conf):
    BaseHardware.__init__(self, app, conf)
    print "Balthus:Init called"
    self.tty_name = '/dev/ttyUSB0'        # serial port name 
    self.serial = None            # the open serial port
    self.timer = 0.02            # time between  commands in seconds
    self.time0 = 0                # time of last  command
    self.serial_out = []        # send commands slowly
    self.vfo_frequency = 0

  def open(self):
    print "***Open called"
    self.serial = serial.Serial(port=self.tty_name, baudrate=57600,  parity=serial.PARITY_NONE, rtscts=1, timeout=0)
    self.SendDJX11('AL~SDRON\r')        #Set the IQ mode
    #set the step frequecy to 50hz
    t = BaseHardware.open(self)        # save the message
    self.tune=144000000
    self.vfo=144000000-10000
    return t

  def close(self):
    print "***close called"    
    BaseHardware.close(self)
    if self.serial:
      self.serial.write('AL~SDROF\r')
      time.sleep(1)            # wait for output to drain, but don't block
      self.serial.close()
      self.serial = None


  def ChangeFrequency(self, rx_freq, vfo_freq, source='', band='', event=None):
    print "Change frequency called :"+ str(rx_freq)+" "+str(vfo_freq)
    #fo_freq = (vfo_freq + 5000) / 10000 * 10000        # round frequency
    if vfo_freq != self.vfo_frequency and vfo_freq >= 100000:
      self.vfo_frequency = vfo_freq
      cmd='AL~FW%011d\r\r' % vfo_freq
      print "Sending cmd:" +cmd
      self.SendDJX11(cmd)
    return rx_freq, vfo_freq


  def SendDJX11(self, msg):    # Send commands, but not too fast
    if self.serial:
      if time.time() - self.time0 > self.timer:
        self.serial.write(msg)            # send message now
        self.time0 = time.time()
      else:
        self.serial_out.append(msg)        # send message later

  def HeartBeat(self):    # Called at about 10 Hz by the main
    BaseHardware.HeartBeat(self)
    if self.serial:
      chars = self.serial.read(1024)
      if chars:
        print chars
      if self.serial_out and time.time() - self.time0 > self.timer:
        self.serial.write(self.serial_out[0])
        self.time0 = time.time()
        del self.serial_out[0]


#useful to catch signal and make a thread dump
def dumpstacks(signal, frame):
    id2name = dict([(th.ident, th.name) for th in threading.enumerate()])
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""), threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename, lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    print "\n".join(code)

signal.signal(signal.SIGQUIT, dumpstacks)

# In ALSA, soundcards have these names.  The "hw" devices are the raw
# hardware devices, and should be used for soundcard capture.
#name_of_sound_capt = "hw:0"
#name_of_sound_capt = "hw:1"
#name_of_sound_capt = "plughw"
#name_of_sound_capt = "plughw:1"
#name_of_sound_capt = "default"

sample_rate = 48000                    # ADC hardware sample rate in Hertz
name_of_sound_capt = "hw:1"            # Name of soundcard capture hardware device.
name_of_sound_play = "default"        # Use the same device for play back
channel_i = 0                    # Soundcard index of in-phase channel:  0, 1, 2, ...
channel_q = 1                        # Soundcard index of quadrature channel:  0, 1, 2, ...

default_screen = 'WFall'
default_mode = 'FM'
persistent_state = True
invertSpectrum = 0
