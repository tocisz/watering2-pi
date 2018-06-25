import messages
import vw_conf
import time
import datetime
import rrdtool

dbpath = '/home/pi/pwm/watering2-pi/moisture.rrd'
pin = 0

r = messages.send_and_receive(messages.analog_read_req(pin))
readings = "N:"+"%.2f:%.2f:%.2f" % (
    r.to_ohm(r.value-r.sigma),
    r.to_ohm(r.value),
    r.to_ohm(r.value+r.sigma)
    )
print(readings)
rrdtool.updatev([dbpath, readings])
