'''
    Developed by Krishnakumar Karuppasamy
    version 2.0
    17-12-2018
    Documentation link 
'''
import pymysql as p
from RPLCD import CharLCD
import RPi.GPIO as GPIO
import MFRC522
from urllib2 import urlopen


framebuffer = [
    '',
    '',
    ]

lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 18])

def write_to_lcd(lcd, framebuffer, num_cols):       
    lcd.home()
    for row in framebuffer:
        lcd.write_string(row.ljust(num_cols)[:num_cols])
        lcd.write_string('\r\n')

#inistialize the buffer of screen
write_to_lcd(lcd, framebuffer, 16)

#display value to LCD 
def lcdDisplay(long_string):
    lcd.clear()
    def loop_string(string, lcd, framebuffer, row, num_cols, delay=0.2): #DELAY= CONTROLS THE SPEED OF SCROLL
        padding = ' ' * num_cols
        s = padding + string + padding
        for i in range(len(s) - num_cols + 1):
            framebuffer[row] = s[i:i+num_cols]
            write_to_lcd(lcd, framebuffer, num_cols)
            time.sleep(delay)

    loop_string(long_string, lcd, framebuffer, 1, 16)


#delay for mysql server start 
time.sleep(5)

# Open database connection
db = p.connect("127.0.0.1","root","admin","sit_iot" )


# prepare a cursor object using cursor() method
cursor = db.cursor()

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print ("Welcome to SIT RFID Portal")

#send to server
def sendToServer(uid, name):
    value=uid.replace(' ','')
    name=name.replace(' ','%20')    
    try:
        print ('server function')
        #print (urlopen('your server and values')
        
    except:
        print ('cannot send')

#check whether network available or not
def networkChecking():
    try:
        urlopen('http://172.217.194.106',timeout=2)
        return True
    except:
        return False

#validate the UID from user
def validate(uid):
    uid=str(uid)
    uid=uid.replace(' ','')    
    getResult=cursor.execute("select * from employee_details where uid='%s'" %(uid))
    result = cursor.fetchone()    
    if getResult:
        print('name %s' %result[1])
        #lcdDisplay(result[1])
        if networkChecking():            
            print('network available')            
            #sendToServer(uid,result[1])
        else:
            print('network failuer')
            #lcdDisplay('network failure')
    else:
        print('not register')
        #GPIO.output(12,1)  #display light result
        #lcdDisplay('un authorized')
        #time.sleep(1)
        #GPIO.output(11,0)
        

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while True:

    # Scan for cards
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
         print(str(uid)+' is your id')
         #GPIO.output(11,1)  #display light result
         #time.sleep(1)
         #GPIO.output(11,0)
         validate(uid)                                           