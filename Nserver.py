#Mac Carter UIC 
#In "main" comments partain to the 'todo list' in the code.

DEBUG = False
#REMOVE

#!/usr/bin/env python
# """A simple/readable example of driving a Shiftbrite / Octobar / Allegro A6281 
# via  hardware SPI on the Raspberry Pi.
 
# You must have /dev/spidev* devices / bcm2708_spi driver for this to work.
# """
 
import fcntl, array, RPi.GPIO as GPIO
#
#   ^   ENABLE THE SCRIPT ABOVE ^
#

#TO DO:
#    figure out gradient from one color to the input colour.
#   finish blinking, Threading somehow.
#   Come up with some way to interperate music. https://rg3.github.io/youtube-dl/download.html
#   Come up with some way to twitter stuff. https://pypi.python.org/pypi/twitter
#   pulsing lights needs threading or to spawn a process.
#   figureout an algorytm for the sky
#   Where to get weather api python https://code.google.com/p/python-weather-api/wiki/Examples#Yahoo!_Weather
# 
#
#
#
#
#
#
#


#-------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------CREDIT for some snipits go to----------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------#
        #                                                                                                                         #
        #               http://docs.macetech.com/doku.php/raspberry_pi_with_octobrite_shiftbrite                                  #
        #                                                                                                                         #
        #   Basic code was used from this webite to help facilitate the use of the rasberri pi's SPI busself.                     #
        #                                                                                                                         #
#-------------------------------------------------------------------------------------------------------------------------------------# 
#-------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------------------------------#
        #                                                                                                                         #
        #                   https://github.com/backupbrain/tornado-websocket-echo-server                                          #
        #                                                                                                                         #
        #     Basic example code was used form backupbrain's github in order to create this programself.                          #
        #          His code was a very basic 'echo' websockets example using the tornado librarry                                 #
        #                                                                                                                         #
        #                                                                                                                         #
        #                                                                                                                         #
#-------------------------------------------------------------------------------------------------------------------------------------# 

#import the web and socket infromation form tornado packages

import math

import threading

# try:
#     from Tkinter import *
# except NameError:
#     pass

import tornado.web
import tornado.websocket
import tornado.ioloop

import time #import time, sleep #time libraries 

from random import randint



 
### /Configuration ###
## Diagram by Mac Carter
## Here is your pi interface
# with the pins layed out on the board
# =======================================
# |                             o  5v   |
# |                             o  o    |
# |         ---------           o  gnd  |
# |                             o  o    |
# |                             o  o    |
# |                             o  o    |
# |                             o  o    |
# |                             o  o    |
# |                             o  o    |
# |                             Di o    |
# |                             o  o    |
# |                             Ci Li   |
# |                             o  Ei   |
# |                                     |
# |                                     |
# |                                     |
# |                                     |
# |                                     |
# |                                     |
# |                                     |
# |                                     |
# |  __________                         |
# |  |        |                         |
# |  |ETHERNET|                         |
# |  |        |                         |
# ===|--------|====|---------|===========
#    		       |===USB===|

### /Configuration ###
 
# set to the number of modules you are controlling.  If this is  a shiftbrite,
#it would be 1, if it's an octobar, 8, etc
 
NUM_LEDS =14
 
#In addition to the hardware SPI pins, we require two general GPIO pins for 
#the enable and latch pins.  It doesn't matter what pins you use
 

ENABLE_PIN = 8
LATCH_PIN  = 7


def printDebug(r,g,b):
    print("r"+str(r))
    print("g"+str(g))
    print("b"+str(b))
    print("\n")
    pass
    
    #draw led seems to be a lot faster.
