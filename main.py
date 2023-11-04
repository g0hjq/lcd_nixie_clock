import time
from machine import Pin,PWM

import settings
import display
import ds3231
import leds


#=======================================================================
#=======================================================================
# Helper Functions
#=======================================================================
#=======================================================================


def rtc_1hz_interrupt(pin):
    global tick
    tick = True
    

def get_button():
    if (btn_mode_pin.value()):
        return "M"
    
    if (btn_left_pin.value()):
        return "L"
    
    if (btn_right_pin.value()):
        return "R"
    
    else:
        return None

    
    
def adjust_simple_setting(setting_name, min_value, max_value, display_function):
    value = settings.get_setting(setting_name)
    new_value, timeout = set(value, min_value, max_value, display_function)
    settings.save_setting(setting_name, new_value)

    return new_value, timeout


# Displays a decimal number at the specified position on the LCDs
def display_int(number, position, digits):
    for i in range(position+digits-1, position-1, -1):
        LCD.select_digit(i)
        LCD.display_digit(number%10)
        number = number / 10
        


# Allows the user to change a setting value with the up and down buttons.
#
# Returns the new value and True if no button pressed after a few seconds
# or the new value and False if the mode button is pressed
#
# Calls the callback display_function each time the value is changed to show it on
# the LCDs in whatever format is appropriate for the data type
def set(initial_value, min_value, max_value, display_function):
    new_value = initial_value
    previous_value = -1
    start_time = time.ticks_ms() 
    
    while True:

        # If a setting has changed. call the supplied function to display the new setting 
        if (new_value != previous_value):
            if (display_function):
                display_function(new_value)
                time.sleep(0.2)

            previous_value = new_value            

        # Respond to any button pressed
        btn = get_button()
                    
        if (btn == "L"):  # UP Button Pressed. Increment the value
            start_time = time.ticks_ms() 
            new_value = new_value+1
            if (new_value > max_value):
                new_value = min_value
                
        elif (btn == "R"):  # DOWN button pressed. Decrement the value
            start_time = time.ticks_ms() 
            new_value = new_value-1
            if (new_value < min_value):
                new_value = max_value
                
        elif (btn == "M"):  # Mode Button Pressed. Return
            break

        else:
            time.sleep(0.1)
        
        # if no buttons pressed for a while, timeout and return
        if time.ticks_ms() > (start_time + 5000): # 5 seconds
            return new_value, True
    
    return new_value, False


#===================================================================
#===================================================================
#===================================================================
# Callback functions used when changing settings
#===================================================================
#===================================================================
#===================================================================

def fn_display_brightness(value):
    LCD.set_brightness(value)        
    display_int(value,4,2)
    

def fn_display_rgb_mode(value):
    leds.set_rgb_pattern(value)
    display_int(value,4,2)
  
  
def fn_display_true_false(value):
    display_int(value,5,1)
  
  
def fn_display_12_24(value):
    if value==0:
        display_int(12,4,2)
    else:
        display_int(24,4,2)


def fn_display_font(value):
    LCD.set_font(value)
    display_int(value,4,2)
    LCD.select_digit(0)
    LCD.display_text(mode)

    
def fn_display_hour(value):
    display_int(value,2,2)
    
    
def fn_display_min(value):
    display_int(value,4,2)
  
  
def fn_display_sec(value):
    display_int(value,4,2)
  

def fn_display_adjust_timing(value):    
    RTC.Set_Timing(value)
    display_int(value,3,3)
   
   
#==============================================================================
#==============================================================================
#==============================================================================
# Functions used to change the clock's settings
#==============================================================================
#==============================================================================
#==============================================================================
      
def set_alarm_on_off():
    _, timeout = adjust_simple_setting("alarm_on", 0, 1, fn_display_true_false)
    
    if (timeout):
        return("Time")
    else:
        return("Set Alarm Hour")
        

def set_alarm_hour():
    _, timeout = adjust_simple_setting("alarm_hour", 0, 23, fn_display_hour)
    
    if (timeout):
        return("Time")
    else:
        return("Set Alarm Min")
        
        
def set_alarm_min():
    _, timeout = adjust_simple_setting("alarm_min", 0, 59, fn_display_min)
    
    if (timeout):
        return("Time")
    else:
        return("Set Hour")
        
        
