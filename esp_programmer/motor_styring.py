import network
import espnow
from machine import Pin
from time import sleep_ms, sleep, ticks_ms
from adc_sub import ADC_substitute


pin_stepper_in1 = 21                  
pin_stepper_in2 = 22
pin_stepper_in3 = 32
pin_stepper_in4 = 33

IN1 = Pin(pin_stepper_in1, Pin.OUT) 
IN2 = Pin(pin_stepper_in2, Pin.OUT)
IN3 = Pin(pin_stepper_in3, Pin.OUT)
IN4 = Pin(pin_stepper_in4, Pin.OUT)
stepper_pins = [IN1, IN2, IN3, IN4]

## BATTERY
pin_battery = 39
battery = ADC_substitute(pin_battery)
ip1 = 1720
ip2 = 2550
bp1 = 0 
bp2 = 100                              
alpha = (bp2 - bp1) / (ip2 - ip1)
beta = bp1 - alpha * ip1

station = network.WLAN(network.STA_IF)
station.active(True)

esp_now = espnow.ESPNow()
esp_now.active(True)

MAC_ADDR_BROADCAST = const(b'\xff\xff\xff\xff\xff\xff')


def get_battery_percentage():          
    ip = battery.read_adc()            

    bp = alpha * ip + beta             
    bp = int(bp)
    
    if bp < 0:                         
        bp = 0
    elif bp > 100:
        bp = 100
    
    return bp

def esp_now_mac_in_list(mac_addr):
    try:
        esp_now.get_peer(mac_addr)
    except OSError as ose: 
        if ose.args[1] == "ESP_ERR_ESPNOW_NOT_FOUND": 
            return False               # MAC address is not in the list     
    
    return True

def esp_now_add_mac_address(mac_addr):
    if esp_now_mac_in_list(mac_addr) == False:
        esp_now.add_peer(mac_addr)
        
        
def esp_now_send_message(mac_addr, string):
    try:
        esp_now.send(mac_addr, string, False)
    except ValueError as e:
        print("Error sending the message: " + str(e))  



def stepper_motor(pins, sequence):
    for step in sequence:      
        for i in range(len(pins)):
            pins[i].value(step[i])
            sleep_ms(2)
            
    pins[-1].value(0)                


def step_clockwise(pins):
    sequence_cw = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    stepper_motor(pins, sequence_cw)

def step_counter_clockwise(pins):
    sequence_ccw = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
    stepper_motor(pins, sequence_ccw)

start_time = ticks_ms()
interval = 30000

esp_now_add_mac_address(MAC_ADDR_BROADCAST)

while True:
    
    battery_percent = get_battery_percentage()
    battery_percentage = f'4CBatMotor {battery_percent}'
    
    host, msg = esp_now.recv()
    
    if msg:
        if msg == b'*open':
            for i in range(128):
                step_clockwise(stepper_pins)

        elif msg == b'*close':
            for i in range(128):
                step_counter_clockwise(stepper_pins)
    if ticks_ms() - start_time >= interval:
        esp_now_send_message(MAC_ADDR_BROADCAST, battery_percentage)
                
                
            
            