def drawLed(num,r,g,b):
    num =  num + 1

    red8Bit = r>>2
    green8Bit = g>>2
    blue8Bit = b>>2
    
    red8BitInverse = 255 - red8Bit
    green8BitInverse = 255 - green8Bit
    blue8BitInverse = 255 - blue8Bit

    red8BitHex = "{:02x}".format(red8Bit)
    green8BitHex = "{:02x}".format(green8Bit)
    blue8BitHex = "{:02x}".format(blue8Bit)
    fillColor = "#" + str(red8BitHex) + str(green8BitHex) + str(blue8BitHex)
    
    red8BitInverse = "{:02x}".format(red8BitInverse)
    green8BitInverse = "{:02x}".format(green8BitInverse)
    blue8BitInverse = "{:02x}".format(blue8BitInverse)
    fillColorInverse = "#" + str(red8BitInverse) + str(green8BitInverse) + str(blue8BitInverse)

    string = "Light_" + str(num)
    stringTwo = "Text_" + str(num)
    w.itemconfig(string, fill=fillColor)
    w.itemconfig(stringTwo, fill=fillColorInverse)
    
    pass 

def decodeColor(shouldRender,num,color):
#print color
    
    #undo encoding changes.
    red = (color[1] & 0b00001111)<<6
    red = (color[2] & 0b11111100)>>2 | red

    blue = (color[0] & 0b00111111)<<4
    blue = (color[1] & 0b11110000)>>4 | blue
    
    green = (color[2] & 0b00000011)<<8
    green = color[3] & 0b11111111 | green
    
    
    if True:
        print "red: " + str(red)
        print "green: " + str(green)
        print "blue: " + str(blue)


    if shouldRender:
        num =  num + 1

        red8Bit = r>>2
        green8Bit = g>>2
        blue8Bit = b>>2
        
        red8BitInverse = 255 - red8Bit
        green8BitInverse = 255 - green8Bit
        blue8BitInverse = 255 - blue8Bit

        red8BitHex = "{:02x}".format(red8Bit)
        green8BitHex = "{:02x}".format(green8Bit)
        blue8BitHex = "{:02x}".format(blue8Bit)
        fillColor = "#" + str(red8BitHex) + str(green8BitHex) + str(blue8BitHex)
        
        red8BitInverse = "{:02x}".format(red8BitInverse)
        green8BitInverse = "{:02x}".format(green8BitInverse)
        blue8BitInverse = "{:02x}".format(blue8BitInverse)
        fillColorInverse = "#" + str(red8BitHex) + str(green8BitHex) + str(blue8BitHex)

        string = "Light_" + str(num)
        stringTwo = "Text_" + str(num)
        w.itemconfig(string, fill=fillColor)
        w.itemconfig(stringTwo, fill=fillColorInverse)

        #print(string)

        pass
    pass

def bootSequence():
    for x in xrange(0,NUM_LEDS):
        set_led(x, 0, 0, 0)

    updateLeds(leds)

    for x in xrange(0,NUM_LEDS):
        set_led(x, 0, 1023, 0)
        updateLeds(leds)
        delay(150)


    delay(500)
    for x in xrange(0,NUM_LEDS):
        set_led(x, 1023, 1023, 1023)
        updateLeds(leds)

    delay(300)
    for x in xrange(0,NUM_LEDS):
        set_led(x, 0, 0, 0)
    updateLeds(leds)

    delay(200)
    for x in xrange(0,NUM_LEDS):
        set_led(x, 1023, 1023, 1023)

    updateLeds(leds)
#Wave("asdf")

    pass

def delay(number):
    time.time()
    time.sleep(float(number)/1000.0)#convert seconds to miliseconds
    pass



# def static(message):

# if message[3]=="#":

#     r = "0x"+(message[4]+message[5])
#     g = "0x"+(message[6]+message[7])
#     b = "0x"+(message[8]+message[9])
    
#     r = (eval(r)<<2)
#     g = (eval(g)<<2)
#     b = (eval(b)<<2)
    
#     printDebug(r,g,b)
#     for x in xrange(0,NUM_LEDS):
#         set_led(x, r, g, b)

#     updateLeds(leds)

# else:
#     FlashAllRedPattern()

# pass


