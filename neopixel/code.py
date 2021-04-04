import time,random
import board
import neopixel
from fade import Fader
import gradient
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from effects import neopixel_strip

count = 0
fadeState = False
randomState = False
colorChaseState = False
colorPongState = False
colorChaseColors = ""
colorPongColors = ""
previous = None

fader = Fader(gradient.july4th24[1])

# Set up NeoPixel strip
pixel_pin = board.A1
num_pixels = 240
pixels = neopixel.NeoPixel(pixel_pin, num_pixels,brightness=1.0, auto_write=False)

ns = neopixel_strip(num_pixels,pixels)

neoPixelPowerState = "OFF"
Isconnected = False

# Get MQTT details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("MQTT secrets are kept in secrets.py, please add them there!")
    raise

# Connect to WiFi
print("Connecting to WiFi...")
wifi.wifi.connect()
print("Connected!")

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
    client.subscribe("ledStrip/color")
    client.subscribe("ledStrip/chase")
    client.subscribe("ledStrip/pong")
    client.subscribe("ledStrip/fade")
    client.subscribe("ledStrip/random")


def disconnected(client, userdata, rc):
    global Isconnected
    Isconnected = False
    # This method is called when the client is disconnected
    print("Disconnected from MQTT Broker!")

def mqttUpdate():

    try:
        mqtt_client.loop()

    except (ValueError, RuntimeError) as e:
        print("Failed to update", e)
        wifi.wifi.reset()
        print("Connecting to WiFi...")
        wifi.wifi.connect()
        print("Connected!")
        time.sleep(10)
        print("Connecting to WiFi...")
        wifi.wifi.connect()
        print("Connected!")
        mqtt_client.connect()

def publish(topic,message):

    try:
        mqtt_client.publish(topic, message)

    except (ValueError, RuntimeError) as e:
        print("Failed to send message", e)
        print("Reseting WiFi...")
        wifi.wifi.reset()
        time.sleep(10)
        print("Connecting to WiFi...")
        wifi.wifi.connect()
        print("Connected!")
        mqtt_client.connect()

def message(client, topic, message):
    global neoPixelPowerState
    global colorChaseState
    global colorChaseColors
    global colorPongColors
    global colorPongState
    global randomState
    """Method callled when a client's subscribed feed has a new
    value.
    :param str topic: The topic of the feed with a new value.
    :param str message: The new value
    """
    try:
        print("New message on topic {0}: {1}".format(topic, message))
        if topic == "ledStrip/power":
            if message == "ON":
                setColor(WHITE)
                publish("ledStrip/status", "ON")
                neoPixelPowerState = "ON"
            elif message == "OFF":
                fadeColor(0)
                colorChaseState = False
                colorPongState = False
                randomState = False
                setColor(BLACK)
                publish("ledStrip/status", "OFF")
                neoPixelPowerState = "OFF"
        elif topic == "ledStrip/color":
            fadeColor(0)
            colorChaseState = False
            colorPongState = False
            randomState = False
            color = message
            color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            setColor(color)
        elif topic == "ledStrip/chase":
            fadeColor(0)
            colorPongState = False
            randomState = False
            colorChaseColors = ""
            colorChaseColors = message.split(",")
            for x in range(4):
                colorChaseColors[x] = tuple(int(colorChaseColors[x][i:i+2], 16) for i in (0, 2, 4))
            colorChaseState = True
        elif topic == "ledStrip/pong":
            fadeColor(0)
            colorChaseState = False
            randomState = False
            colorPongColors = ""
            colorPongColors = message.split(",")
            for x in range(4):
                colorPongColors[x] = tuple(int(colorPongColors[x][i:i+2], 16) for i in (0, 2, 4))
            colorPongState = True
        elif topic == "ledStrip/fade":
            global fader
            colorPongState = False
            colorChaseState = False
            randomState = False
            r=random.randint(0,5)
            if message == "pride24":
                fader = Fader(gradient.pride24[r])
                fadeColor(1)
            elif message == "halloween24":
                fader = Fader(gradient.halloween24[r])
                fadeColor(1)
            elif message == "anna_howard_shaw24":
                fader = Fader(gradient.anna_howard_shaw24[r])
                fadeColor(1)
            elif message == "pastels24":
                fader = Fader(gradient.pastels24[r])
                fadeColor(1)
            elif message == "rgb24":
                fader = Fader(gradient.rgb24[r])
                fadeColor(1)
            elif message == "july4th24":
                fader = Fader(gradient.july4th24[r])
                fadeColor(1)
            elif message == "ireland24":
                fader = Fader(gradient.ireland24[r])
                fadeColor(1)
            elif message == "icy24":
                fader = Fader(gradient.icy24[r])
                fadeColor(1)
            elif message == "gray24":
                fader = Fader(gradient.gray24[r])
                fadeColor(1)
            elif message == "white_to_off24":
                fader = Fader(gradient.white_to_off24[r])
                fadeColor(1)
            elif message == "green_to_off24":
                fader = Fader(gradient.green_to_off24[r])
                fadeColor(1)
            elif message == "red_to_off24":
                fader = Fader(gradient.red_to_off24[r])
                fadeColor(1)
            elif message == "blue_to_off24":
                fader = Fader(gradient.blue_to_off24[r])
                fadeColor(1)
        elif topic == "ledStrip/random":
            colorPongState = False
            colorChaseState = False
            randomColor(1)

    except (ValueError, RuntimeError) as e:
        print("Failed to recieve message", e)
        print("Reseting WiFi...")
        wifi.wifi.reset()
        time.sleep(10)
        print("Connecting to WiFi...")
        wifi.wifi.connect()
        print("Connected!")
        mqtt_client.connect()


