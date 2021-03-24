import paho.mqtt.client as mqtt 

class mqTTPub:

    def __init__(
        self,
        *,
        mqttBroker ="",
        client="",
    ):
 
        client = mqtt.Client(client)
        client.connect(mqttBroker) 
        
    def publish(self, topic, message):
        self.client.publish(topic, message)
        print("Just published " + message + " to topic " + topic)