def static(message):
    
    if message[3]=="#" or message[3]=="&":
    
        r = "0x"+(message[4]+message[5])
        g = "0x"+(message[6]+message[7])
        b = "0x"+(message[8]+message[9])
        
        r = (eval(r)<<2)
        g = (eval(g)<<2)
        b = (eval(b)<<2)
        
        printDebug(r,g,b)
        
        if message[3]=="#":
            
            for x in xrange(0,NUM_LEDS):

                set_led(x, r, g, b)
            
            updateLeds(leds)

        else:

            lightNo = eval(message[1]+message[2])
            
            if lightNo < NUM_LEDS:
                
                set_led(lightNo,r,g,b)

    else:

        FlashAllRedPattern()

    pass

def blinking(message):
    print "entered blinking"
    if message[3]=="#":
        r = "0x"+(message[4]+message[5])
        g = "0x"+(message[6]+message[7])
        b = "0x"+(message[8]+message[9])

        r = (eval(r)<<2)
        g = (eval(g)<<2)
        b = (eval(b)<<2)

        # printDebug(r,g,b)

        while True:
            for x in xrange(0,NUM_LEDS):
                set_led(x, r, g, b)

            updateLeds(leds)
            delay (200)

            for x in xrange(0,NUM_LEDS):
                set_led(x, 0, 0, 0)

            updateLeds(leds)
            delay (200)

    pass

def music(message):
## Libarry still needs to be chosen
    pass

def pulsing(message):#figure out how to maintain luminase intensity still.
    if message[3]=="#":
        r = "0x"+(message[4]+message[5])
        g = "0x"+(message[6]+message[7])
        b = "0x"+(message[8]+message[9])

        r = (eval(r)<<2)
        g = (eval(g)<<2)
        b = (eval(b)<<2)

        #temp vars
        rOld = r
        gOld = g
        bOld = b


        # 100'ths of color subtracted each time.
        rMult = r/100
        gMult = g/100
        bMult = b/100

        while False: # make this a thread that gets interpreted from a global var being set.

            for x in xrange(0,100):
                time.sleep(100)#asuming miliseconds.

                if ((r>0) and ((r-rMult)>0)):
                    r-=rMult
                if ((g>0) and ((g-gMult)>0)):
                    g-=gMult
                if ((b>0) and ((b-bMult)>0)):
                    b-=bMult

                for x in xrange(0,NUM_LEDS):
                    set_led(x, rOld, gOld, bOld)

            for x in xrange(0,100):
                time.sleep(100)#asuming miliseconds.
                if (r<bOld and ((r+rMult)<1023)):
                    r+=rMult
                if (g<bOld and ((g+gMult)<1023)):
                    g+=gMult
                if (b<bOld and ((b+bMult)<1023)):
                    b+=bMult

                for x in xrange(0,NUM_LEDS):
                    set_led(x, r, g, b)

            updateLeds(leds)
    pass

def strobe(message):#msg format COMMAND(400),COLOR(#XXXXXX) ,INTERVAL_FLASH (2),(3),(4)readDigits  (10,100,1000) 
                    #example 400#EF1616240
                    #broken up 400-#EF1616-2-40
    if message[3]=="#":
        r = "0x"+(message[4]+message[5])
        g = "0x"+(message[6]+message[7])
        b = "0x"+(message[8]+message[9])

    delayTime = 300# default delayTime

    if message[10]=="2":
        delayTime = message[11]+message[12]

    if message[10]=="3":
        delayTime = message[11]+message[12]+message[13]

    if message[10]=="4":
        delayTime = message[11]+message[12]+message[13]+message[14]

    delayTime = int(delayTime)

    r = (eval(r)<<2)
    g = (eval(g)<<2)
    b = (eval(b)<<2)

    while False:#still need to figure out threading.
        for x in xrange(0,NUM_LEDS):
            set_led(x, r, g, b)

        delay(delayTime/4)#should cause a nice strobe effect.
        updateLeds(leds)

        for x in xrange(0,NUM_LEDS):
            set_led(x, 0, 0, 0)

        delay(delayTime/2)
        updateLeds(leds)

    pass

def partyMode(message):
    ##need to experiment more with what function/sets of repeting color combos might work.
    pass

def sky(message):
    ## how does a sky behave? going to figure out delta map
    colorlist
    ColorList = ["FFCC33","E3A857","FD5E53"]## the three colors.

    # ["FFCC33"]#sunglow yellow
    # ["E3A857"]#deeper orange
    # ["FD5E53"]#sunset orange

    pass

