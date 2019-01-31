#!/usr/bin/python3
import time
import gpiozero
import SimpleMFRC522
import mysql.connector as connector
import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd
from mysql.connector import errorcode
import threading
# Raspberry Pi pin configuration:

btn1 = 16
btn2 = 12
btn3 = 1


id = (None, None)
points_new = 0
counter = False
cleared = False
thread_alive = False

lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d7 = digitalio.DigitalInOut(board.D20)
lcd_d6 = digitalio.DigitalInOut(board.D21)
lcd_d5 = digitalio.DigitalInOut(board.D6)
lcd_d4 = digitalio.DigitalInOut(board.D13)
lcd_backlight = digitalio.DigitalInOut(board.D2)
lcd_columns = 16
lcd_rows    = 2
config = 0
while config != 3:
    config = 0
    try:
        lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
        config += 1
    except:
        print("Error with lcd config")
    try:
        reader = SimpleMFRC522.SimpleMFRC522()
        config +=1
    except:
        print("Error with reader config")
    try:
        print("Connecting to Database")
        lcd.clear()
        lcd.message = "Connecting to \nDatabase" 
        con = connector.connect(user='alicjamus_baza1', password='cQ2Qvg8U23', host='95.216.64.27', database='alicjamus_baza1')
        cursor = con.cursor()
        time.sleep(2.0)
        config += 1
    except connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Access denied')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('DB does not exist')
        else:
            print(err)
    finally:
        print('connected')


def btn_plus():
    global points_new
    global counter
    global cleared
    cleared = False
    points_new +=1
    counter = True


def btn_minus():
    global points_new
    global counter
    global cleared
    cleared = False
    points_new-=10
    counter = True


def btn_reset():
    global points_new
    global counter
    global cleared
    cleared = False
    points_new = 0
    counter = False


button1 = gpiozero.Button(btn1)
button2 = gpiozero.Button(btn2)
button3 = gpiozero.Button(btn3)

button1.when_released = btn_plus
button2.when_released = btn_minus
button3.when_released = btn_reset


class CardThread(threading.Thread):
    def __init__(self):
        super(CardThread, self).__init__()
    def run(self):
        while True:
            global id
            id = reader.read_id()
while thread_alive != True:
    try:
        thread1 = CardThread()
        thread1.setDaemon(True)
        thread1.start()
        thread_alive = thread1.is_alive()
    except:
        print("thread exception")
try:
    lcd.clear()
    while True:
            lcd.message = "Przyloz Karte lub\nWprwoadz punkty"
            while counter == True:
                if cleared == False:
                    lcd.clear()
                    cleared = True
                if points_new > 0: 
                    lcd.message = "Points +{}".format(points_new)
                else:
                    lcd.message = "Points {}".format(points_new)
                if id != (None, None):
                    cursor.execute("select points,isActive from Users where cardId='{}'".format(id))
                    points, active = cursor.fetchone()
                    if active == 1:
                        points_new = points + points_new
                        if points_new < 0:
                            lcd.message = "Za malo punktow\nna karcie"
                            time.sleep(2.0)
                            lcd.clear()
                            counter = False
                            points_new = 0
                            break
                        else:
                            cursor.execute("update Users set points = {} where cardId = {}".format(points_new, id))
                            con.commit()
                            counter = False
                            points_new = 0
                            break
                    else:
                        lcd.clear()
                        lcd.message = "Karta nie aktywna"
                        time.sleep(1.0)
                        counter = False
                        points_new = 0
                        break
            if id != (None, None):
                cursor.execute("select points from Users where cardId='{}'".format(id))
                points = cursor.fetchone()
                
                if(not points):
                    cursor.execute("insert into Users (cardId) values ({})".format(id))
                    con.commit()
                    lcd.clear()
                    lcd.message= "Dodano karte\nklienta"
                    print(cursor.rowcount,"Not in database, adding")
                    time.sleep(5.0)
                    lcd.clear()
                elif(points == (None,) and active == (None,)):
                    lcd.clear()
                    lcd.message = "Karta nie \naktywna"
                    time.sleep(3.0)
                    lcd.clear()
                elif(points):
                    points = points[0]
                    print(points)
                    lcd.clear()
                    lcd.message = 'Punkty:{}'.format(str(points))
                    time.sleep(3)
                    lcd.clear()
        
finally:
        thread1.join(0)
        lcd.clear()
        lcd.message = 'Bay'
        time.sleep(2.0)
        lcd.clear()
        con.close()
        




