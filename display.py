#===============================================
# LCD driver for the Waveshare ST7789 1.14"
# 240x134 pixel LCD
#
# Note that this is rotated 90 degrees anticlockwise,
# so the screen coordinates when drawing text are:
#
#
#        0,239 *================* 133,239
#              |                |
#              |                |
#              |                |
#              |                |
#              |                |
#              |                |
#              |                |
#              |                |
#              |                |
#              |                |
#              |                |
#          0,0 *================* 133,0
#
# However, due to the rotation, native framebuff
# coordinates have the x and y axis swapped.
#
# By Gary Bleads, June 2023    gary@bleads.co.uk
#===============================================


from machine import Pin,SPI,PWM
import framebuf
import time
import settings


# ===========Start of FONTS Section=========================
# Standard ASCII 5x8 font
# https://gist.github.com/tdicola/229b3eeddc12d58fb0bc724a9062aa05
FONT_HEIGHT = 8
FONT_WIDTH = 5
FONT = bytes([
    0x00, 0x00, 0x00, 0x00, 0x00, # <space>
    0x3E, 0x5B, 0x4F, 0x5B, 0x3E,
    0x3E, 0x6B, 0x4F, 0x6B, 0x3E,
    0x1C, 0x3E, 0x7C, 0x3E, 0x1C,
    0x18, 0x3C, 0x7E, 0x3C, 0x18,
    0x1C, 0x57, 0x7D, 0x57, 0x1C,
    0x1C, 0x5E, 0x7F, 0x5E, 0x1C,
    0x00, 0x18, 0x3C, 0x18, 0x00,
    0xFF, 0xE7, 0xC3, 0xE7, 0xFF,
    0x00, 0x18, 0x24, 0x18, 0x00,
    0xFF, 0xE7, 0xDB, 0xE7, 0xFF,
    0x30, 0x48, 0x3A, 0x06, 0x0E,
    0x26, 0x29, 0x79, 0x29, 0x26,
    0x40, 0x7F, 0x05, 0x05, 0x07,
    0x40, 0x7F, 0x05, 0x25, 0x3F,
    0x5A, 0x3C, 0xE7, 0x3C, 0x5A,
    0x7F, 0x3E, 0x1C, 0x1C, 0x08,
    0x08, 0x1C, 0x1C, 0x3E, 0x7F,
    0x14, 0x22, 0x7F, 0x22, 0x14,
    0x5F, 0x5F, 0x00, 0x5F, 0x5F,
    0x06, 0x09, 0x7F, 0x01, 0x7F,
    0x00, 0x66, 0x89, 0x95, 0x6A,
    0x60, 0x60, 0x60, 0x60, 0x60,
    0x94, 0xA2, 0xFF, 0xA2, 0x94,
    0x08, 0x04, 0x7E, 0x04, 0x08, # UP
    0x10, 0x20, 0x7E, 0x20, 0x10, # Down
    0x08, 0x08, 0x2A, 0x1C, 0x08, # Right
    0x08, 0x1C, 0x2A, 0x08, 0x08, # Left
    0x1E, 0x10, 0x10, 0x10, 0x10,
    0x0C, 0x1E, 0x0C, 0x1E, 0x0C,
    0x30, 0x38, 0x3E, 0x38, 0x30,
    0x06, 0x0E, 0x3E, 0x0E, 0x06,
    0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x5F, 0x00, 0x00,
    0x00, 0x07, 0x00, 0x07, 0x00,
    0x14, 0x7F, 0x14, 0x7F, 0x14,
    0x24, 0x2A, 0x7F, 0x2A, 0x12,
    0x23, 0x13, 0x08, 0x64, 0x62,
    0x36, 0x49, 0x56, 0x20, 0x50,
    0x00, 0x08, 0x07, 0x03, 0x00,
    0x00, 0x1C, 0x22, 0x41, 0x00,
    0x00, 0x41, 0x22, 0x1C, 0x00,
    0x2A, 0x1C, 0x7F, 0x1C, 0x2A,
    0x08, 0x08, 0x3E, 0x08, 0x08,
    0x00, 0x80, 0x70, 0x30, 0x00,
    0x08, 0x08, 0x08, 0x08, 0x08,
    0x00, 0x00, 0x60, 0x60, 0x00,
    0x20, 0x10, 0x08, 0x04, 0x02,
    0x3E, 0x51, 0x49, 0x45, 0x3E,
    0x00, 0x42, 0x7F, 0x40, 0x00,
    0x72, 0x49, 0x49, 0x49, 0x46,
    0x21, 0x41, 0x49, 0x4D, 0x33,
    0x18, 0x14, 0x12, 0x7F, 0x10,
    0x27, 0x45, 0x45, 0x45, 0x39,
    0x3C, 0x4A, 0x49, 0x49, 0x31,
    0x41, 0x21, 0x11, 0x09, 0x07,
    0x36, 0x49, 0x49, 0x49, 0x36,
    0x46, 0x49, 0x49, 0x29, 0x1E,
    0x00, 0x00, 0x14, 0x00, 0x00,
    0x00, 0x40, 0x34, 0x00, 0x00,
    0x00, 0x08, 0x14, 0x22, 0x41,
    0x14, 0x14, 0x14, 0x14, 0x14,
    0x00, 0x41, 0x22, 0x14, 0x08,
    0x02, 0x01, 0x59, 0x09, 0x06,
    0x3E, 0x41, 0x5D, 0x59, 0x4E,
    0x7C, 0x12, 0x11, 0x12, 0x7C, # A
    0x7F, 0x49, 0x49, 0x49, 0x36,
    0x3E, 0x41, 0x41, 0x41, 0x22,
    0x7F, 0x41, 0x41, 0x41, 0x3E,
    0x7F, 0x49, 0x49, 0x49, 0x41,
    0x7F, 0x09, 0x09, 0x09, 0x01,
    0x3E, 0x41, 0x41, 0x51, 0x73,
    0x7F, 0x08, 0x08, 0x08, 0x7F,
    0x00, 0x41, 0x7F, 0x41, 0x00,
    0x20, 0x40, 0x41, 0x3F, 0x01,
    0x7F, 0x08, 0x14, 0x22, 0x41,
    0x7F, 0x40, 0x40, 0x40, 0x40,
    0x7F, 0x02, 0x1C, 0x02, 0x7F,
    0x7F, 0x04, 0x08, 0x10, 0x7F,
    0x3E, 0x41, 0x41, 0x41, 0x3E,
    0x7F, 0x09, 0x09, 0x09, 0x06,
    0x3E, 0x41, 0x51, 0x21, 0x5E,
    0x7F, 0x09, 0x19, 0x29, 0x46,
    0x26, 0x49, 0x49, 0x49, 0x32,
    0x03, 0x01, 0x7F, 0x01, 0x03,
    0x3F, 0x40, 0x40, 0x40, 0x3F,
    0x1F, 0x20, 0x40, 0x20, 0x1F,
    0x3F, 0x40, 0x38, 0x40, 0x3F,
    0x63, 0x14, 0x08, 0x14, 0x63,
    0x03, 0x04, 0x78, 0x04, 0x03,
    0x61, 0x59, 0x49, 0x4D, 0x43,
    0x00, 0x7F, 0x41, 0x41, 0x41,
    0x02, 0x04, 0x08, 0x10, 0x20,
    0x00, 0x41, 0x41, 0x41, 0x7F,
    0x04, 0x02, 0x01, 0x02, 0x04,
    0x40, 0x40, 0x40, 0x40, 0x40,
    0x00, 0x03, 0x07, 0x08, 0x00,
    0x20, 0x54, 0x54, 0x78, 0x40,
    0x7F, 0x28, 0x44, 0x44, 0x38,
    0x38, 0x44, 0x44, 0x44, 0x28,
    0x38, 0x44, 0x44, 0x28, 0x7F,
    0x38, 0x54, 0x54, 0x54, 0x18,
    0x00, 0x08, 0x7E, 0x09, 0x02,
    0x18, 0xA4, 0xA4, 0x9C, 0x78,
    0x7F, 0x08, 0x04, 0x04, 0x78,
    0x00, 0x44, 0x7D, 0x40, 0x00,
    0x20, 0x40, 0x40, 0x3D, 0x00,
    0x7F, 0x10, 0x28, 0x44, 0x00,
    0x00, 0x41, 0x7F, 0x40, 0x00,
    0x7C, 0x04, 0x78, 0x04, 0x78,
    0x7C, 0x08, 0x04, 0x04, 0x78,
    0x38, 0x44, 0x44, 0x44, 0x38,
    0xFC, 0x18, 0x24, 0x24, 0x18,
    0x18, 0x24, 0x24, 0x18, 0xFC,
    0x7C, 0x08, 0x04, 0x04, 0x08,
    0x48, 0x54, 0x54, 0x54, 0x24,
    0x04, 0x04, 0x3F, 0x44, 0x24,
    0x3C, 0x40, 0x40, 0x20, 0x7C,
    0x1C, 0x20, 0x40, 0x20, 0x1C,
    0x3C, 0x40, 0x30, 0x40, 0x3C,
    0x44, 0x28, 0x10, 0x28, 0x44,
    0x4C, 0x90, 0x90, 0x90, 0x7C,
    0x44, 0x64, 0x54, 0x4C, 0x44,
    0x00, 0x08, 0x36, 0x41, 0x00,
    0x00, 0x00, 0x77, 0x00, 0x00,
    0x00, 0x41, 0x36, 0x08, 0x00,
    0x02, 0x01, 0x02, 0x04, 0x02,
    0x3C, 0x26, 0x23, 0x26, 0x3C,
    0x1E, 0xA1, 0xA1, 0x61, 0x12
])