def Wave(message):
    ## color switch of temp colors down the line pre defined.
    ColorList = ["FF0000","FF4000","FF8000","FFBF00","FFFF00","BFFF00","80FF00","40FF00","00FF00","00FF40","00FF80","00FFBF","00FFFF","00BFFF","0080FF","0040FF","0000FF","4000FF","8000FF","BF00FF","FF00FF","FF00BF","FF0080","FF0040"]
    for n in xrange(0,10000):
        for i in xrange(0,NUM_LEDS):
            l=i+n
            Hex=ColorList[l%24]
            r = "0x"+(Hex[0]+Hex[1])
            g = "0x"+(Hex[2]+Hex[3])
            b = "0x"+(Hex[4]+Hex[5])

            r = (eval(r)<<2)
            g = (eval(g)<<2)
            b = (eval(b)<<2)

            set_led(i, r, g, b)

        delay(200);
        updateLeds(leds)

    pass

def weather(message):
    ##need a weather api 
    pass

def dnddice(message):
    #come up with encoding scheme, d2 d3 d4 d5 d6
    pass

def random(message):
    ##
    for x in xrange(0,NUM_LEDS):
        r = randint(0, 1023)
        g = randint(0, 1023)
        b = randint(0, 1023)
        for x in xrange(0,NUM_LEDS):
            set_led(x, r, g, b)

    updateLeds(leds)
    pass

def clock(message):
    # NUM_LEDS=31#fix

    tOld=0

    t = time.time()
    t = int(t)
    print(t)
    while True:#add threading
        if tOld!=t:
            tOld=t
            t = time.time()
            t = int(t)
            print("asdf")
            t = "{0:b}".format(t)

            for x in xrange(0,NUM_LEDS):
                if t[30-x]=="1":
                    print x," on"
                    set_led(x, 1023, 1023, 1023)
                else:
                    print x," off"
                    set_led(x, 0, 0, 0)
            delay(1000)
            updateLeds(leds)
    pass

def gradentSwitch(message):
    #calculate deltas and switch.
    pass

def dayTime(message):
    ##implement time changing elements form red to full bright, maybe transition to sky() and then back to red.
    pass

def twitter(message):
    #E00 - String (MESSAGE) - INITIAL(COLOR) - Fade (COLOR)
    #still ned to find an API for this.
    pass

def barLights(message):
    #FOO bar, basically just dim lighting
    for x in xrange(0,NUM_LEDS):
        set_led(x, 700, 500, 500)

    updateLeds(leds)
    pass

def telemetry(lightIn,X1,X2,Y1,Y2,time):
    X2-X1
    Y2-Y1
    LightIn
    pass

def FlashAllRedPattern():
    counter = 3

    while counter!=0:
        for x in xrange(0,NUM_LEDS):
            set_led(x, 0, 0, 0)

        updateLeds(leds)

        delay(130)

        for x in xrange(0,NUM_LEDS):
            set_led(x, 1023, 0, 0)

        updateLeds(leds)

        delay(70)

        counter=counter-1
    DEBUG
    pass

def off():
    for x in xrange(0,NUM_LEDS):#turns off the lights. 
        set_led(x, 0, 0, 0)
        print(x)
    updateLeds(leds)

    pass

def encodeColor(red, green, blue):
    # """Takes 10 bits of each color (0-1023) and packs it into the four bytes
    # needed by the LED controller
 
    # Ported from: http://docs.macetech.com/doku.php/shiftbrite#code_example
    # """
    rv = bytearray(4)
 
    #2bit control, 6bit blue
    rv[0] = (0b00 << 6) & 0b11111111 | blue >> 4
 
    #4bit blue, 4 bit red
    rv[1] = (blue << 4) & 0b11111111 | red >> 6
 
    #6bit red, 2 bit green
    rv[2] = (red  << 2) & 0b11111111 | green >> 8
 
    #8bits green
    rv[3] = green & 0b11111111
 
    return rv
 
