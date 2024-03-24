import network
import espnow
from dht import DHT11
from machine import Pin, UART
from time import sleep, ticks_ms
import sys, uselect


pir = Pin(32, Pin.IN)
dht11 = DHT11(Pin(26, Pin.IN))

########################################
# UART

uart_port = 2
uart_speed = 9600

uart = UART(uart_port, uart_speed)

usb = uselect.poll()
usb.register(sys.stdin, uselect.POLLIN)

########################################
# OBJECTS
station = network.WLAN(network.STA_IF) 
station.active(True)             

esp_now = espnow.ESPNow()              
esp_now.active(True)                  

########################################
# CONSTANTS
MAC_ADDR_BROADCAST = const(b'\xff\xff\xff\xff\xff\xff')
                           
########################################
# FUNCTIONS

# Is the MAC address in the list
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
            print(host, msg)
            if msg.startswith("Vejrst"):
                uart.write(f"{msg}\n".encode())
            if msg.startswith("4CBatMotor"):
                uart.write(f"{msg}\n".encode())
            return host, msg
        else:
            return None, None
    
    except ValueError as e:
        print("Error receiving: " + str(e))
        return None, None

motor_close = "*close"
motor_open = "*open"

start_time = ticks_ms()
interval = 2000

esp_now_add_mac_address(MAC_ADDR_BROADCAST)

while True:

    dht11.measure()

    temperature = dht11.temperature()
    humidity = dht11.humidity()
    
    dht11_data = f'Temp&Hum {temperature} {humidity}'
    
    if ticks_ms() - start_time >= interval:
        start_time = ticks_ms()
        uart.write(f"{dht11_data}\n".encode())
    
    esp_now_receive_message()
    
    if uart.any() > 0:
        string = uart.read().decode()
        print(string)
        if string == "['*open']":
            esp_now_send_message(MAC_ADDR_BROADCAST, motor_open)
        
        if string == "['*close']":
            esp_now_send_message(MAC_ADDR_BROADCAST, motor_close)
    
    if usb.poll(0):
        ch = sys.stdin.read(1)
        uart.write(ch)
        if ch == "\n":
            print()
            
    if pir():
        pir_data = 'Pir4C'
        uart.write(f"{pir_data}\n".encode())
        if not pir():
            pass