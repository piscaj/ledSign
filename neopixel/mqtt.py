import adafruit_minimqtt.adafruit_minimqtt as MQTT
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import wifi, esp
from code import setColor, fadeColor, BLACK, PURPLE

neoPixelPowerState = "OFF"

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

### MQTT Code ###
# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name

def connected(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print("Connected to MQTT broker!")
    # Subscribe to all changes on the default_topic feed.
    client.subscribe("ledStrip/power")
    client.subscribe("ledStrip/preset")


def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    print("Disconnected from MQTT Broker!")


def message(client, topic, message):
    global neoPixelPowerState
    """Method callled when a client's subscribed feed has a new
    value.
    :param str topic: The topic of the feed with a new value.
    :param str message: The new value
    """
    print("New message on topic {0}: {1}".format(topic, message))
    if topic == "ledStrip/power":
        if message == "ON":
            setColor(PURPLE)
            mqtt_client.publish("ledStrip/status", "ON")
            neoPixelPowerState = "ON"
        elif message == "OFF":
            fadeColor(0)
            setColor(BLACK)
            mqtt_client.publish("ledStrip/status", "OFF")
            neoPixelPowerState = "OFF"
            
            
# Initialize MQTT interface with the esp interface
MQTT.set_socket(socket, esp)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(broker=secrets["broker"],port=secrets["port"])

# Setup the callback methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

# Connect the client to the MQTT broker.
mqtt_client.connect()


