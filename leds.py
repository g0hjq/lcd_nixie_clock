#=========================================================================================    
# This code runs on the second core of the Raspberry Pi Pico.
#
# Its job is to animate the neopixel LEDs and sound the alarm buzzer in the background
#
# Communication with the main thread is through the global variables
#    led_mode
#    led_mode_changed
#    alarm_soundings
#    settings
#=========================================================================================    

from machine import Pin
import neopixel
import settings


led_strip = neopixel.NeoPixel(Pin(settings.NEOPIXEL_PIN), 6)

full = 50
half = int(full / 2)
    
    
#-----------------------------------------------------------------------------
# Converts HSV color to rgb tuple and returns it.
# The logic is almost the same as in Adafruit NeoPixel library:
# https://github.com/adafruit/Adafruit_NeoPixel so all the credits for that
# go directly to them (license: https://github.com/adafruit/Adafruit_NeoPixel/blob/master/COPYING)
#    
# hue: Hue component. Should be on interval 0..65535
# sat: Saturation component. Should be on interval 0..255
# val: Value component. Should be on interval 0..255
# returns: (r, g, b) tuple
#-----------------------------------------------------------------------------
def colourHSV(hue, sat, val):
    """
    """
    if hue >= 65536:
        hue %= 65536

    hue = (hue * 1530 + 32768) // 65536
    if hue < 510:
        b = 0
        if hue < 255:
            r = 255
            g = hue
        else:
            r = 510 - hue
            g = 255
    elif hue < 1020:
        r = 0
        if hue < 765:
            g = 255
            b = hue - 510
        else:
            g = 1020 - hue
            b = 255
    elif hue < 1530:
        g = 0
        if hue < 1275:
            r = hue - 1020
            b = 255
        else:
            r = 255
            b = 1530 - hue
    else:
        r = 255
        g = 0
        b = 0

    v1 = 1 + val
    s1 = 1 + sat
    s2 = 255 - sat

    r = ((((r * s1) >> 8) + s2) * v1) >> 8
    g = ((((g * s1) >> 8) + s2) * v1) >> 8
    b = ((((b * s1) >> 8) + s2) * v1) >> 8

    return r, g, b



def set_led_pattern(ledmode):
            
    if ledmode == 0:	# off
        led_strip.fill((0,0,0))
        led_strip.write()

    elif ledmode == 1:	# red
        led_strip.fill((full,0,0))
        led_strip.write()

    elif ledmode == 2: # green
        led_strip.fill((0,full,0))
        led_strip.write()

    elif ledmode == 3: # blue
        led_strip.fill((0,0,full))
        led_strip.write()

    elif ledmode == 4: # yellow
        led_strip.fill((half,half,0))
        led_strip.write()

    elif ledmode == 5: # cyan
        led_strip.fill((0,half,half))
        led_strip.write()

    elif ledmode == 6: # magenta
        led_strip.fill((half,0,half))
        led_strip.write()

    elif ledmode == 7: # amber
        led_strip.fill((50,6,0))
        led_strip.write()

    elif ledmode == 8: # whiteish
        led_strip.fill((int(2.0*half), half, int(0.5*half)))
        led_strip.write()
        
    elif ledmode == 9:   # rainbow
        hue = 0
        for i in range(0,6):
            led_strip.__setitem__(i,colourHSV(hue, 255, full))
            hue = hue + 10000         # difference of colurs between LEDs                    
        led_strip.write()

    elif ledmode == 10:   # red/blue alternate
        colour1 = (full,0,0)
        colour2 = (0,0,full)
        led_strip.__setitem__(0,colour1)
        led_strip.__setitem__(1,colour2)
        led_strip.__setitem__(2,colour1)
        led_strip.__setitem__(3,colour2)
        led_strip.__setitem__(4,colour1)
        led_strip.__setitem__(5,colour2)
        led_strip.write()
                                    
 
 
 
