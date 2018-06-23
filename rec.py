#!/usr/bin/env python
import time
import pigpio
import vw

RX=9
TX=10

BPS=2000

pi = pigpio.pi() # Connect to local Pi.

rx = vw.rx(pi, RX, BPS) # Specify Pi, rx GPIO, and baud.

msg = 0

start = time.time()

while (time.time()-start) < 300:

  msg += 1
  while rx.ready():
     print("Got " + "".join(chr (c) for c in rx.get()))

rx.cancel() # Cancel Virtual Wire receiver.

pi.stop() # Disconnect from local Pi.
