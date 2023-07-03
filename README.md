# lcd_nixie_clock
Pseudo Nixie LCD clock in Micropython for the Waveshare kit and Pi Pico

This project contains the MicroPython code for a Raspberry Pi Pico RP2040 to drive the Waveshare Programmable RGB Pseduo Nixie Tube clock. See https://www.waveshare.com/lcd-clock-a.htm

![image](https://github.com/g0hjq/lcd_nixie_clock/assets/37076748/554df180-edf5-486d-a488-68c63047eff1)

## Features
- Shows the time in 12 or 24 hour format
- Shows time in on the LCDs in the style of Nixie tubes. Other types of display may be shown
- Shows Hours, minutes and seconds, or Hours, Minutes and Alarm status
- Alarm sounds the buzzer and flashes the LED neopixels
- Controlable brightness
- Ten preset RGB lighting patterns. More may be added if desired

## Limitations
- Due to the lmiited amount of eeprom in the Pi Pico, only one font may be loaded at any one time, however alternative .raw font files may be created and uploaded via Thonny. 
- The temperature and humidity from the BME280 sensor are not displayed. The sensor is on the PCB, inside an unventilated case, so is never going to be able to give accurate readings.
- Due to the way the LCD chip enable pins and DC pins are wired, it is not possible to use the standard Adafruit driver libraries. This uses modified versions of the Waveshare 1.14" python examples to drive all 6 LCDs. As it is written in Micropython, the performance is not optimum, but adequate for this project
- I wanted to animate the RGB LED lighting in the RP2040's second core, but was unable to do this reliably. It would often crash after an hour or so. Maybe this can be revisited some time.

## Font Files
- The ten images for the digits 0 to 9 are stored in .raw files. This is explained here: https://www.penguintutor.com/programming/picodisplayanimations . You can create your own set of font files as follows:
- Create a set of 10 image files at resolution 240 x 135 pixels.
- Rotate the images anticlockwise 90 degrees and save as .png files 0.png to 9.png
- Run the conversion program animation_convert.py. This will produce files 0.raw to 9.raw
- Use thonny to upload the .raw files to the root directory of the pi pico

## Files
- main.py : The main program file in Micropython
- ds3231.py : Driver for the DS3231 real time clock chip
- display.py : LCD driver for the Waveshare ST7789 1.14" 240x134 pixel LCD. Also includes a 5x8 ASCII text font which is shown magnified 4x
- leds.py : Controls the RGB neopixel LEDs behind each digit. Consider adding more effects and/or animations, maybe running as a seperate thread in the second core.
- setings.py : Saves and retrieves the alarm time, display mode and other setting values in the settings.json file below.
- settings.json : Contains the setting values. This file is written to every time one of the clock settings is changed. settings.json will be created automatically if it does not exist
