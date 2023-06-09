
import random, time, machine

from umqttsimple import MQTTClient

BROKER = '192.168.143.1'
PORT = 1883
TOPIC = "farm/devices/esp"
topic = "farm/devices/esp"
# generate client ID with pub prefix randomly
USERNAME = 'solenoid'
PASSWORD = '#Coolp4ss'
CLIENT_ID = f'dominys-garden-esp-{USERNAME}'

client = MQTTClient(CLIENT_ID, BROKER, PORT, USERNAME, PASSWORD)

def relayoff():
  print('RELAYYYY !!!')

  relay = machine.Pin(33, machine.Pin.OUT)
  relay.value(0)
  client.publish(topic, 'RELAYYYY OFF!!!', retain=False, qos=0)
  
def relayon():
  print('RELAYYYY !!!')

  relay = machine.Pin(33, machine.Pin.OUT)
  relay.value(5)
  client.publish(topic, 'RELAYYYY ON!!!', retain=False, qos=0)

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
    if(msg == b'relayon'):
        relayon()
    if(msg == b'relayoff'):
        relayoff()


def publish(topic):
    while True:

       time.sleep(1)
       msg = input('> ')
       client.publish(topic, msg, retain=False)
 

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
#publish(topic)
waitmsg()












