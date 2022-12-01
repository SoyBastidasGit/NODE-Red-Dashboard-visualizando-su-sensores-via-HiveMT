#mqtt-subscribe.py

import network
import time
from machine import Pin
from simple import MQTTClient

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID","PASSWORD")
time.sleep(5)
print(wlan.isconnected())

#####################################################
led = Pin("LED", Pin.OUT)
LED_state = 0
#####################################################

mqtt_server = 'broker.hivemq.com'
client_id = 'SoyBastidas'
topic_sub = b'Picow-led'


def sub_cb(topic, msg):
    print("Nuevo mensaje sobre el tema: {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(msg)
    if msg == "on":
        led.value(1)
    elif msg == "off":
        led.value(0)

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=60)
    client.set_callback(sub_cb)
    client.connect()
    print('Conectado a %s Cliente MQTT'%(mqtt_server))
    return client

def reconnect():
    print('No se pudo conectar con el Cliente MQTT. Reconectando...')
    time.sleep(5)
    machine.reset()
    
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
while True:
    client.subscribe(topic_sub)
    time.sleep(1)
