#!/usr/bin/env python
from opensign import OpenSign, OpenSignCanvas
from threading import Thread

class mySign:
    
    sign = OpenSign()
    isRunning = False 
    killSign = False
    busy = False
    newMessage = OpenSignCanvas()
    powerOffMessage = OpenSignCanvas()
    emptyMessage = OpenSignCanvas()
    
    powerOffMessage
    powerOffMessage.clear
    powerOffMessage.add_font("comic", "/usr/share/fonts/truetype/msttcorefonts/Comic_Sans_MS.ttf", 14)
    powerOffMessage.set_stroke(1, (255, 255, 255))
    powerOffMessage.add_text("OFF", (255, 0, 0), y_offset=-2)
    powerOffMessage.set_shadow()
     
    def __init__(
        self,
        *,
        myText="Hello",
        myTextColor=(255, 0, 0),
        textStrokeColor=(255, 255, 255),
        backgroundColor=(245, 66, 215)  
    ):
        
        self.myText=myText
        self.myTextColor=myTextColor
        self.textStrokeColor=textStrokeColor
        self.backgroundColor=backgroundColor 
        
        self.makeNewMessage(myText,myTextColor,textStrokeColor)
        
    def makeNewMessage(self,text,textColor,strokeColor):
        mySign.newMessage.clear
        mySign.newMessage.add_font("comic", "/usr/share/fonts/truetype/msttcorefonts/Comic_Sans_MS.ttf", 14)
        mySign.newMessage.set_stroke(1, strokeColor)
        mySign.newMessage.add_text(text, textColor, y_offset=-2)
        mySign.newMessage.set_shadow()
        return "New message created"
    
    def startSign(self):
        if mySign.isRunning == False:
            mySign.busy=True
            mySign.killSign = True
            tSign = Thread(target=self._runSign).start()
    
    def stopSign(self):
        mySign.busy=True
        mySign.killSign=False
        print('Killing Sign Process...')
             
    def _runSign(self):
        mySign.isRunning = True
        print('Sign Starting...')
        while mySign.killSign:
            print('Started...')
            mySign.busy=False
            if mySign.killSign:
                mySign.sign.join_in_vertically(mySign.newMessage)
            if mySign.killSign:
                mySign.sign.loop_left(mySign.newMessage)
            if mySign.killSign:
                mySign.sign.flash(mySign.newMessage, count=3)
            if mySign.killSign:
                mySign.sign.split_out_vertically(mySign.newMessage)
            if mySign.killSign:
                mySign.sign.sleep(1)
            if mySign.killSign:
                mySign.sign.set_background_color(self.backgroundColor)
            if mySign.killSign:
                mySign.sign.fade_in(mySign.newMessage)
            if mySign.killSign:
                mySign.sign.sleep(1)
            if mySign.killSign:
                mySign.sign.fade_out(mySign.newMessage)
            if mySign.killSign:
                mySign.sign.scroll_in_from_top(mySign.newMessage)
            if mySign.killSign:
                mySign.sign.sleep(1)
            if mySign.killSign:
                mySign.sign.scroll_out_to_bottom(mySign.newMessage)
            if mySign.killSign:
                mySign.sign.scroll_in_from_right(mySign.newMessage)
            if mySign.killSign:
                mySign.sign.sleep(1)
            else:
                #mySign.sign.hide(mySign.newMessage)
                #mySign.sign.flash(mySign.powerOffMessage, count=1)
                #mySign.sign.hide(mySign.powerOffMessage)
                #mySign.sign.set_background_color((0,0,0))
                #mySign.sign.show(mySign.powerOffMessage)
                print('Sign Stopped...')
                mySign.isRunning = False
                mySign.busy=False
        mySign.isRunning = False
        mySign.busy=False
    
         

