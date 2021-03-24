import paho.mqtt.client as mqtt 

class mqTTSub:

    def __init__(
        self,
        *,
        mqttBroker ="",
        client="",
        topic="",
    ):
 
        client = mqtt.Client(client)
        client.connect(mqttBroker) 
            
    def on_disconnect(client, userdata,rc=0):
        logging.debug("DisConnected result code "+str(rc))
        client.loop_stop()
        
    def newSubscription(self, topic):
        def on_message(self,client, userdata, message):
            print("received message: " ,str(message.payload.decode("utf-8")))   
        client.loop_start()
        self.client.subscribe(topic)
        self.client.on_message=on_message 
        
