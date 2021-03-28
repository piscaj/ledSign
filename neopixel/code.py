import time
import board
import neopixel
from fade import Fader
from gradient import *
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import adafruit_esp32spi.adafruit_esp32spi_socket as socket

count = 0
fadeState = False
colorChaseState = False
colorChaseColors = ""

# Set up NeoPixel strip
pixel_pin = board.A1
num_pixels = 240
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1.0, auto_write=False)

neoPixelPowerState = "OFF"
Isconnected = False

# Get MQTT details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("MQTT secrets are kept in secrets.py, please add them there!")
    raise

# Initialize MQTT interface with the esp interface
MQTT.set_socket(socket, wifi.esp)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(broker=secrets["broker"],port=secrets["port"])

### MQTT Code ###
# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name

def connected(client, userdata, flags, rc):
    global Isconnected
    Isconnected = True
    # This function will be called when the client is connected
    # successfully to the broker.
    print("Connected to MQTT broker!")
    # Subscribe to all changes on the default_topic feed.
    client.subscribe("ledStrip/power")
    client.subscribe("ledStrip/preset")
    client.subscribe("ledStrip/color")


def disconnected(client, userdata, rc):
    global Isconnected
    Isconnected = False
    # This method is called when the client is disconnected
    print("Disconnected from MQTT Broker!")


def message(client, topic, message):
    global neoPixelPowerState
    global colorChaseState
    global colorChaseColors
    """Method callled when a client's subscribed feed has a new
    value.
    :param str topic: The topic of the feed with a new value.
    :param str message: The new value
    """
    print("New message on topic {0}: {1}".format(topic, message))
    if topic == "ledStrip/power":
        if message == "ON":
            setColor(WHITE)
            mqtt_client.publish("ledStrip/status", "ON")
            neoPixelPowerState = "ON"
        elif message == "OFF":
            fadeColor(0)
            colorChaseState = False
            setColor(BLACK)
            mqtt_client.publish("ledStrip/status", "OFF")
            neoPixelPowerState = "OFF"
    if topic == "ledStrip/color":
        fadeColor(0)
        colorChaseState = False
        color = message
        color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        setColor(color)
    if topic == "ledStrip/chase":
        fadeColor(0)
        colorChaseColors = ""
        colorChaseColors = message.split(",")
        for x in range(4): 
            colorChaseColors[x] = tuple(int(colorChaseColors[x][i:i+2], 16) for i in (0, 2, 4))
        colorChaseState = True

# Setup the callback methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

# Connect the client to the MQTT broker.
mqtt_client.connect()

# NeoPixel ######################################

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 114, 204)
PINK = (255, 5, 234)
BLACK = (0, 0, 0)
WHITE = (255, 255, 212)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def color_chase(color, wait):
    global neoPixelPowerState
    mqtt_client.publish("ledStrip/preset", "CHASE")
    mqtt_client.publish("ledStrip/status", "ON")
    neoPixelPowerState = "ON"
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    mqtt_client.loop()
    mqtt_client.publish("ledStrip/status", "ON")
    mqtt_client.publish("ledStrip/preset", "CHASE")


def rainbow_cycle(wait):
    global neoPixelPowerState
    mqtt_client.publish("ledStrip/preset", "RAINBOW")
    mqtt_client.publish("ledStrip/status", "ON")
    neoPixelPowerState = "ON"
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)
    mqtt_client.loop()
    mqtt_client.publish("ledStrip/status", "ON")
    mqtt_client.publish("ledStrip/preset", "RAINBOW")

def setColor(color):
    global neoPixelPowerState
    mqtt_client.publish("ledStrip/preset", "COLOR")
    mqtt_client.publish("ledStrip/status", "ON")
    neoPixelPowerState = "ON"
    pixels.fill(color)
    pixels.show()

def fadeColor(state):
    global fadeState
    if state == 1:
        fadeState = True
    elif state == 0:
        fadeState = False

pride = (4980736, 4980736, 4981248, 4982272, 4984064, 4986880, 4990720, 4996096, 3951616, 1592320, 412672, 19456, 13312, 5126, 1048, 60, 76, 65612, 327756, 852044, 1507367, 2359309, 3538946, 4980736)

fader = Fader(pride)

previous = None

while True:
    if Isconnected:
        if fadeState:
            count+=1
            fader.update()
            if fader.color != previous:
                pixels.fill(fader.color)
                pixels.write()
                previous = fader.color
            if count == 5000:
                mqtt_client.loop()
                mqtt_client.publish("ledStrip/status", neoPixelPowerState)
                count=0
        if colorChaseState:
            count+=1
            if count < 5:
                color_chase(colorChaseColors[count],0)
            elif count > 4:
                mqtt_client.loop()
                mqtt_client.publish("ledStrip/status", neoPixelPowerState)
                count=0
        else:
            count = 0
            mqtt_client.loop()
            time.sleep(2)
            mqtt_client.publish("ledStrip/status", neoPixelPowerState)