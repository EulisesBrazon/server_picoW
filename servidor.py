#server
import network
try:
  import usocket as socket
except:
  import socket
import urequests
import socket
#displey
from sysfont import sysfont
from machine import SPI
from ST7735 import TFT
#other tools
from time import sleep
from machine import Pin
import gc
gc.enable()
 
ssid = 'picoW'
password = '12345678'

#global variable
date = 'None'
oldDate = 'None'
ip = 'None'

#define pin RGB
red= Pin(11,Pin.OUT)
green= Pin(10,Pin.OUT)
blue= Pin(12,Pin.OUT)

#difien values for displey use
spi = SPI(0, baudrate=20000000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
tft=TFT(spi,0,7,1)
tft.initr()
tft.rgb(True)

led = Pin("LED", Pin.OUT)
led.off()

def get_string_value(input: bool):
    if input:
        return "ON"
    return "OFF"

def http_get(path: str):
    try:
        url = 'http://192.168.211.239/'+path
        response = urequests.requests.get(url)   
        response.close()
    except Exception as e:
        print(e)
        
def accesPoint():
    wlan = network.WLAN(network.AP_IF)
    wlan.config(essid=ssid, password=password)
    wlan.active(True)
    while wlan.active() == False:
        print('Create connection...')
        sleep(1)
    name_ssid = wlan.config('ssid')
    print(f'Acces Point {name_ssid} Created ')
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    led.on()
    return ip
    

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

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(5)
    
    return connection

def saveFile(string):
    file = open("Info.txt", "w")#changed the opening mode, which creates the file automatically
    string = string.split("C")
    for word in string:
        file.write("<p>"+ word +"C</p> ")
    #file.write(string)
    file.close()
    
def loadFile():
    try:
        file = open("Info.txt", "r")#Try, if it doesn't exist
        return file.read()		
    except:
        return 'None'

def webpage(isOnRed, isOnGreen, isOnBlue):
    #Template HTML
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RGB Controller</title>
    <style>
        html {
                    font-family: Helvetica;
                    display: inline-block;
                    margin: 0px auto;
                    text-align: center;
                }
                h1 {
                    color: #0F3376;
                    padding: 2vh;
                }
                p {
                    font-size: 1.5rem;
                }
                table {
                    margin: auto;            
                }
                td{
                    padding: 10px ;
                } 
                .Button {           
                    border-radius: 31px;           
                    display: inline-block;
                    cursor: pointer;
                    color: #ffffff;
                    font-family: Arial;
                    font-size: 17px;
                    font-weight: bold;
                    font-style: italic;
                    padding: 17px 19px;
                    text-decoration: none;           
                }
                .ButtonR {
                    background-color: #ec4949;            
                    border: 6px solid #991f1f;           
                    text-shadow: 0px 2px 2px #471e1e;
                }
                .ButtonR:hover {
                    background-color: #f51616;
                }

                .Button:active {
                    position: relative;
                    top: 1px;
                }
                .ButtonG {
                    background-color: #49ec56;            
                    border: 6px solid #23991f;          
                    text-shadow: 0px 2px 2px #1e4723;
                }
                .ButtonG:hover {
                    background-color: #29f516;
                }  
                .ButtonB {
                    background-color: #4974ec;           
                    border: 6px solid #1f3599;         
                    text-shadow: 0px 2px 2px #1e2447;
                }
                .ButtonB:hover {
                    background-color: #165df5;
                }
    </style>
</head>
<body>
    <h1>Raspberry Pi Pico W Web Server</h1>
                <p>RGB Control</p>    

                <table>
                    <tbody>
                        <tr>
                            <td>
                                <p><a href="/led-r"><button class="ButtonR Button">R</button></a></p>
                            </td>
                            <td>
                                <strong> """+ isOnRed +"""</strong> 
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <p><a href="/led-g"><button class="ButtonG Button">G</button></a></p>
                            </td>
                            <td>
                                <strong> """+ isOnGreen +"""</strong> 
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <p><a href="/led-b"><button class="ButtonB Button">B</button></a></p>
                            </td>
                            <td>
                            <strong> """+ isOnBlue +""" </strong>  
                            </td>
                        </tr>
                        
                    </tbody>
                </table>

</body>
<footer>
    """+ loadFile() +"""
</footer>
</html>

            """
    return str(html)

def startDisplay(date):
    
    size=2
    separation = 4
    h=0
    #data reading
    date = str(date)
    tft.fill(TFT.BLACK)#clean screen
    tft.text((0, h), "IP: ", TFT.RED, sysfont, size, nowrap=True)
    h += sysfont["Height"]*size+separation
    tft.text((0, h), str(ip), TFT.GREEN, sysfont, size, nowrap=True)
    h += sysfont["Height"]*size+separation
    tft.text((0, h), "SSID: ", TFT.RED, sysfont, size, nowrap=True)
    h += sysfont["Height"]*size+separation
    tft.text((0, h), ssid, TFT.GREEN, sysfont, size, nowrap=True)
    h += sysfont["Height"]*size+separation
    tft.text((0, h), "Temperatura: ", TFT.RED, sysfont, size, nowrap=True)
    h += sysfont["Height"]*size+separation
    tft.text((0, h), date, TFT.GREEN, sysfont, size, nowrap=True)
    
def refreshDisplay(date):
    global oldDate
    size=2
    #data reading
    date = str(date)
    tft.text((0, 100), oldDate, TFT.BLACK, sysfont, size, nowrap=True)
    tft.text((0, 100), date, TFT.GREEN, sysfont, size, nowrap=True)
    oldDate = date

def serve(connection):
    #Start a web server
    global date
    
    red.off()
    green.off()
    blue.off()
    
    red_value = False
    green_value = False
    blue_value = False
    
    
    while True:
        
        client = connection.accept()[0]
        call = client.recv(1024)
        call = str(call)
             
        try:
            request = call.split()[1]
        except IndexError:
            pass
        print(f'Request {request}')
        if request == '/led-r':
            red_value = not red_value
            pave = red_value
            red.value(red_value)
                
            client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            html = webpage(get_string_value(red_value),get_string_value(green_value),get_string_value(blue_value))
            client.send(html)
        elif request == '/led-g':
            green_value = not green_value
            green.value(green_value)
                
            client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            html = webpage(get_string_value(red_value),get_string_value(green_value),get_string_value(blue_value))
            client.send(html)
        elif request == '/led-b':
            blue_value = not blue_value
            blue.value(blue_value)
                
            client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            html = webpage(get_string_value(red_value),get_string_value(green_value),get_string_value(blue_value))
            client.send(html)
        elif request.startswith('/date:'):
            date = request.lstrip('/date:')#remove /date:
            refreshDisplay(date)
                
            client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        elif request == '/text:':
            print('entro')
            try:
                start = call.index('/text: ') #get position start
                end = call.index('endText') #get position end
                substring = call[start + len('/text:'):end] #get sub string 
                saveFile(str(substring))
            except IndexError:
                pass
                
            client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            html = webpage(get_string_value(red_value),get_string_value(green_value),get_string_value(blue_value))
            client.send(html)
        else:
            client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            html = webpage(get_string_value(red_value),get_string_value(green_value),get_string_value(blue_value))
            client.send(html)
        client.close()
        print(gc.mem_free())

def runServer():
    try:
        global ip
        global date
        ip = accesPoint()
        connection = open_socket(ip)
        startDisplay(date)
        serve(connection)
        
    except KeyboardInterrupt:
        machine.reset()

runServer()
