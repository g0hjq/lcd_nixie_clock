from machine import Pin, I2C
import time

Seconds_Reg = 0x00
Min_Reg     = 0x01
Hour_Reg    = 0x02
Day_Reg     = 0x03
Date_Reg    = 0x04
Month_Reg   = 0x05
Year_Reg    = 0x06
Control_Reg = 0x0e
Status_Reg  = 0x0f
Aging_Reg   = 0x10
MSTemp_Reg  = 0x11
LSTemp_Reg  = 0x12

class DS3231:
    def __init__(self,add = 0x68):
        self.i2c = I2C(1)
        self.address = add 
        self.days_of_week = ["SUN","MON","TUE","WED","THU","FRI","SAT"]
        self.initialise()
                
    def Read_Reg(self, reg):
        return self.i2c.readfrom_mem(self.address, reg, 8)[0]
        
    def Write_Reg(self, reg, data):
        self.i2c.writeto_mem(self.address, reg, bytes([data]))
        
    def BCD_Convert_DEC(self, code):
        code1 =(((code & 0xf000)>>12) )*1000  + (((code & 0xf00)>>8) )*100  + (((code & 0xf0)>>4) )*10  + (code & 0x0f)
        return code1;
    
    def DEC_Convert_BCD(self, code):
        code1 = code%10 + ((int(code/10)%10) << 4) + ((int(code/100)%10) << 8) + ((int(code/1000)%10) << 12)
        return int(code1);
    

    def initialise(self):

        # Set true to reset the DS3212, loosing the time and settings
        force_initialise = False
        
        status = self.Read_Reg(Status_Reg)
        if force_initialise or (status & 0x80):
            print("Oscillator was stopped. Re-initialising")
            self.Write_Reg(Status_Reg,0b00000000)
            self.Write_Reg(Control_Reg,0b00000000)
        
            # Default time and date
            self.Set_Time(12,00,00)
            self.Set_Day(0)  # Sunday
            self.Set_Calendar(2023,01,01)

    
    # Fine Tune timekeeping
    #
    # Value = 0 to 256. 128 is the default.
    # The more lower the value, the faster the clock runs.
    #
    # Put an accurate frequency counter on the 1Hz signal on Pico Pin 24 (DS_INT)
    # to calibrate it exactly.
    def Set_Timing(self, trim):
        assert (trim >= 0) and (trim <= 255), "'Set Timing' trim value {0} is out of range".format(trim)

        b = bytes([trim-128 & 0xff])
        self.Write_Reg(Aging_Reg, b[0])    
        

    def Set_Calendar(self,Year,Month,Date):
        self.Set_Year_BCD(self.DEC_Convert_BCD(Year))
        self.Set_Month_BCD(self.DEC_Convert_BCD(Month))
        self.Set_Date_BCD(self.DEC_Convert_BCD(Date))
    
    
    def Read_Calendar(self):
        Calendar = [0,0,0]
        Calendar[0] = self.BCD_Convert_DEC(self.Read_Year_BCD())
        Calendar[1] = self.BCD_Convert_DEC(self.Read_Month_BCD())
        Calendar[2] = self.BCD_Convert_DEC(self.Read_Date_BCD())
        return Calendar
        
    '''Year_Reg     0x06                            '''
    def Read_Year_BCD(self):
        return self.Read_Reg(Year_Reg) | (0x20 << 8)
                
    def Set_Year_BCD(self, Year):
        self.Write_Reg(Year_Reg, Year & 0xff)            
        vai = self.Read_Reg(Month_Reg)
        self.Write_Reg(Month_Reg,  vai & 0x7f)
    
    '''Month_Reg     0x05                            '''
    def Read_Month_BCD(self):
        return self.Read_Reg(Month_Reg)&0x1f
        
    def Set_Month_BCD(self, Month):
        self.Write_Reg(Month_Reg, Month)
    
    '''Date_Reg     0x04                            '''
    def Read_Date_BCD(self):
        return self.Read_Reg(Date_Reg)&0x3f
        
    def Set_Date_BCD(self, Date):
        self.Write_Reg(Date_Reg, Date&0x3f)
            
    '''Day          0x03                            '''
    def Read_Day(self):
        return self.Read_Reg(Day_Reg)&0x07
    
    def Set_Day(self, vai):
       self.Write_Reg(Day_Reg, vai&0x07)
    
    '''Hour         0x02                            '''
    def Set_Time_Hour(self, hour):
        data = self.DEC_Convert_BCD(hour)
        self.Write_Reg(Hour_Reg, data & 0x3F) 
    
    def Read_Time_Hour(self):
        return self.BCD_Convert_DEC(self.Read_Reg(Hour_Reg) & 0x3F)

    '''Min            0x01                               '''
    def Set_Time_Min(self, min):
        data = self.DEC_Convert_BCD(min)
        self.Write_Reg(Min_Reg, data & 0x7F)
        
    def Read_Time_Min (self):
        return self.BCD_Convert_DEC(self.Read_Reg(Min_Reg)&0x7F)

    '''Sec            0x00                               '''
    def Set_Time_Sec(self, sec):
        data = self.DEC_Convert_BCD(sec)
        self.Write_Reg(Seconds_Reg,data & 0x7F)
    
    def Read_Time_Sec(self):
        return self.BCD_Convert_DEC(self.Read_Reg(Seconds_Reg)&0x7F)

    '''Time          0x02  01  00                        '''
    def Set_Time(self, Hour, Min, Sec):#
        self.Set_Time_Sec(Sec)
        self.Set_Time_Min(Min)
        self.Set_Time_Hour(Hour)
    
    def Read_Time(self):
        hr = self.Read_Time_Hour()
        min = self.Read_Time_Min()
        sec = self.Read_Time_Sec()
        return hr,min,sec
    