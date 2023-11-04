from machine import Pin
import neopixel
import settings


rgb_strip = neopixel.NeoPixel(Pin(settings.NEOPIXEL_PIN), 6)

full = 40   # RGB LCD brightness. 10=low, 255=max.
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



def set_rgb_pattern(rgbmode):
            
    if rgbmode == 0:	# off
        rgb_strip.fill((0,0,0))
        rgb_strip.write()

    elif rgbmode == 1:	# red
        rgb_strip.fill((full,0,0))
        rgb_strip.write()

    elif rgbmode == 2: # green
        rgb_strip.fill((0,full,0))
        rgb_strip.write()

    elif rgbmode == 3: # blue
        rgb_strip.fill((0,0,full))
        rgb_strip.write()

    elif rgbmode == 4: # yellow
        rgb_strip.fill((half,half,0))
        rgb_strip.write()

    elif rgbmode == 5: # cyan
        rgb_strip.fill((0,half,half))
        rgb_strip.write()

    elif rgbmode == 6: # magenta
        rgb_strip.fill((half,0,half))
        rgb_strip.write()

    elif rgbmode == 7: # amber
        rgb_strip.fill((50,6,0))
        rgb_strip.write()

    elif rgbmode == 8: # whiteish
        rgb_strip.fill((int(2.0*half), half, int(0.5*half)))
        rgb_strip.write()
        
    elif rgbmode == 9:   # rainbow
        hue = 0
        for i in range(0,6):
            rgb_strip.__setitem__(i,colourHSV(hue, 255, full))
            hue = hue + 10000         # difference of colurs between LEDs                    
        rgb_strip.write()

    elif rgbmode == 10:   # red/blue alternate
        colour1 = (full,0,0)
        colour2 = (0,0,full)
        rgb_strip.__setitem__(0,colour1)
        rgb_strip.__setitem__(1,colour2)
        rgb_strip.__setitem__(2,colour1)
        rgb_strip.__setitem__(3,colour2)
        rgb_strip.__setitem__(4,colour1)
        rgb_strip.__setitem__(5,colour2)
        rgb_strip.write()
                                    
 
 
 
