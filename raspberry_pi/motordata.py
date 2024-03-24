###################################################################
# Ligger på Rasp. Modtager motor data fra Azure og sender til ESP #
###################################################################

import serial as ser
from datetime import datetime
import paho.mqtt.subscribe as subscribe


data = ser.Serial("/dev/ttyS0", 9600, timeout=2)

def on_message_print(client, userdata, message):
    payload_string = str(message.payload)
    userdata["message_count"] += 1

    payload_string_strip = payload_string.strip('b"()').strip("',")
    payload_replaced = payload_string_strip.replace("'", "").replace(",", "")
    payload_split = payload_replaced.split()

    data.write(f"{payload_split}".encode())

subscribe.callback(on_message_print, "gruppe4c/motor", hostname="74.234.16.224", userdata={"message_count": 0})


