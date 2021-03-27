import time
import board
import busio
import neopixel
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from fade import Fader
import gradient

count = 0
neoPixelPowerState = "OFF"

# Set up NeoPixel
pixel_pin = board.A1
num_pixels = 240
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1.0, auto_write=False)

### WiFi ###

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)

wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)

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



# Connect to WiFi
print("Connecting to WiFi...")
wifi.connect()
print("Connected!")

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


# NeoPixel ######################################

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 114, 204)
PINK = (255, 5, 234)
BLACK = (0, 0, 0)

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
    mqtt_client.publish("ledStrip/preset", "CHASE")
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
        mqtt_client.loop()
    time.sleep(0.1)


def rainbow_cycle(wait):
    mqtt_client.publish("ledStrip/preset", "RAINBOW")
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)
        mqtt_client.loop()

def setColor(color):
    mqtt_client.publish("ledStrip/preset", "COLOR")
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
fadeState = True

previous = None

while True:
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
    else:
        count = 0
        mqtt_client.loop()
        time.sleep(0.5)
        mqtt_client.publish("ledStrip/status", neoPixelPowerState)

