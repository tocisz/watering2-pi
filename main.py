import messages
import vw_conf
import time
import datetime

exit = False
while not exit:

    line = raw_input("> ")
    response = None

    if line == "exit":
        exit = True

    elif line == "get time":
        response = messages.send_and_receive(messages.time_req(0))

    elif line == "set time":
        now = int(time.mktime(datetime.datetime.now().timetuple()))
        response = messages.send_and_receive(messages.time_req(now))

    elif line.startswith("read "):
        args = line.split(" ")
        pin = int(args[1])
        response = messages.send_and_receive(messages.analog_read_req(pin))

    elif line.startswith("blink "):
        args = line.split(" ")
        pin = int(args[1])
        ms = int(args[2])
        response = messages.send_and_receive(messages.blink_req(pin, ms))

    else:
        print("Wrong command")

    if response:
        print("Got "+str(response))
