import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import signal
import RPi.GPIO as GPIO
import MFRC522
import signal
GPIO.setwarnings(False) 
continue_reading = True

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)
defused = False

try:
    # Turn backlight on
    lcd.set_backlight(0)

    # Print a two line message
    lcd.message('Initiate Launch\nOf Cyber Attack')

    # Wait 5 seconds
    time.sleep(5.0)

    time.left = 45
    i = 0 

    #time.sleep(60.0)
    
    while i <= time.left:
        lcd.clear()
        lcd.message('T-Minus ' + str(time.left) + '\nMins to Launch')
        time.left -= 1
        time.sleep(60.0)
        
        #logic for RFID
        signal.signal(signal.SIGINT, end_read)
        # create the reader object
        MIFAREReader = MFRC522.MFRC522()
        # detect touch of the card, get status and tag type
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # Get the RFID card uid and status
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If status is alright, continue to the next stage
        if status == MIFAREReader.MI_OK:
            defused = True
            break       
        

    lcd.clear()
    if defused:
        message = 'Congratulations!\nAttack Stopped'
        lcd.message(message)
        time.sleep(45.0)
    else:
        message = 'Launching'
        lcd.message(message)
        for i in range(lcd_columns-len(message)):
            time.sleep(1)
            lcd.move_right()
        for i in range(lcd_columns-len(message)):
            time.sleep(1)
            lcd.move_left()
        for i in range(lcd_columns-len(message)):
            time.sleep(1)
            lcd.move_right()
        for i in range(lcd_columns-len(message)):
            time.sleep(1)
            lcd.move_left()    

        lcd.clear()
        lcd.message('My Evil Cyber\nAttack Launched!')
    # Turn backlight on.
    lcd.set_backlight(0)
    # Turn backlight off.
    time.sleep(15)
    lcd.clear()
    lcd.set_backlight(1)
except KeyboardInterrupt:
    # Turn the screen off
    lcd.clear()
    lcd.set_backlight(1) 