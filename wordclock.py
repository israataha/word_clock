import time
import datetime
from neopixel import *


# LED strip configuration:
LED_COUNT   = 144    # Number of LED pixels.
LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)
LED_BRIGHTNESS  = 250  # Set to 0 for darkest and 255 for brightest
LED_CHANNEL = 0
LED_STRIP = ws.WS2811_STRIP_GRB

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

full_hour= range(133,139)

#happy_birthday = list(range(36,41)) + list(range(52,60))

def show_time(strip):
    now = datetime.datetime.now()
    hour = now.hour%12 + (1 if now.minute/5 >= 7 else 0)
    minute = now.minute/5
    taw_indices = prefix + \
            minutes[minute] + \
            list(hours[hour]) + \
            (list(full_hour) if (minute == 0) else [])

    print(taw_indices)

    #Set all LEDs back to black
    for i in range(LED_COUNT)
        strip.setPixelColor(i, Color(0,0,0))

    for i in range(len(taw_indices))
        strip.setPixelColor(taw_indices[i], Color(255,255,255))

    strip.show()

if __name__ == '__main__':
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()

    prev_min = -1

    while True:
        # Get current time
        now = datetime.datetime.now()
        # Check, if a minute has passed (to render the new time)
        if prev_min < now.minute:
            # Set background color
            show_time(strip)
            prev_min = -1 if now.minute == 59 else now.minute
    
