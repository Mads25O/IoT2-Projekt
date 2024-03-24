import paho.mqtt.publish as publish
from time import sleep
from get_sensor_data import get_kontor_dht11_data, get_kontor_ccs811_data, get_motor_data, get_vejrst_sensor_data
from log_sensor_data import log_kontor_dht11_data, log_kontor_ccs811_data, log_motor_data, log_motor_status

def open_window():
    payload = ("*open")
    get_motor_bat = int(str(get_motor_data(1)[2]).strip("[]"))
    log_motor_data(1, get_motor_bat)
    publish.single("gruppe4c/motor", payload, hostname="74.234.16.224")
    

def close_window():
    payload = ("*close")
    get_motor_bat = int(str(get_motor_data(1)[2]).strip("[]"))
    log_motor_data(0, get_motor_bat)
    publish.single("gruppe4c/motor", payload, hostname="74.234.16.224")
    

while True:

    #### Henter data fra database ####

    kontor_dht11 = get_kontor_dht11_data(1)
    temperature = int(str(kontor_dht11[1]).strip("[]"))
    humidity = int(str(kontor_dht11[2]).strip("[]"))

    kontor_ccs811 = get_kontor_ccs811_data(1)
    co2 = int(str(kontor_ccs811[1]).strip("[]"))

    vejrstation = get_vejrst_sensor_data(1)
    vejrst_temp = int(str(vejrstation[1]).strip("[]"))
    
    motor_data = int(str(get_motor_data(1)[1]).strip("[]"))

    #### Motor styring ####

    if vejrst_temp >= 10:
        if co2 >= 3000:
            motor_data = int(str(get_motor_data(1)[1]).strip("[]"))
            if motor_data == 0:
                open_window()

            
        if co2 >= 2000:
            motor_data = int(str(get_motor_data(1)[1]).strip("[]"))
            if temperature >= 15:            
                if motor_data == 0:
                    open_window()
                

        if co2 >= 1500:
            motor_data = int(str(get_motor_data(1)[1]).strip("[]"))
            if temperature >= 20:
                if motor_data == 0:
                    open_window()

        
        if co2 <= 1000:
            motor_data = int(str(get_motor_data(1)[1]).strip("[]"))
            if motor_data == 1:
                close_window()

        if temperature <= 15:
            motor_data = int(str(get_motor_data(1)[1]).strip("[]"))
            if co2 >= 2500:
                if motor_data == 0:
                    open_window()

            
            if co2 < 2500:
                motor_data = int(str(get_motor_data(1)[1]).strip("[]"))
                if motor_data == 1:
                    close_window()
                
    else:
        pass
    sleep(10)