
import random, time
from machine import Pin, ADC

from umqttsimple import MQTTClient

BROKER = '192.168.143.1'
PORT = 1883
TOPIC = "farm/devices/esp"
topic = "farm/devices/esp"
# generate client ID with pub prefix randomly
USERNAME = 'esp0001'
PASSWORD = '#Coolp4ss'
CLIENT_ID = f'dominys-garden-esp-{USERNAME}'

client = MQTTClient(CLIENT_ID, BROKER, PORT, USERNAME, PASSWORD)

def soil_moisture():
    i = 0
    opt = ''
    while True:
        moisture = ADC(Pin(35)) #sensor
        #moisture = Pin(35, Pin.IN)#, Pin.PULL_UP)
        moisture_value = moisture.read() #sensor
        #moisture_value = moisture.value() #curto
        print(moisture_value, '#', i, '#')
        if  moisture_value >= 500:
            if opt == 'off':
                pass
            else:
                opt = 'off'
                relay(opt)
            #print('OFF')
        else:
            if opt == 'on':
                pass
            else:
                opt = 'on'
                relay(opt)
            #print('ON')
        i += 1
        time.sleep(1.0)


def relay(opt):
  print(opt+' RELAYYYY !!!')
  client.publish(topic, 'relay'+opt, retain=False, qos=0)

def connect():
    import network
    ssid = "URRA"
    password =  "hotmarines"
    station = network.WLAN(network.STA_IF)
    if station.isconnected() == True:
        print("Conectado!!!")
        print(station.ifconfig())
        return
    station.active(True)
    station.connect(ssid, password)
    while station.isconnected() == False:
        pass
    print("Conectado!!!")
    print(station.ifconfig())




def sub_cb(topic, msg):
    payload = topic + '#  -->  ' + msg
    print("{}#  -->  {}".format(msg, topic))
    #if(msg == b'relay'):
        #relay()

'''
def publish(topic):
    while True:

       time.sleep(1)
       msg = input('> ')
       client.publish(topic, msg, retain=False)
'''

def waitmsg():
    while True:
        soil_moisture()
        if True:
            client.wait_msg()
            
        else: 
            client.check_msg()
        time.sleep(2.0)
        
       
client.set_callback(sub_cb)
connect()
client.connect()
client.subscribe(topic)
waitmsg()