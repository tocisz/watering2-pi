#!/usr/bin/env python
import messages
import vw_conf
import time
import datetime

now = int(time.mktime(datetime.datetime.now().timetuple()))
response = messages.send_and_receive(messages.time_req(now))
print("Got "+str(response))
