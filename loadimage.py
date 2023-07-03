import display
import time


# See https://www.penguintutor.com/programming/picodisplayanimations


# This is based on a binary image file (RGB565) with the same dimensions as the screen
# updates the global display_buffer directly
def blit_image_file (filename):
    
    position = 0
    blocksize = 1024
    
    with open (filename, "rb") as file:
        chunk = file.read(blocksize)        
        while chunk:
            #print(position)
            LCD.buffer[position:position+len(chunk)] = chunk
            chunk = file.read(blocksize)
            position = position + len(chunk)
    

LCD = display.Display()

for d in range(0,6):
    LCD.select_digit(d)
    LCD.fill(LCD.white)
    LCD.show()

print("Loading")

print("displaying")

starttime = time.ticks_ms()

LCD.select_digit(0)
blit_image_file ("0.raw")
LCD.show()

LCD.select_digit(1)
blit_image_file ("1.raw")
LCD.rect(0,0,240,135,LCD.white)
LCD.rect(1,1,238,133,LCD.white)
LCD.rect(2,2,236,131,LCD.white)
LCD.rect(3,3,234,129,LCD.white)

    
LCD.show()

LCD.select_digit(2)
blit_image_file ("2.raw")
LCD.show()

LCD.select_digit(3)
blit_image_file ("3.raw")
LCD.show()

LCD.select_digit(4)
blit_image_file ("4.raw")
LCD.show()

LCD.select_digit(5)
blit_image_file ("5.raw")
LCD.show()





endtime = time.ticks_ms()


print("time = {0} milliseconds".format(endtime - starttime));
        

# Do nothing - but continue to display the image