def set_hour():
    hour,_,_ = RTC.Read_Time()
    new_value, timeout = set(hour, 0, 23, fn_display_hour)
    RTC.Set_Time_Hour(new_value)
    
    if (timeout):
        return("Time")
    else:
        return("Set Min")
        
        
def set_minute():
    _,minute,_ = RTC.Read_Time()
    new_value, timeout = set(minute, 0, 59, fn_display_min)
    RTC.Set_Time_Min(new_value)
    
    if (timeout):
        return("Time")
    else:
        return("Set Second")

        
def set_second():
    _,_,second = RTC.Read_Time()
    old_value = second
    new_value, timeout = set(second, 0, 59, fn_display_sec)
    if new_value != old_value:
        RTC.Set_Time_Sec(new_value)
    
    if (timeout):
        return("Time")
    else:
        return("Set Font")
        
def set_font():
    _, timeout = adjust_simple_setting("font", 1, 9, fn_display_font)
    
    if (timeout):
        return("Time")
    else:
        return("Set Light Level")


def set_brightness():    
    _, timeout = adjust_simple_setting("brightness", 1, 10, fn_display_brightness)
    
    if (timeout):
        return("Time")
    else:
        return("Set RGB Mode")


def set_rgb_mode():
    
    _, timeout = adjust_simple_setting("rgb_mode", 0, 10, fn_display_rgb_mode)

    if (timeout):
        return("Time")
    else:
        return("Set 12/24 Hours")


def set_12_24():
    _, timeout = adjust_simple_setting("24_hour", 0, 1, fn_display_12_24)
    
    if (timeout):
        return("Time")
    else:
        return("Show Secs")


def set_show_seconds():
    _, timeout = adjust_simple_setting("show_secs", 0, 1, fn_display_true_false)
    if (timeout):
        return("Time")
    else:
        return("Adjust Timing")


def set_adjust_timing():
    adjust_simple_setting("adjust_timing", 0, 255, fn_display_adjust_timing)
    return("Time")



#====================================================================
#====================================================================
#====================================================================
# Display the current time until a button is pressed
#====================================================================
#====================================================================
#====================================================================

def show_digit_if_changed(num, pos):
    global previous_digits
    
    if num != previous_digits[pos]:
        
        LCD.select_digit(pos)

        if num is None:
            LCD.fill(LCD.black)
            previous_digits[pos] = None
        else:
            x = int(num)
            LCD.display_digit(x)
            previous_digits[pos] = x
        
        LCD.show()            

    
# 4-digit mode : display hours, minutes and flashing colon
def show_time_4_digits(hr, min, sec):

    # Show minute and alarm on/off and alarm time once a minute
    x = int(min%10)
    
    if (x != previous_digits[4]):
        LCD.select_digit(5)
        if bool(settings.get_setting("alarm_on")):            
            LCD.display_text("Alarm ON  {0}:{1:02d}".
                format(settings.get_setting("alarm_hour"),
                       settings.get_setting("alarm_min")))
        else:
            LCD.display_text("Alarm OFF")
        
        LCD.select_digit(4)
        previous_digits[4] = x
        LCD.display_digit(x)
        
    # Show tens of minute
    show_digit_if_changed(min/10, 3)

    # show blinking colon
    LCD.show_colon(2, sec%2)

    # show hour. Suppress leading zero if in 12 hour mode
    show_digit_if_changed(hr%10, 1)
    
    if (settings.get_setting("24_hour")==1) or (hr>9):
        show_digit_if_changed(hr/10, 0)
    else:
        show_digit_if_changed(None, 0)

    LCD.show()

        
        
# 4-digit mode : display hours, minutes and seconds
def show_time_6_digits(hr, mins, sec):

    show_digit_if_changed(sec%10, 5)
    show_digit_if_changed(sec/10, 4)
    show_digit_if_changed(mins%10, 3)
    show_digit_if_changed(mins/10, 2)
    show_digit_if_changed(hr%10, 1)
    show_digit_if_changed(hr/10, 0)



