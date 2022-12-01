#mqtt-publish.py

import network
import time, utime
from machine import Pin, Timer
from simple import MQTTClient

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID","PASSWORD")
time.sleep(5)
print(wlan.isconnected())

######################################################################

led = Pin("LED", Pin.OUT)
LED_state = 0

######################################################################

mqtt_server = 'broker.hivemq.com'
client_id = 'SoyBastidas'
topic_pub = b'Picow-led'
topic_msg_on = b'Led Activado'
topic_msg_off = b'Led Desactivado'

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=3600)
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
    if LED_state == 1:
        LED_state = 0
        led.value(LED_state)
        client.publish(topic_pub, topic_msg_off)
        time.sleep(3)
    else:
        LED_state = 1
        led.value(LED_state)
        client.publish(topic_pub, topic_msg_on)
        time.sleep(3)
