#!/usr/bin/python
import time
import paho.mqtt.client as mqtt

# Will be called upon reception of CONNACK response from the server.
def on_connect(client, data, flags, rc):
    client.subscribe("ledStrip/status", 1)

def on_message(client, data, msg):
    print("Received message: " ,str(msg.topic+" "+msg.payload.decode("utf-8")))
    
def publishMessage(topic,message):
    client.publish(topic, message,1)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Set the username to 'token:CHANNEL_TOKEN' before calling connect
#client.username_pw_set("token:YOUR_CHANNEL_TOKEN")
# Alternatively, set the username to your SECRET KEY
#client.username_pw_set('YOUR_SECRET_KEY')
client.connect("192.168.2.145", 1883, 60)
client.loop_start()

#Test
#while 1:
    # Publish a message every second
    #client.publish("ledStrip/status", "ON",1)
    #publishMessage("ledStrip/status","OFF")
    #time.sleep(1)