#Ramirez Bastidas Jose Daniel
#node-red.py

import network
import time
from simple import MQTTClient

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID","PASSWORD")
time.sleep(5)
print(wlan.isconnected())

#########################################################
#Temperatura.py
import machine
import utime

sensortemp = machine.ADC(4)
factorconversion = 3.3 / 65365
temperatura = 0

class Temp:
    def T():
         rawValue = sensortemp.read_u16() * factorconversion
         temperatura = 27 - (rawValue - 0.706) / 0.001721
         utime.sleep(1)
         return temperatura

#########################################################

mqtt_server = 'broker.hivemq.com'
client_id = 'SoyBastidas'
topic_pub_temp = b'Temperatura'

def mqtt_connect():
   client = MQTTClient(client_id, mqtt_server, keepalive=3600)
   client.connect()
   print('Connected to %s MQTT Broker'%(mqtt_server))
   return client

def reconnect():
   print('Failed to connect to the MQTT Broker. Reconnecting...')
   time.sleep(5)
   machine.reset()
   
try:
   client = mqtt_connect()
except OSError as e:
   reconnect()

while True:
    tempe = Temp.T()
    print(tempe)
    client.publish(topic_pub_temp, str(tempe))
    utime.sleep(1)
