import network
import espnow
try: 
    from dht import DHT11
except:
    pass
from machine import Pin, ADC
from time import sleep, ticks_ms
from adc_sub import ADC_substitute

dht11 = DHT11(Pin(26, Pin.IN))
led = Pin(13, Pin.OUT)

############ OBJECTS ##############

station = network.WLAN(network.STA_IF)     
station.active(True)

esp_now = espnow.ESPNow()                   
esp_now.active(True)                        

############ CONSTANTS ############

MAC_ADDR_BROADCAST = const(b'\xff\xff\xff\xff\xff\xff')

############ BATTERY ##############
pin_battery = 32
battery = ADC_substitute(pin_battery)
ip1 = 1680
ip2 = 2440
bp1 = 0                                
bp2 = 100                             
alpha = (bp2 - bp1) / (ip2 - ip1)      


beta = bp1 - alpha * ip1               

                           
############ FUNCTIONS ############

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
            return False                  
    
    return True                       


def esp_now_add_mac_address(mac_addr):
    if esp_now_mac_in_list(mac_addr) == False:
        esp_now.add_peer(mac_addr)           


def esp_now_send_message(mac_addr, string):
    try:
        esp_now.send(mac_addr, string, False)
    except ValueError as e:
        print("Error sending the message: " + str(e))    


def esp_now_receive_message():
    try:    
        host, msg = esp_now.recv(10)              
        if msg:                            
            return host, msg
        else:
            return None, None
    
    except ValueError as e:
        print("Error receiving: " + str(e))
        return None, None

esp_now_add_mac_address(MAC_ADDR_BROADCAST)
while True:
    battery_percentage = get_battery_percentage()
    
    led.off()
    try:
        dht11.measure()
    
        temperature = dht11.temperature()
        humidity = dht11.humidity()

        dht11_data = f'Vejrst {temperature} {humidity} {battery_percentage}'
    
        esp_now_send_message(MAC_ADDR_BROADCAST, dht11_data)
        led.on()
    except:
        pass
    sleep(2)

