import time
import board
import neopixel
from fade import Fader
from gradient import *
import mqtt 

count = 0

# Set up NeoPixel strip
pixel_pin = board.A1
num_pixels = 240
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1.0, auto_write=False)


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
    mqtt.mqtt_client.publish("ledStrip/preset", "CHASE")
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
        mqtt.mqtt.mqtt_client.loop()
        mqtt.mqtt_client.publish("ledStrip/status", mqtt.neoPixelPowerState)
    time.sleep(0.1)


def rainbow_cycle(wait):
    mqtt.mqtt_client.publish("ledStrip/preset", "RAINBOW")
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)
        mqtt.mqtt_client.loop()
        mqtt.mqtt_client.publish("ledStrip/status", mqtt.neoPixelPowerState)

def setColor(color):
    mqtt.mqtt_client.publish("ledStrip/preset", "COLOR")
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
            mqtt.mqtt_client.loop()
            mqtt.mqtt_client.publish("ledStrip/status", mqtt.neoPixelPowerState)
            count=0
    else:
        count = 0
        mqtt.mqtt_client.loop()
        time.sleep(3)
        mqtt.mqtt_client.publish("ledStrip/status", mqtt.neoPixelPowerState)

