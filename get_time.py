#!/usr/bin/env python
import messages
import vw_conf

response = messages.send_and_receive(messages.time_req(0))
print("Got "+str(response))