# Setup the callback methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

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

def color_pong(color, direction):
    global neoPixelPowerState
    setColor(BLACK)
    publish("ledStrip/preset", "PONG")
    neoPixelPowerState = "ON"
    if direction == "ping":
        for i in range(num_pixels):
            pixels[i] = color
            pixels.show()
    elif direction == "pong":
        for i in reversed(range(num_pixels + 1)):
            pixels[i-1] = color
            pixels.show()

def color_chase(color, wait):
    global neoPixelPowerState
    publish("ledStrip/preset", "CHASE")
    publish("ledStrip/status", "ON")
    neoPixelPowerState = "ON"
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()

def rainbow_cycle(wait):
    global neoPixelPowerState
    publish("ledStrip/preset", "RAINBOW")
    publish("ledStrip/status", "ON")
    neoPixelPowerState = "ON"
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)
    mqttUpdate()

def setColor(color):
    global neoPixelPowerState
    publish("ledStrip/preset", "COLOR")
    publish("ledStrip/status", "ON")
    neoPixelPowerState = "ON"
    pixels.fill(color)
    pixels.show()

def fadeColor(state):
    global fadeState
    if state == 1:
        fadeState = True
    elif state == 0:
        fadeState = False

def randomColor(state):
    global randomState
    if state == 1:
        randomState = True
    elif state == 0:
        randomState = False
    
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
                mqttUpdate()
                publish("ledStrip/status", neoPixelPowerState)
                count=0
        elif colorChaseState:
            count+=1
            if count <= 4:
                color_chase(colorChaseColors[count-1],0)
            else:
                mqttUpdate()
                publish("ledStrip/status", neoPixelPowerState)
                count=0
        elif colorPongState:
            count+=1
            if count == 1 or count == 3:
                color_pong(colorPongColors[count-1],"ping")
            elif count == 2 or count == 4:
                color_pong(colorPongColors[count-1],"pong")
            else:
                mqttUpdate()
                publish("ledStrip/status", neoPixelPowerState)
                count=0
        elif randomState:
            for x in list(range(0, ns.strand_length*10)):
                ns.randlights()
            mqttUpdate()
            publish("ledStrip/status", neoPixelPowerState)
            count=0
        else:
            count = 0
            mqttUpdate()
            publish("ledStrip/status", neoPixelPowerState)
            time.sleep(2)