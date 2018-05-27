import os
import time
import datetime
import fontdemo
import RPi.GPIO as GPIO
#import birthdays
from neopixel import *

# Import the ADS1x15 module.
import Adafruit_ADS1x15

# LED strip configuration:
HEIGHT      = 12
WIDTH       = 12
LED_COUNT   = 144    # Number of LED pixels.
LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)
LED_BRIGHTNESS  = 200  # Set to 0 for darkest and 255 for brightest
LED_CHANNEL = 0
LED_STRIP = ws.WS2811_STRIP_GRB

GAIN = 1

GPIO_PIN_IN  = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN_IN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

prefix = list(range(7,9)) + list(range(10,12)) # -> IT IS

minutes = [[], \
        # -> FIVE PAST
        list(range(25,29)) + list(range(42,46)), \
        # -> TEN PAST
        list(range(1,4)) + list(range(42,46)), \
        # -> QUARTER PAST
        list(range(17,24)) + list(range(42,46)), \
        # -> TWENTY PAST
        list(range(30,36)) + list(range(42,46)), \
        # -> TWENTYFIVE PAST
        list(range(30,36)) + list(range(25,29)) + list(range(42,46)), \
        # -> HALF PAST
        list(range(12,16)) + list(range(42,46)), \
        # -> TWENTYFIVE TO
        list(range(30,36)) + list(range(25,29)) + list(range(58,60)), \
        # -> TWENTY TO
        list(range(30,36)) + list(range(58,60)), \
        # -> QUARTER TO
        list(range(17,24)) + list(range(58,60)), \
        # -> TEN TO
        list(range(1,4)) + list(range(58,60)), \
        # -> FIVE TO
        list(range(25,29)) + list(range(58,60)) ]

hours= [range(120,128), \
        # -> ONE
        range(68,71), \
        # -> TWO
        range(108,111), \
        # -> THREE
        range(114,119), \
        # -> FOUR
        range(103,107), \
        # -> FIVE
        range(80,84), \
        # -> SIX
        range(111,114), \
        # -> SEVEN
        range(74,79), \
        # -> EIGHT
        range(97,102), \
        # -> NINE
        range(128,132), \
        # -> TEN
        range(92,95),\
        # -> ELEVEN
        range(61,67), \
        # -> NOON
        range(140,144)]

full_hour= list(range(133,139))

happy_birthday = list(range(36,41)) + list(range(48,56))

def getStripIndexFrom2D(x, y, offset=1):
    '''
    Mapping coordinates to the wordclocks display
    Needs hardware/wiring dependent implementation
    Final range:
         (0,0): top-left 
         (self.WCA_WIDTH-1, self.WCA_HEIGHT-1): bottom-right
    '''
    if y%2 == 0:
        pos = (WIDTH*offset-x-1)+(HEIGHT*y)
    else:
        pos = HEIGHT*(y+offset-1)+x
    return pos

def setColorToAll(strip, color, offset=1):
    for i in range(offset*HEIGHT-1 if offset > 1 else 0, LED_COUNT):
        strip.setPixelColor(i, color)

def setColorBy2DCoordinates(strip, x, y, color, offset=1):
    '''
    Mapping coordinates to the wordclocks display
    Needs hardware/wiring dependent implementation
    Final range:
         (0,0): top-left
         (self.WCA_WIDTH-1, self.WCA_HEIGHT-1): bottom-right
    '''
    strip.setPixelColor(getStripIndexFrom2D(x,y, offset), color)

def show_time(strip):
    now = datetime.datetime.now()
    
    minute = int(now.minute/5.0 + 0.5)
      
    hour = now.hour%12 + (1 if minute >= 7 else 0)
    if now.hour == 12 and minute < 7:
        hour = 12
   
    if minute == 12:
        minute = 0
        
    taw_indices = prefix + \
            minutes[minute] + \
            list(hours[hour]) + \
            (full_hour if (minute == 0 and hour%12 != 0) else [])

    print(taw_indices)

    #Set all LEDs back to black
    setColorToAll(strip, Color(0,0,0))

    for i in range(len(taw_indices)):
        strip.setPixelColor(taw_indices[i], Color(255,255,255))

    strip.show()