def updateLeds(bytes):
    if (not DEBUG):
        # """Just write the byte array out to the SPI device and toggle the latch"""
        #write the shit out over SPI
        spidev.write(bytes)
        print(len(bytes))
        spidev.flush()
     
        #latch, #rpi is slow enough we don't need a delay here
        GPIO.output(LATCH_PIN, 1)
        GPIO.output(LATCH_PIN, 0)
    pass
 
 
def set_led(num, r, g, b):

    # """helper function to quickly set an LED color
 
    # Don't use this in production code, global is bad mmmkay?
    # """
    if DEBUG:
        drawLed(num,r,g,b)
        pass
    global leds
 
    leds[num*4:(num*4)+4] = encodeColor(r, g, b)
#decodeColor(DEBUG,num,leds[num*4:(num*4)+4])

class LightThread (threading.Thread):
    lightStatic = "000"
    lightBlinking = "100"
    lightMusic = "200"
    lightPulsing = "300"
    lightStrobe = "400"
    lightPartyMode = "500"
    lightSky = "600"
    lightWave = "700"
    lightWeather = "800"
    lightDnddice = "900"
    lightRandom = "A00"
    lightClock = "B00"
    lightGradentSwitch = "C00"
    lightDayTime = "D00"
    lightTwitter = "E00"
    lightBarLights = "F00"
    lightOff = "0FF"


    def __init__(self):
        threading.Thread.__init__(self)
        #application = tornado.web.Application([(r'/',WSHandler)])
        # application = tornado.web.Application([(r"/", WebSocketHandler),])
        # application.listen(8888)
    def run(self):
        # start a thread for the state machine.
        print "Started a light thread"
        

class TornadoThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #application = tornado.web.Application([(r'/',WSHandler)])
        application = tornado.web.Application([(r"/", WebSocketHandler),])
        application.listen(8888)
    def run(self):
        delay(3000)
        bootSequence()
        print "Start a tornado"
        tornado.ioloop.IOLoop.instance().start()


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        i=0
        #on sequence 
        # print "connection opened"
        # self.write_message("connection opened")

    def on_close(self):
        i=0
        print "connection closed"

    def on_message(self,message):
        print "message received: {}".format(message)

        messageHeader = message[0]+message[1]+message[2]
        print "message header: {}".format(messageHeader)
        if messageHeader[0] == "0":#done
            static(message)
        if messageHeader == "100":#Enable threading
            blinking(message)
        if messageHeader == "200":#Still searching for a library
            music(message)
        if messageHeader == "300":#Enable threading
            pulsing(message)
        if messageHeader == "400":#Enable threading
            strobe(message)
        if messageHeader == "500":#Search for a good distribution of light colors
            partyMode(message)
        if messageHeader == "600":#search for a good distibution of random in and out clouds.
            sky(message)
        if messageHeader == "700":#done add threading
            Wave(message)
        if messageHeader == "800":#need a weather api 
            weather(message)
        if messageHeader == "900":#come up with encoding scheme, d2 d3 d4 d5 d6
            dnddice(message)
        if messageHeader == "A00":#done add threading
            random(message)
        if messageHeader == "B00":#add threading
            clock(message)
        if messageHeader == "C00":#calculate deltas and switch.
            gradentSwitch(message)
        if messageHeader == "D00":#implement time changing elements form red to full bright, maybe transition to sky() and then back to red.
            dayTime(message)
        if messageHeader == "E00":#still ned to find an API for this.
            twitter(message)
        if messageHeader == "F00":#BAR get it? bar lighting, just a dim lighting thats all. also done.
            barLights(message)
        if messageHeader == "0FF":#done
            off()
            
        #else:
        #FlashAllRedPattern();#incorrect command.


        #write the data to the strip    
        updateLeds(leds)

        # self.write_message("message received")

application = tornado.web.Application([
    (r"/", WebSocketHandler),
])


