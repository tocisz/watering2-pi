import time
import datetime

MSGID = 0
def get_new_message_id():
    global MSGID
    MSGID = (MSGID+1)%256;
    return MSGID

class generic_request(object):
    def __init__(self, msg_type, data):
        self.id = get_new_message_id()
        self.type = msg_type
        self.data = data

    def set_data(data):
        self.data = data

    def to_bytes(self):
        return [self.id, self.type] + self.data

class time_req(generic_request):
    msg_type = 1
    def __init__(self, timestamp = 0):
        self.timestamp = timestamp

        data = []
        t = self.timestamp
        for i in range(4):
            data.append(t & 0xff)
            t >>= 8

        super(time_req,self).__init__(time_req.msg_type, data)

class analog_read_req(generic_request):
    msg_type = 2
    def __init__(self, pin):
        self.pin = pin
        super(analog_read_req,self).__init__(analog_read_req.msg_type, [self.pin])

class blink_req(generic_request):
    msg_type = 3
    def __init__(self, pin, ms):
        self.pin = pin
        self.ms = ms
        data = [
            pin,
            ms & 0xff,
            (ms >> 8) & 0xff
        ]
        super(blink_req,self).__init__(blink_req.msg_type, data)

class PacketTooShort(Exception):
    pass
class WrongDataLength(Exception):
    pass

class generic_response(object):
    msg_type = 0 # always 0 for response
    def __init__(self, packet):
        if len(packet) < 2:
            raise PacketTooShort

        self.id = packet[0]
        self.type = packet[1]
        self.data = packet[2:]

class time_resp(generic_response):
    data_length = 4
    def __init__(self, msg):
        self.id = msg.id
        self.type = msg.type
        self.data = msg.data
        if len(self.data) != time_resp.data_length:
            raise WrongDataLength

        self.timestamp = 0;
        for i in range(time_resp.data_length):
            self.timestamp >>= 8
            self.timestamp |= (self.data[i] << 24)

    def __str__(self):
        df = datetime.datetime.fromtimestamp(self.timestamp)
        return df.strftime('%Y-%m-%d %H:%M:%S')

class analog_read_resp(generic_request):
    data_length = 2

    def __init__(self, msg):
        self.id = msg.id
        self.type = msg.type
        self.data = msg.data
        if len(self.data) != analog_read_resp.data_length:
            raise WrongDataLength

        self.value = 0;
        for i in range(analog_read_resp.data_length):
            self.value >>= 8
            self.value |= (self.data[i] << 8)

    def __str__(self):
        return str(self.value)

class blink_resp(generic_request):
    data_length = 0

    def __init__(self, msg):
        self.id = msg.id
        self.type = msg.type
        self.data = msg.data
        if len(self.data) != blink_resp.data_length:
            raise WrongDataLength

    def __str__(self):
        return "OK"

import vw_conf as vw

def send_bytes(b):
    while not vw.tx.ready():
        time.sleep(0.02)
    print("Sending "+repr(b))
    vw.rx.pause()
    vw.tx.put(b)
    while not vw.tx.ready(): # Wait for transmission to finish
        time.sleep(0.02)
    vw.rx.resume()

class ResponseTimeout(Exception):
    pass
class BadResponseId(Exception):
    pass
class BadResponseType(Exception):
    pass

def create_response_object(packet, req):
    resp = generic_response(packet)

    if resp.id != req.id:
        raise BadResponseId

    if resp.type != 0:
        raise BadResponseType

    if req.type == time_req.msg_type:
        return time_resp(resp)

    elif req.type == analog_read_req.msg_type:
        return analog_read_resp(resp)

    elif req.type == blink_req.msg_type:
        return blink_resp(resp)

    return None

def send_and_receive(req):
    b = req.to_bytes()

    retries = 0
    while retries < 5:
        if retries > 0:
            print("Retrying")
        retries += 1

        send_bytes(b)
        try:
            wait_iteration = 0
            while not vw.rx.ready():
                time.sleep(0.02)
                wait_iteration += 1
                if wait_iteration > 100:
                    raise ResponseTimeout

            resp = vw.rx.get()
            print("Resonse "+repr(resp))
            resp = create_response_object(resp, req)
            if resp != None:
                return resp
        except ResponseTimeout:
            print("ResponseTimeout")
            continue
        except PacketTooShort:
            print("PacketTooShort")
            continue
        except WrongDataLength:
            print("WrongDataLength")
            continue
        except BadResponseId:
            print("BadResponseId")
            continue
        except BadResponseType:
            print("BadResponseType")
            continue

    # All retries failed
    raise ResponseTimeout