def showText(strip, text, font=None, fg_color=None, bg_color=None, fps=8, count=1, offset=1):
        '''
        Display text on display
        '''
        if font     == None: font=os.path.join('/usr/share/fonts/truetype/freefont/','FreeSans.ttf')
        if fg_color == None: fg_color=Color(255,255,255)
        if bg_color == None: bg_color=Color(0,0,0)

        text = '    '+text+'    '

        fnt = fontdemo.Font(font, HEIGHT-offset+3 if offset > 1 else HEIGHT)
        text_width, text_height, text_max_descent = fnt.text_dimensions(text)
        text_as_pixel = fnt.render_text(text)

        print(text_width)
        print(text_as_pixel)
        
        # Display text count times
        for i in range(count):

            # Erase previous content
            setColorToAll(strip, bg_color, offset)

            # Assure here correct rendering, if the text does not fill the whole display
            render_range = WIDTH if WIDTH < text_width else text_width
            print(render_range)
            for y in range(text_height):
                for x in range(render_range):
                    setColorBy2DCoordinates(strip, x, y, fg_color if text_as_pixel.pixels[y * text_width + x ] else bg_color, offset)

            # Show first frame for 0.5 seconds
            strip.show()
            time.sleep(0.5)

            print(text_width - WIDTH + 1)
            # Shift text from left to right to show all.
            for cur_offset in range(text_width - WIDTH + 1):
                for y in range(text_height):
                    for x in range(WIDTH):
                        setColorBy2DCoordinates(strip, x, y, fg_color if text_as_pixel.pixels[y * text_width + x + cur_offset] else bg_color, offset)
                strip.show()
                time.sleep(1.0/fps)

def show_birthday(strip, name):
    setColorToAll(strip, Color(0,0,0))

    for i in range(len(happy_birthday)):
        strip.setPixelColor(happy_birthday[i], Color(255,255,255))

    strip.show()
    
    showText(strip, name, offset=7)

def set_brightness(strip, adc_value):
    brightness = 255 - ((adc_value - 1700) / 1000 * 8)
    print('adc_value ' + repr(adc_value))
    print('brightness ' + repr(brightness))
    
    #if (brightness != LED_BRIGHTNESS):
    if brightness > 255:
        brightness = 255
        
    strip.setBrightness(brightness)
    #strip.show()
    #   LED_BRIGHTNESS = brightness

if __name__ == '__main__':
    print(LED_BRIGHTNESS)
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()

    # Create an ADS1115 ADC (16-bit) instance.
    # adc = Adafruit_ADS1x15.ADS1115()
    
    prev_date = datetime.date(1900,1,1)
    prev_min = -1

    show_birthday_message = False
    birthday_name = ''

    try:
        while True:
        
            # adc_value = adc.read_adc(3, GAIN)
            # set_brightness(strip, adc_value)
            
            input_state = GPIO.input(GPIO_PIN_IN)
            if GPIO.input(GPIO_PIN_IN) == 0:
            #print "Button is pressed"
                time.sleep(2)
                if GPIO.input(GPIO_PIN_IN) == 0:
                    #print "Long Press"
                    setColorToAll(strip, Color(0,0,0))
                    strip.show()
                    GPIO.cleanup()
                    os.system("sudo shutdown -h now")
                
            # Get current date and time
            today = datetime.date.today()
            now = datetime.datetime.now()
            
            # Check, if a minute has passed (to render the new time)
            #if prev_min < now.minute:
            show_time(strip)
                    
            #    prev_min = -1 if now.minute == 59 else now.minute

            time.sleep(5)
    except KeyboardInterrupt:
        setColorToAll(strip, Color(0,0,0))
        strip.show()
        GPIO.cleanup()

