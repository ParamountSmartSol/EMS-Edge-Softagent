import uuid
import os
def get_gateway_id():
    mac = uuid.getnode()
    return ''.join(['{:02X}'.format((mac >> i) & 0xff) for i in range(40, -1, -8)])

