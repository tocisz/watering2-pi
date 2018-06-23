import pigpio
import vw
import atexit

RX=9
TX=10
BPS=2000
pi = pigpio.pi() # Connect to local Pi.
tx = vw.tx(pi, TX, BPS) # Specify Pi, tx GPIO, and baud.
rx = vw.rx(pi, RX, BPS) # Specify Pi, rx GPIO, and baud.

def close():
    print("Cleaning up.")
    tx.cancel() # Cancel Virtual Wire sender
    rx.cancel() # Cancel Virtual Wire receiver
    pi.stop() # Disconnect from local Pi

atexit.register(close)
