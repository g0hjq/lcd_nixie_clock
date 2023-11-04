#=============================================================
#=============================================================
#=============================================================
# Settings and global variables, shared by all python modules
#=============================================================
#=============================================================
#=============================================================

import json

# GPIO Pin Numbers for LCD
RST_PIN    = 12
CLK_PIN    = 10
DIN_PIN    = 11
DC_PIN     = 8
CS1_PIN    = 2
CS2_PIN    = 3
CS3_PIN    = 4
BL_PIN     = 13

# GPIO pins for push buttons
MODE_PIN  = 17
LEFT_PIN  = 16
RIGHT_PIN = 15

# Other GPIO Pins
BUZZER_PIN = 14
NEOPIXEL_PIN = 22
RTC_1HZ_PIN = 18


# Global Variables
settings = {
    "alarm_hour": 7,
    "alarm_min": 30,
    "alarm_on": 0,
    "font": 1,
    "brightness" : 5,
    "rgb_mode": 1,
    "24_hour" : 1,
    "show_secs" : 1,
    "adjust_timing" : 128
}

tick = True


#==============================================================================
#==============================================================================
#==============================================================================
# Functions to Read and write the Settings File "settings.json" on eeprom
#==============================================================================
#==============================================================================
#==============================================================================

# Save all settings to "disk".
def save_settings():
    with open("settings.json", "w") as f:
        json.dump(settings, f)
 
 
# Load all settings from "disk"
def load_settings():
    global settings
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
    except:
        print("Unable to load settings.json . Creating new file")
        save_settings()


# Retrieve a single setting value from memory
def get_setting(key):
    if key in settings:
        return int(settings[key])
    else:
        raise Exception("Key '" + key + "' not found in settings. Delete file settings.json and try again")


# Update a single setting value in memory and "disk"
def save_setting(key,value):
    if key in settings:
        settings[key] = value
        save_settings()
    else:
        raise Exception("Key '" + key + "' not found in settings. Delete file settings.json and try again")

 