#=================================================================
#=================================================================
#=================================================================
# LCD Display Class. Based on the Waveshare 1.14" example
#=================================================================
#=================================================================
#=================================================================
class Display(framebuf.FrameBuffer):


    # Constructor
    def __init__(self):

        self.width = 240
        self.height = 135
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        self.black =   0x0000
        self.amber =   0x07FC
        self.yellow=   0x07FF
        self.text_fg = self.amber
        #self.text_bg = 0x0120
        self.text_bg = self.black
        
        self.selected_digit = 0;
        self.cs1 = Pin(settings.CS1_PIN,Pin.OUT)
        self.cs2 = Pin(settings.CS2_PIN,Pin.OUT)
        self.cs3 = Pin(settings.CS3_PIN,Pin.OUT)
        self.rst = Pin(settings.RST_PIN,Pin.OUT)        
        self.bl  = Pin(settings.BL_PIN)        
        
        self.pwm = PWM(self.bl)
        self.pwm.freq(1000)
        self.set_backlight(100)
        
        # Use Hardware SPI for speed. 
        self.spi = SPI(1,
                       25_000_000,
                       polarity=0,
                       phase=0,
                       sck=Pin(settings.CLK_PIN),
                       mosi=Pin(settings.DIN_PIN),
                       miso=None)
        
         # this has to be after setting up SPI as the LCDs DC pin has been wired to the SPI1 miso input
        self.dc = Pin(settings.DC_PIN,Pin.OUT)
        self.dc.value(1)
        
        # Set up the frame buffer
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        
        # Wiggle the LCD reset line
        self.reset_all()
        
        # Reset all digits
        for digit in range(0,6):
            self.select_digit(digit)
            self.init()
            
        self.clear()
        

    # Change the backlight level from 0 to 10
    def set_backlight(self, percent):        
        if (percent < 0):
            percent = 0
            
        if (percent > 10):
            percent = 10            
            
        self.pwm.duty_u16(6550*percent)
    
    
    # Selects the current digit from 0 (left) to 5 (right)
    def select_digit(self, num):
        global selected_digit
        self.selected_digit = 5-num
         

    # chip select one LCD
    def cs_l(self): 
        self.cs1.value(self.selected_digit&0x01)
        self.cs2.value((self.selected_digit>>1)&0x01)
        self.cs3.value((self.selected_digit>>2)&0x01)
                
                
    # release cip select for all LCDs
    def cs_h(self):
        self.cs1.value(1)
        self.cs2.value(1)
        self.cs3.value(1)


    #  Write a single command byte to the current LCD
    def write_cmd(self, cmd):
        self.cs_h()
        self.dc(0)
        self.cs_l()
        self.spi.write(bytearray([cmd]))
        self.cs_h()


    #  Write a single data byte to the current LCD
    def write_data(self, buf):
        self.cs_h()
        self.dc(1)
        self.cs_l()
        self.spi.write(bytearray([buf]))
        self.cs_h()

    # Wiggle the LCD reset pins
    def reset_all(self):
        self.rst(1)
        time.sleep(0.01)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)
        time.sleep(0.01)


    # Initialise the currently selected LCD
    def init(self):
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)
        self.write_cmd(0x11)
        self.write_cmd(0x29)


    # Sends the entire frame buffer to the currently selected LCD
    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)
        
        self.write_cmd(0x2C)
        
        self.cs_h()
        self.dc(1)
        self.cs_l()
        self.spi.write(self.buffer)
        self.cs_h()
        

    # Clears all digits to black
    def clear (self):
        for d in range(0,6):
            self.select_digit(d)
            self.fill(self.black)
            self.show()


    # Displays a single character.
    # The coordinates are for the bottom left of the character
    def print_char(self,letter, left, top, col):
        code = ord(letter) * 5    # 5 bytes per character
        for ii in range(5):
            line = FONT[code + 4 - ii]
            for yy in range(8):
                if (line >> yy) & 0x1:
                    
                    # Draw the character 4x oversized
                    x0 = ii*4+109-left
                    x1 = x0+1
                    x2 = x1+1
                    x3 = x2+1
                    
                    y0 = yy*4+205-top
                    y1 = y0+1
                    y2 = y1+1
                    y3 = y2+1
                    
                    self.pixel(y0,x0,col) 
                    self.pixel(y1,x0,col) 
                    self.pixel(y2,x0,col) 
                    self.pixel(y3,x0,col) 
                    self.pixel(y0,x1,col) 
                    self.pixel(y1,x1,col) 
                    self.pixel(y2,x1,col) 
                    self.pixel(y3,x1,col) 
                    self.pixel(y0,x2,col) 
                    self.pixel(y1,x2,col) 
                    self.pixel(y2,x2,col) 
                    self.pixel(y3,x2,col) 
                    self.pixel(y0,x3,col) 
                    self.pixel(y1,x3,col) 
                    self.pixel(y2,x3,col) 
                    self.pixel(y3,x3,col) 


    # Displays up to six short words of text on the current LCD, centred X and Y
    def display_text(self,line):
        self.fill(self.text_bg)
        words = line.split(" ")
        height = len(words) * 32
        top = int(self.width/2 + height/2) - 20
        
        for word in words:
            width = len(word) * 24
            left = int((self.height - width)/2)-4
            
            for letter in word:
                self.print_char(letter, left, top, self.text_fg)
                left = left + 24
                
            top = top - 40        
        
        self.show()


    # Loads a number image file onto the selected LCD,
    # i.e. display_digit(0) displays file "0.raw"
    #
    # This is based on a binary image file (RGB565) with the same dimensions as the screen
    # updates the global display_buffer directly, reading the file in 1KB chunks for speed
    # The .raw image files must be preprocessed before uploading to the Pico.
    #
    # see https://www.penguintutor.com/programming/picodisplayanimations
    # for a python program to generate the files in the correct format.
    def display_digit (self, num):
        
        if num is not None:
            position = 0
            blocksize = 1024

            filename = str(int(num)) + ".raw"
            with open (filename, "rb") as file:
                chunk = file.read(blocksize)        
                while chunk:
                    self.buffer[position:position+len(chunk)] = chunk
                    position = position + len(chunk)
                    chunk = file.read(blocksize)
        else:
            print("Clearing digit ", self.selected_digit)
            self.fill(self.black)
        
        self.show()