if __name__ == "__main__":
    #open the SPI device for writing


    if(not DEBUG):
        spidev = file("/dev/spidev0.0", "wb")

        #set the speed of the SPI bus, 5000000 == 5mhz  
        #Magic number below is from spidev.h SPI_IOC_WR_MAX_SPEED_HZ
        #TODO: can I reference this as a constant from termios?
        fcntl.ioctl(spidev, 0x40046b04, array.array('L', [5000000]))

        #setup our GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ENABLE_PIN, GPIO.OUT)
        GPIO.setup(LATCH_PIN, GPIO.OUT)

        #both pins low to start
        GPIO.output(LATCH_PIN, 0)
        GPIO.output(ENABLE_PIN, 0)

    #setup the initial LED state as a byte array of 4 bytes per module
    leds = bytearray(4 * NUM_LEDS)
    
    
    TornadoThread = TornadoThread()

    # Start new Threads
    TornadoThread.start()

    if(DEBUG):
        top = Tk()
        global w
        w = Canvas(top, width=640, height=480)

        w.create_oval(50, 50, 100, 100, fill="yellow", tags ="Light_1")
        w.create_text(75, 75, text="1", fill="purple", font="Helvetica 26 bold underline", tags = "Text_1")
        w.create_oval(150, 50, 200, 100, fill="yellow", tags ="Light_2")
        w.create_text(175, 75, text="2", fill="purple", font="Helvetica 26 bold underline", tags = "Text_2")
        w.create_oval(250, 50, 300, 100, fill="yellow", tags ="Light_3")
        w.create_text(275, 75, text="3", fill="purple", font="Helvetica 26 bold underline", tags = "Text_3")
        w.create_oval(350, 50, 400, 100, fill="yellow", tags ="Light_4")
        w.create_text(375, 75, text="4", fill="purple", font="Helvetica 26 bold underline", tags = "Text_4")
        w.create_oval(450, 50, 500, 100, fill="yellow", tags ="Light_5")
        w.create_text(475, 75, text="5", fill="purple", font="Helvetica 26 bold underline", tags = "Text_5")
        w.create_oval(550, 50, 600, 100, fill="yellow", tags ="Light_6")
        w.create_text(575, 75, text="6", fill="purple", font="Helvetica 26 bold underline", tags = "Text_6")


        w.create_oval(50, 150, 100, 200, fill="yellow", tags ="Light_7")
        w.create_text(75, 175, text="7", fill="purple", font="Helvetica 26 bold underline", tags = "Text_7")
        w.create_oval(150, 150, 200, 200, fill="yellow", tags ="Light_8")
        w.create_text(175, 175, text="8", fill="purple", font="Helvetica 26 bold underline", tags = "Text_8")
        w.create_oval(250, 150, 300, 200, fill="yellow", tags ="Light_9")
        w.create_text(275, 175, text="9", fill="purple", font="Helvetica 26 bold underline", tags = "Text_9")
        w.create_oval(350, 150, 400, 200, fill="yellow", tags ="Light_10")
        w.create_text(375, 175, text="10", fill="purple", font="Helvetica 26 bold underline", tags = "Text_10")
        w.create_oval(450, 150, 500, 200, fill="yellow", tags ="Light_11")
        w.create_text(475, 175, text="11", fill="purple", font="Helvetica 26 bold underline", tags = "Text_11")
        w.create_oval(550, 150, 600, 200, fill="yellow", tags ="Light_12")
        w.create_text(575, 175, text="12", fill="purple", font="Helvetica 26 bold underline", tags = "Text_12")


        w.create_oval(50, 250, 100, 300, fill="yellow", tags ="Light_13")
        w.create_text(75, 275, text="13", fill="purple", font="Helvetica 26 bold underline", tags = "Text_13")
        w.create_oval(150, 250, 200, 300, fill="yellow", tags ="Light_14")
        w.create_text(175, 275, text="14", fill="purple", font="Helvetica 26 bold underline", tags = "Text_14")
        w.create_oval(250, 250, 300, 300, fill="yellow", tags ="Light_15")
        w.create_text(275, 275, text="15", fill="purple", font="Helvetica 26 bold underline", tags = "Text_15")


        w.pack(side="top", fill="both", expand=True)
        top.mainloop()
    