#=======================================================================
#=======================================================================
#=======================================================================
# Displays the current time and sounds the alarm if necessary
#=======================================================================
#=======================================================================
#=======================================================================
def show_time():
    global tick
    global previous_digits
    
    sound_alarm = False    
    tick = True
    previous_digits = [None,None,None,None,None,None]
    
    while True:
        
        if tick:  # wait for the next 1 second tick
            
            tick = False
            hr24,min,sec = RTC.Read_Time()

            # Check if it's time to sound the alarm.
            if (sec == 0) and \
               (settings.get_setting("alarm_on") == 1) and \
               (settings.get_setting("alarm_hour") == hr24) and \
               (settings.get_setting("alarm_min") == min):                    
                print("WAKEY WAKEY!")
                sound_alarm = True
                                
            if sound_alarm:
                if (sec % 2) == 0:
                    leds.rgb_strip.fill((255,255,255))
                else:
                    leds.rgb_strip.fill((0,0,0))
                leds.rgb_strip.write()
                
                buzzer.duty_u16(32768)
                for i in range(0,4):
                    buzzer.freq(1500)
                    time.sleep(0.05)
                    buzzer.freq(2400)
                    time.sleep(0.05)
                buzzer.duty_u16(0)
                    
            # Display the current time
            hr = hr24
                
            if settings.get_setting("24_hour"):
                # 24 hour clock. Show time as 0-23
                hr = hr24
            else:
                # 12 hour clock. Show time as 1-12
                hr = hr24 % 12                
                if (hr == 0):                
                    hr = 12

            if settings.get_setting("show_secs") == 1:            
                show_time_6_digits(hr,min,sec)
            else:
                show_time_4_digits(hr,min,sec)

            
        # Here would be a good place to animate the LEDs etc
        
        if sound_alarm:            
            if get_button() is not None:
                
                # Stop the alarm
                sound_alarm = False
                buzzer.duty_u16(0)
                leds.set_rgb_pattern(settings.get_setting("rgb_mode"))
                
                # Wait for button release
                while True:
                    time.sleep(0.2)
                    if get_button() is None:
                        break
                    
        else:
            if get_button() == "M":
                return("Alarm On/ Off")
                


#=======================================================================
#=======================================================================
#=======================================================================
# Main Body
#=======================================================================
#=======================================================================
#=======================================================================

settings.load_settings()
leds.set_rgb_pattern(settings.get_setting("rgb_mode"))

btn_mode_pin  = Pin(settings.MODE_PIN, Pin.IN)
btn_left_pin  = Pin(settings.LEFT_PIN, Pin.IN)
btn_right_pin = Pin(settings.RIGHT_PIN, Pin.IN)
rtc_1Hz_pin   = Pin(settings.RTC_1HZ_PIN, Pin.IN)

LCD = display.Display()
LCD.set_font(settings.get_setting("font"))

RTC = ds3231.DS3231(add = 0x68)
RTC.Set_Timing(settings.get_setting("adjust_timing"))

buzzer = PWM(Pin(settings.BUZZER_PIN, Pin.OUT))
buzzer.duty_u16(0)

# Set up the handler to recieve a regular interrupt on the 1Hz output from the DS3231
rtc_1Hz_pin.irq(trigger=Pin.IRQ_RISING, handler=rtc_1hz_interrupt)


#===================================================================
# The main control loop starts here
#===================================================================
mode = "Time"
tick = True


while True:
    LCD.set_brightness(settings.get_setting("brightness"))
    LCD.clear()


    if (mode == "Time"):
        mode = show_time()
    else:
        LCD.select_digit(0)
        LCD.display_text(mode)

        if mode == "Alarm On/ Off":
            mode = set_alarm_on_off()
            
        elif mode == "Set Alarm Hour":
            mode = set_alarm_hour()
            
        elif mode == "Set Alarm Min":
            mode = set_alarm_min()
            
        elif mode == "Set Hour":
            mode = set_hour()
            
        elif mode == "Set Min":
            mode = set_minute()
            
        elif mode == "Set Second":
            mode = set_second()
            
        elif mode == "Set Font":
            mode = set_font()
            
        elif mode == "Set Light Level":
            mode = set_brightness()
            
        elif mode == "Set RGB Mode":
            mode = set_rgb_mode()
            
        elif mode == "Set 12/24 Hours":
            mode = set_12_24()
            
        elif mode == "Show Secs":
            mode = set_show_seconds()
            
        elif mode == "Adjust Timing":
            mode = set_adjust_timing()
            
        else:
            print("Unexpected mode :",mode)
            mode = "Time"
    
    
# The end.
