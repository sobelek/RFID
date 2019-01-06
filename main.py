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
        
except connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Access denied')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print('DB does not exist')
    else:
        print(err)
finally:
    print('connected')
    
reader = SimpleMFRC522.SimpleMFRC522()
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

try:
    while True:
            lcd.message("Przyloz Karte")
            id, data = reader.read()
            cursor.execute("select points from Users where cardId='{}'".format(id))
            points = cursor.fetchall()
            if(not points):
                cursor.execute("insert into Users (cardId) values ({})".format(id))
                con.commit()
                lcd.clear()
                lcd.message("Dodano karte\nklienta")
                print(cursor.rowcount,"Not in database, adding")
                time.sleep(5.0)
            elif(points):
                points = points[0][0]
                print(points)
                lcd.clear()
                lcd.message('Punkty:{}'.format(str(points)))
                time.sleep(3)
                lcd.clear()
        
finally:
        lcd.clear()
        lcd.message('Bay')
        time.sleep(2.0)
        lcd.clear()
        GPIO.cleanup()
        con.close()
        




