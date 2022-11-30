



''' Codigo monstruoso de Breno Araújo '''

import random, time, machine

from umqttsimple import MQTTClient

BROKER = '192.168.43.102'
PORT = 1883
TOPIC = "farm/devices/esp"
topic = "farm/devices/esp"
USERNAME = 'esp0001'
PASSWORD = '#Coolp4ss'
CLIENT_ID = f'dominys-garden-esp-{USERNAME}'

client = MQTTClient(CLIENT_ID, BROKER, PORT, USERNAME, PASSWORD)


logfile = 'data.txt'

logfile = open('data.txt', 'w')

def soil_moisture():
    #120 - 140 nothing water
    
    TMP = 120
    i = 1
    moisture = machine.ADC(machine.Pin(35))

    while True:
        hum = moisture.read()
        print(hum, '#', i, '#')
        moisture_unity = str(hum)
        moisture_data = str(moisture_unity + '\n')
        logfile.write(moisture_data)
        i += 1
        if ( i > 120):
            logfile.close()
            break
        time.sleep(1.0)
          


def relay():
    print('RELAYYYY !!!')

    relay = machine.Pin(33, machine.Pin.OUT)
    time.sleep(0.005)
    relay.value(5)
    time.sleep(0.005)
    relay.value(0)
    client.publish(topic, 'RELAYYYY !!!', retain=False, qos=0)

def beep():
    print('BEEP !!!')
    p23 = machine.Pin(33, machine.Pin.OUT)
    buzzer = machine.PWM(p23)
    buzzer.freq(1200)
    buzzer.duty(100)
    time.sleep(2)
    buzzer.duty(0)
    buzzer.deinit()
    client.publish(topic, 'BEEP !!!', retain=False, qos=0)

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
    if(msg == b'beep'):
        beep()
        beep()
        beep()
    if(msg == b'relay'):
        relay()


def waitmsg():
    while True:
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
#soil_moisture()












