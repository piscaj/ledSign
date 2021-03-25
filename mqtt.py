#!/usr/bin/python
import time
import paho.mqtt.client as mqtt

neoPixlPowerStatus = "OFF"
neoPixlPreset = ""
mqttConnected = False

# Will be called upon reception of CONNACK response from the server.
def on_connect(client, data, flags, rc):
    mqttConnected = True
    client.subscribe("ledStrip/status", 1)
    client.subscribe("ledStrip/preset", 1)

#Recieve message from subscription
def on_message(client, data, msg):
    global neoPixlPowerStatus, neoPixlPreset
    print("Received message: " ,str(msg.topic+" "+msg.payload.decode("utf-8")))
    if str(msg.topic) == "ledStrip/status":
        if str(msg.payload.decode("utf-8")) == "ON":
            neoPixlPowerStatus = "ON"
        elif str(msg.payload.decode("utf-8")) == "OFF":
            neoPixlPowerStatus = "OFF"
         
#Publish message to topic   
def publishMessage(topic,message):
    try:
        client.publish(topic, message,1)
    except:
        mqttConnected = False
        print("MQTT connection lost.")
    
        

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