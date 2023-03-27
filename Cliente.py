#server tools
import network
try:
  import usocket as socket
except:
  import socket
import urequests
#other tools
from machine import Pin
from time import sleep
from machine import SPI,Pin,ADC
import gc
gc.enable()

ssid = 'picoW'
password = '12345678'

#define value for use LM35
analog_value = ADC(26)

#define pin RGB
buttonRed = machine.Pin(21,machine.Pin.IN, machine.Pin.PULL_DOWN)
buttonGreen = machine.Pin(20,machine.Pin.IN, machine.Pin.PULL_DOWN)
buttonBlue = machine.Pin(19,machine.Pin.IN, machine.Pin.PULL_DOWN)
buttonText  = machine.Pin(18,machine.Pin.IN, machine.Pin.PULL_DOWN)

def readTemperature():
    conversion_factor = 3.3/ 65535
    temp_voltage_raw = analog_value.read_u16()
    convert_voltage = temp_voltage_raw*conversion_factor
    tempC = convert_voltage/(10.0 / 1000)
    return tempC

def http_get(path: str):
    try:
        url = 'http://192.168.4.1/'+path
        response = urequests.post(url)
        
        print(response)
        if response is not None:
            response.close()
    except Exception as e:
        print(e)
        
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

delay = 0.3

def buttons():
    
    if buttonRed.value()==1:
        print("Red")
        http_get("led-r")
        sleep(delay)
        sentTemp()
        
    if buttonGreen.value()==1:
        print("Green")
        http_get("led-g")
        sleep(delay)
        sentTemp()
        
    if buttonBlue.value()==1:
        print("Blue")
        http_get("led-b")
        sentTemp()
        sleep(delay)
        
    if buttonText.value()==1:      
        #http_get("led-b")
        sentText()
        sleep(delay)

def saveFile(temperature):
    try:
        file = open("Info.txt", "ab")#Try, if it doesn't exist
        file.write(str(temperature)+"C")
        file.close()
    except:
        file = open("Info.txt", "wb")#changed the opening mode, which creates the file automatically
        file.write(str(temperature)+"C")
        file.close()
        
def loadFile():
    try:
        file = open("Info.txt", "r")#Try, if it doesn't exist
        return file.read()		
    except:
        print("archivo no existente")

def sentText():
    text = loadFile()
    print("entro aqui")
    print(text)
    http_get('text: '+str(text)+'endText')

def sentTemp():
    temp = readTemperature()
    print(temp)
    saveFile(temp)
    http_get('date:'+str(temp))
        
def runClient():
    try: 
        conenection = connect()
        while True:
            buttons()
    except KeyboardInterrupt:
        machine.reset()

runClient()

 



