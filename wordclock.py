#import wordclock_display as wcd
#import time_as_words as taw
import time
import datetime

class wiring:
    # LED strip configuration:
    WCA_HEIGHT  = 12      # len(layout)             
    WCA_WIDTH   = 12      # len(layout[0])
    LED_COUNT   = WCA_HEIGHT*WCA_WIDTH    # Number of LED pixels.
    LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
    LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)
    brightness  = 20

class layout:
    def __init__(self):

        self.prefix = list(range(0,2)) + list(range(3,5)) # -> IT IS

        self.minutes=[[], \
            # -> FIVE PAST
            list(range(31,35)) + list(range(42,46)), \
            # -> TEN PAST
            list(range(8,11)) + list(range(42,46)), \
            # -> QUARTER PAST
            list(range(17,24)) + list(range(42,46)), \
            # -> TWENTY PAST
            list(range(24,30)) + list(range(42,46)), \
            # -> TWENTYFIVE PAST
            list(range(24,30)) + list(range(31,35)) + list(range(42,46)), \
            # -> HALF PAST
            list(range(12,16)) + list(range(42,46)), \
            # -> TWENTYFIVE TO
            list(range(24,30)) + list(range(31,35)) + list(range(48,50)), \
            # -> TWENTY TO
            list(range(24,30)) + list(range(48,50)), \
            # -> QUARTER TO
            list(range(17,24)) + list(range(48,50)), \
            # -> TEN TO
            list(range(8,11)) + list(range(48,50)), \
            # -> FIVE TO
            list(range(31,35)) + list(range(48,50)) ]

        self.hours= [range(124,132), \
            # -> ONE
            range(68,71), \
            # -> TWO
            range(108,111), \
            # -> THREE
            range(114,119), \
            # -> FOUR
            range(97,101), \
            # -> FIVE
            range(72,76), \
            # -> SIX
            range(111,114), \
            # -> SEVEN
            range(77,82), \
            # -> EIGHT
            range(102,107), \
            # -> NINE
            range(120,124), \
            # -> TEN
            range(92,95),\
            # -> ELEVEN
            range(61,67), \
            # -> NOON
            range(140,144)]

        self.full_hour= range(133,139)

        #self.happy_birthday = list(range(36,41)) + list(range(52,60))

class time_display:
    def __init__(self):
        self.prefix = list(range(0,2)) + list(range(3,5)) # -> IT IS

        self.minutes=[[], \
            # -> FIVE PAST
            list(range(31,35)) + list(range(42,46)), \
            # -> TEN PAST
            list(range(8,11)) + list(range(42,46)), \
            # -> QUARTER PAST
            list(range(17,24)) + list(range(42,46)), \
            # -> TWENTY PAST
            list(range(24,30)) + list(range(42,46)), \
            # -> TWENTYFIVE PAST
            list(range(24,30)) + list(range(31,35)) + list(range(42,46)), \
            # -> HALF PAST
            list(range(12,16)) + list(range(42,46)), \
            # -> TWENTYFIVE TO
            list(range(24,30)) + list(range(31,35)) + list(range(48,50)), \
            # -> TWENTY TO
            list(range(24,30)) + list(range(48,50)), \
            # -> QUARTER TO
            list(range(17,24)) + list(range(48,50)), \
            # -> TEN TO
            list(range(8,11)) + list(range(48,50)), \
            # -> FIVE TO
            list(range(31,35)) + list(range(48,50)) ]

        self.hours= [range(124,132), \
            # -> ONE
            range(68,71), \
            # -> TWO
            range(108,111), \
            # -> THREE
            range(114,119), \
            # -> FOUR
            range(97,101), \
            # -> FIVE
            range(72,76), \
            # -> SIX
            range(111,114), \
            # -> SEVEN
            range(77,82), \
            # -> EIGHT
            range(102,107), \
            # -> NINE
            range(120,124), \
            # -> TEN
            range(92,95),\
            # -> ELEVEN
            range(61,67), \
            # -> NOON
            range(140,144)]

        self.full_hour= range(133,139)

    def run(self):
        prev_min = -1

        while True:
            # Get current time
            now = datetime.datetime.now()
            # Check, if a minute has passed (to render the new time)
            if prev_min < now.minute:
                # Set background color
                self.show_time()
                prev_min = -1 if now.minute == 59 else now.minute

    def show_time(self):
        now = datetime.datetime.now()
        hour = now.hour%12 + (1 if now.minute/5 >= 7 else 0)
        minute = round(now.minute/5)
        taw_indices = self.prefix + \
                self.minutes[minute] + \
                list(self.hours[hour]) + \
                (list(self.full_hour) if (minute == 0) else [])

        print(taw_indices)

class wordclock:
    def __init__(self):
        # Create object to display any content on the wordclock display
        # Its implementation depends on your (individual) wordclock layout/wiring
        #self.wcd = wcd.wordclock_display()
        x = 2

    def run(self):
        # Run the wordclock forever
        while True:
            #taw.time_as_words().run(self.wcd)
            time_display().run()
            #print("Hello World!")

if __name__ == '__main__':
    word_clock = wordclock()
    word_clock.run()