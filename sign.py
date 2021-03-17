#!/usr/bin/env python
from opensign import OpenSign, OpenSignCanvas

signOn = 0
signIsStopped = 0


def status():
    global signIsStopped 
    return signIsStopped

def onOff(state):
    global signOn
    global signIsStopped
    
    if (signIsStopped == 0) and (state==1):
        signIsStopped = 1 
        print('Powering Matrix Led On...')
        signOn = state
        
    if (signIsStopped == 1) and (state==0):
        signOn = state
        
    else:
        print('Matrix Led powering Off...')

def start():
    global signOn
    global signIsStopped
    print('Building Canvas...')
    message1 = OpenSignCanvas()
    message1.add_font("dejavu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    message1.set_stroke(1, (255, 255, 255))
    message1.add_text("Bianca's Room", color=(255, 0, 0))
    message1.set_shadow()

    message2 = OpenSignCanvas()
    message2.add_font(
        "comic", "/usr/share/fonts/truetype/msttcorefonts/Comic_Sans_MS.ttf", 14
    )
    message2.set_stroke(1, (0, 0, 0))
    message2.add_text("Fat Cats", color=(255, 255, 0), y_offset=-2)
    message2.set_shadow()

    message3 = OpenSignCanvas()
    message3.add_font("dejavu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    message3.set_stroke(1, (0, 0, 0))
    message3.add_text("ROBLOX", color=(255, 0, 0))

    message4 = OpenSignCanvas()
    message4.add_font("dejavu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    message4.set_stroke(1, (0, 0, 0))
    message4.add_text("Be Nice", color=(255, 255, 255))
    message4.set_shadow()

    sign = OpenSign(chain=1)
    
    while signOn==1:
            print('Starting sign...')
            if signOn==1:
                sign.join_in_vertically(message1)
            if signOn==1:
                sign.loop_left(message1)
            if signOn==1:
                sign.flash(message1, count=3)
            if signOn==1:
                sign.split_out_vertically(message1)
            if signOn==1:
                sign.sleep(1)
            if signOn==1:
                sign.set_background_color((0, 255, 0))
            if signOn==1:
                sign.fade_in(message2)
            if signOn==1:
                sign.sleep(1)
            if signOn==1:
                sign.fade_out(message2)
            if signOn==1:
                sign.scroll_in_from_top(message3)
            if signOn==1:
                sign.sleep(1)
            if signOn==1:
                sign.scroll_out_to_bottom(message3)
            if signOn==1:
                sign.scroll_in_from_right(message4)
            if signOn==1:
                sign.sleep(1)
            else: 
                sign.set_background_color((0, 0, 0)) 
                print('Exiting sign...')
                signIsStopped = 0
                signOn=0
               


# Main function
