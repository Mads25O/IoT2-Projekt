import paho.mqtt.subscribe as subscribe
from log_sensor_data import log_kontor_dht11_data, log_kontor_ccs811_data, log_motor_data, log_vejrst_data, log_pir_data

#### Logger alt data den får i en database ####

def on_message_print(client, userdata, message):
    payload_string = str(message.payload)

    userdata["message_count"] += 1

    payload_string_strip = payload_string.strip('b"()').strip("',")
    payload_replaced = payload_string_strip.replace("'", "").replace(",", "")
    payload_split = payload_replaced.split()

    if 'Temp&Hum' in payload_split[0]:
        temperature = int(payload_split[1])
        humidity = int(payload_split[2])
        log_kontor_dht11_data(temperature, humidity)
        payload_split[0] = "done"

    if 'ccs811_4c' in payload_split[0]:
        co2 = int(payload_split[1])
        log_kontor_ccs811_data(co2)
        payload_split[0] = "done"
    
    if 'Pir4C' in payload_split[0]:
        log_pir_data()
        payload_split[0] = "done"

    if 'Vejrst' in payload_split[0]:
        temperature = int(payload_split[1])
        humidity = int(payload_split[2])
        log_vejrst_data(temperature, humidity)
        payload_split[0] = "done"
    
    if '4CBatmotor' in payload_split[0]:
        status = int(payload_split[0])
        battery = int(payload_split[1])
        log_motor_data(status, battery)
        payload_split[0] = "done"

subscribe.callback(on_message_print, "gruppe4c/sensors", hostname="74.234.16.224", userdata={"message_count": 0})