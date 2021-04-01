import board
import neopixel
import time

class Fader:
    def __init__(self, palette, interval=0.1):
        self.checkin = time.monotonic()
        self.color = 0
        self.interval = interval
        self.palette = palette
        self.max = len(self.palette)*interval
        self.epoch = 0
        
    def updatePalette(self,gradient):
        self.palette = gradient

    def update(self):
        self.epoch = time.monotonic() - self.checkin

        index = round((self.epoch%self.max)/self.interval)

        if index > len(self.palette)-1:
            index = 0
            self.checkin = time.monotonic()

        self.color = self.palette[index]
        self.last = index