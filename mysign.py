#!/usr/bin/env python
from opensign import OpenSign, OpenSignCanvas
from threading import Thread
from PIL import ImageColor


class mySign:

    sign = OpenSign()
    isRunning = False
    killSign = False
    busy = False
    newMessage = OpenSignCanvas()
    powerOffMessage = OpenSignCanvas()
    emptyMessage = OpenSignCanvas()
    showScrollRight = True
    showScrollLeft = True
    showFade = True
    showSplit = True
    showImage = True
    powerOffMessage
    powerOffMessage.clear
    powerOffMessage.add_font(
        "comic", "/usr/share/fonts/truetype/msttcorefonts/Comic_Sans_MS.ttf", 14)
    powerOffMessage.set_stroke(1, (255, 255, 255))
    powerOffMessage.add_text("bye", (255, 0, 0), y_offset=-2)
    powerOffMessage.set_shadow()

    def __init__(
        self,
        *,
        myText="Poopy doopy",
        myTextColor='#EDFF00',
        myStrokeColor='#000000',
        myBackgroundColor='#EC10F2'
    ):

        self.myText = myText
        self.myTextColor = myTextColor
        self.myStrokeColor = myStrokeColor
        self.myBackgroundColor = myBackgroundColor

        # self.makeNewMessage(myText,myTextColor,myStrokeColor)

    def makeNewMessage(self, text, textColor, strokeColor, bgColor):

        self.myText = text
        self.myTextColor = textColor
        self.myStrokeColor = strokeColor
        self.myBackgroundColor = bgColor

        textColor = ImageColor.getcolor(textColor, "RGB")
        strokeColor = ImageColor.getcolor(strokeColor, "RGB")
        bgColor = ImageColor.getcolor(bgColor, "RGB")

        if self.isRunning:
            self.stopSign()
            while self.isRunning:
                print('Waiting for sign to stop...')
                self.sign.sleep(1)
        self.newMessage.clear()
        self.sign.show(self.newMessage)
        self.sign.sleep(1)
        self.sign.hide(self.newMessage)
        self.newMessage.add_font(
            "comic", "/usr/share/fonts/truetype/msttcorefonts/Comic_Sans_MS.ttf", 14)
        self.newMessage.set_stroke(1, strokeColor)
        self.newMessage.add_text(text, textColor, y_offset=-2)
        self.newMessage.set_shadow()
        print('Message updated...')
        self.startSign()
        return "New message created"

    def startSign(self):
        if self.isRunning == False:
            self.busy = True
            self.killSign = True
            tSign = Thread(target=self._runSign).start()

    def stopSign(self):
        self.busy = True
        self.killSign = False
        print('Killing Sign Process...')

    def _runSign(self):
        self.isRunning = True
        print('Sign Starting...')
        while self.killSign:
            print('Started...')
            self.busy = False
            if self.killSign:
                self.sign.set_background_color(
                ImageColor.getcolor(self.myBackgroundColor, "RGB"))
            if (self.killSign) and (self.showSplit):
                self.sign.join_in_vertically(self.newMessage)
            if (self.killSign) and (self.showScrollLeft):
                self.sign.scroll_in_from_right(self.newMessage)
            if (self.killSign) and (self.showScrollLeft):
                self.sign.scroll_out_to_left(self.newMessage)
            if (self.killSign) and (self.showScrollRight):
                self.sign.scroll_in_from_left(self.newMessage)
            if (self.killSign) and (self.showScrollRight):
                self.sign.scroll_out_to_right(self.newMessage)
            if (self.killSign) and (self.showSplit):
                self.sign.split_out_vertically(self.newMessage)
            if (self.killSign) and (self.showFade):
                self.sign.sleep(1)
            if (self.killSign) and (self.showFade):
                self.sign.fade_in(self.newMessage)
            if (self.killSign) and (self.showFade):
                self.sign.sleep(1)
            if (self.killSign) and (self.showFade):
                self.sign.fade_out(self.newMessage)
            if self.killSign:
                self.sign.sleep(1)
            else:
                self.sign.hide(self.newMessage)
                self.sign.set_background_color((0, 0, 0))
                self.sign.set_position(self.powerOffMessage, 0, 0)
                self.sign.show(self.powerOffMessage)
                self.sign.sleep(1)
                self.sign.hide(self.powerOffMessage)
                print('Sign Stopped...')
                self.isRunning = False
                self.busy = False
        self.isRunning = False
        self.busy = False
