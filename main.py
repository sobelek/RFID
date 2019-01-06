#/usr/bin/python
import time
import RPi.GPIO as GPIO
import SimpleMFRC522
import mysql.connector as connector
import Adafruit_CharLCD as LCD
from mysql.connector import errorcode

# Raspberry Pi pin configuration:
lcd_rs        = 26 
lcd_en        = 19
lcd_d4        = 13
lcd_d5        = 6
lcd_d6        = 21
lcd_d7        = 20
lcd_backlight = 2

lcd_columns = 16
lcd_rows    = 2
try:
    con = connector.connect(user='alicjamus_baza1', password='cQ2Qvg8U23', host='95.216.64.27', database='alicjamus_baza1')
    cursor = con.cursor()
#    cursor.execute("insert into Users values ('2', '22222222', 'kurwaaa', '10','1', 'datetime.datetime(2019, 1, 5, 23, 59, 21)')")
#   con.commit()
#    print(cursor.rowcount, 'its good')    
    cursor.execute("select cardId from Users")
    
        
        
except connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Access denied')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print('DB does not exist')
    else:
        print(err)
else:
    con.close()
finally:
    print('connected')
    

reader = SimpleMFRC522.SimpleMFRC522()

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

lcd.clear()
lcd.message('Hello\nworld!')

time.sleep(2.0)

lcd.clear()

lcd.message("KURWA")



try:
    while True:
            id, data = reader.read()
	    print(type(id))
            time.sleep(2.0)
            lcd.clear()
            for points in cursor:
                print(points)
                print("to tu")
                lcd.message("co do chuja")
                time.sleep(3.0)
                lcd.clear()
                lcd.message("chuja2")
                time.sleep(2.0)
finally:
        lcd.message('Bay')
        time.sleep(2.0)
        lcd.clear()
        GPIO.cleanup()
        con.close()
        




