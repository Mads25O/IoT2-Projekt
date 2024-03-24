import serial
import sys
from time import sleep
import ccs811LIBRARY
from datetime import datetime
import paho.mqtt.publish as publish


ser = serial.Serial(port='/dev/ttyS0', baudrate=9600, timeout=2)

sensor = ccs811LIBRARY.CCS811()

def setup(mode=1):
    print('Starting CCS811 Read')
    sensor.configure_ccs811()
    sensor.set_drive_mode(mode)

    if sensor.check_for_error():
        sensor.print_error()
        raise ValueError('Error at setDriveMode.')

    result = sensor.get_base_line()
    sys.stdout.write("baseline for this sensor: 0x")
    if result < 0x100:
        sys.stdout.write('0')
    if result < 0x10:
        sys.stdout.write('0')
    sys.stdout.write(str(result) + "\n")

setup(1)

while True:

    esp_value = ser.readline()
    esp_string = str(esp_value, 'UTF-8')

    
    if esp_string.startswith("Temp&Hum"):
        esp_split = esp_string.split()
        temp_n_hum = esp_split[0]
        temperature = esp_split[1]
        humidity = esp_split[2].strip("'")
        payload = temp_n_hum, temperature, humidity
        publish.single("gruppe4c/sensors", str(payload), hostname="74.234.16.224")
    
    if esp_string.startswith("Pir4C"):
        pir = esp_string.split()
        payload = pir
        publish.single("gruppe4c/sensors", str(payload), hostname="74.234.16.224")

    
    if esp_string.startswith("b'Vejrst"):
        esp_strip = esp_string.strip("b'")
        esp_split = esp_strip.split()
        vejrst = esp_split[0]
        temperature = esp_split[1]
        humidity = esp_split[2]
        battery = esp_split[3].strip("'")
        payload = vejrst, temperature, humidity
        publish.single("gruppe4c/sensors", str(payload), hostname="74.234.16.224")
    
    if esp_string.startswith("b'4CBatMotor"):
        esp_strip = esp_string.strip("b'")
        esp_split = esp_strip.split()
        bat_motor_name = esp_split[0]
        motor_battery = esp_split[1].strip("'")
        payload = bat_motor_name, motor_battery
        publish.single("gruppe4c/sensors", str(payload), hostname="74.234.16.224")

    try:
        if sensor.data_available():
            sensor.read_logorithm_results()
            ccs_name = 'ccs811_4c'
            co2 = sensor.CO2
            payload = ccs_name, co2
            print(payload)

            publish.single("gruppe4c/sensors", str(payload), hostname="74.234.16.224")
    except:
        pass

data.close()