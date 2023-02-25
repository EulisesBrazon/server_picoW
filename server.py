import network
try:
  import usocket as socket
except:
  import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
from machine import Pin
from SensoresPantalla import *
import _thread
import socket
import rgb


ssid = '1234'
password = '1234'

#define pin RGB
red= Pin(19,Pin.OUT)
green= Pin(18,Pin.OUT)
blue= Pin(20,Pin.OUT)

def get_string_value(input: bool):
    if input:
        return "ON"
    return "OFF"

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
    connection.listen(1)
    
    return connection

def webpage(isOnRed, isOnGreen, isOnBlue):
    #Template HTML
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
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
                                <p><a href="/?led-r"><button class="ButtonR Button">R</button></a></p>
                            </td>
                            <td>
                                <strong> """+ isOnRed +"""</strong> 
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <p><a href="/?led-g"><button class="ButtonG Button">G</button></a></p>
                            </td>
                            <td>
                                <strong> """+ isOnGreen +"""</strong> 
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <p><a href="/?led-b"><button class="ButtonB Button">B</button></a></p>
                            </td>
                            <td>
                            <strong> """+ isOnBlue +""" </strong>  
                            </td>
                        </tr>
                    </tbody>
                </table>
                
</body>
</html>

            """
    return str(html)

def server(connection):
    #Start a web server
    red.off()
    green.off()
    blue.off()
    
    red_value = False
    green_value = False
    blue_value = False
    
    while True:
        #acepta la conexión entrante
        client = connection.accept()[0]
        #con la conexión se almacena la petición que tiene un limite de 1024 bytes
        request = client.recv(1024)
        #se almacena los datos en un string
        request = str(request)
        try:
            request = request.split()[1]
            
            if request == '/?led-r':
                red_value = not red_value
                red.value(red_value)
            elif request == '/?led-g':
                green_value = not green_value
                green.value(green_value)
            elif request == '/?led-b':
                blue_value = not blue_value
                blue.value(blue_value)
                
        except IndexError:
            pass
    
        html = webpage(get_string_value(red_value),get_string_value(green_value),get_string_value(blue_value))
        client.send(html)
        client.close()

def runServer():
    try:
        ip = connect()
        connection = open_socket(ip)
        server(connection)
    except KeyboardInterrupt:
        machine.reset()

runServer()
