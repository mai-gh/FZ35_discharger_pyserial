#!/usr/bin/env python3

"""
XY-FZ35

https://www.aliexpress.com/item/FZ35-Adjust-Constant-Current-Electronic-Load-1-5v-25v-5A-35W-Battery-Tester-Discharge-Capacity-meter/32953589108.html
https://www.youtube.com/watch?v=RboBfJe4XXE
https://pyserial.readthedocs.io/en/latest/pyserial_api.html
https://learn.adafruit.com/li-ion-and-lipoly-batteries/voltages


Serial port Control (single-chip TTL level communication)
Baud Rate: 9600 bps
Data bits: 8
Stop bits: 1
Check bit: None
Flow control: None
Serial Port Commands
	

Command   | Info
---------------------
start     | Start upload (approx 1 second between updates) (fixed rate, dont know how to change)
stop      | Stop upload
on        | Turn on Load features
off       | Turn off Load features
read      | Read product parameter settings 

x.xxA     | Set load current
OVP:xx.x  | Over Voltage Protection     (Set maximum load voltage)
OCP:x.xx  | Over Current Protection     (Set maximum discharging current)
OPP:xx.xx | Over Power   Protection     (Set maximum discharging watts)
LVP:xx.x  | Low  Voltage Protection     (Set minimum voltage)
OAH:x.xxx | Over Ampere Hour Protection (Set maximum capacity) (Set to 0.000 to disable)
OHP:xx:xx | Set maximum discharge time  (Set to 00:00 to disable)

--------------------------------------------


default output for 'read': b'OVP:25.2, OCP:5.10, OPP:35.50, LVP:01.5,OAH:0.000,OHP:00:00\r\n'
output for 'start' (continious): 
"""


import serial
import time
from sys import getsizeof

with serial.Serial() as ser:
  ser.port = '/dev/ttyUSB0'
  ser.baudrate = 9600
  ser.bytesize = serial.EIGHTBITS
  ser.parity = serial.PARITY_NONE
  ser.stopbits = serial.STOPBITS_ONE
  ser.timeout = None
  ser.xonxoff = False
  ser.rtscts = False
  ser.dsrdtr = False
  ser.write_timeout = None
  ser.inter_byte_timeout = None
  ser.exclusive = None

  ser.open()

  ser.write(b'stop')
  print("Stopping data upload: {}".format(ser.readline().decode()), end="")

  ser.write(b'off')
  print("Turning off the load: {}".format(ser.readline().decode()), end="")

  ser.write(b'0.50A')
  print("Setting A: {}".format(ser.readline().decode()), end="")

  ser.write(b'OVP:04.3')
  print("Setting OVP: {}".format(ser.readline().decode()), end="")

  ser.write(b'OCP:0.60')
  print("Setting OCP: {}".format(ser.readline().decode()), end="")

  ser.write(b'OPP:05.00')
  print("Setting OPP: {}".format(ser.readline().decode()), end="")

  ser.write(b'LVP:03.2')
  print("Setting LVP: {}".format(ser.readline().decode()), end="")

  ser.write(b'OAH:0.000')
  print("Setting OAH: {}".format(ser.readline().decode()), end="")

  ser.write(b'OHP:00:00')
  print("Setting OHP: {}".format(ser.readline().decode()), end="")

  ser.write(b'read')
  print("Complete Setting Readout: {}".format(ser.readline().decode()), end="")



  ser.write(b'start')
  print("Starting data upload: {}".format(ser.readline().decode()), end="")

  ser.write(b'on')
  print("Turning ON the load: {}".format(ser.readline().decode()), end="")
  

  filename = "discharge_" + time.strftime("%Y%m%d-%H%M%S") + ".log"


  with open(filename, 'wb') as f1:

    spinner = "|"
    while True:
      time.sleep(1)
      line = ser.read(ser.inWaiting())
      f1.write(line)
      f1.flush()
      if getsizeof(line) == 61:
        print("   " + spinner + "  " + line.decode().rstrip(), end="\r")
      elif line.decode().rstrip() == 'LVP':         
        print()
        print()
        print("Discharge Complete")
        break
      if spinner == "|":
        spinner = "/"
      elif spinner == "/":
        spinner = "-"
      elif spinner == "-":
        spinner = "\\"
      elif spinner == "\\":
        spinner = "|"

  ser.close()
