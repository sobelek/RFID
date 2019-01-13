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

lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d7 = digitalio.DigitalInOut(board.D20)
lcd_d6 = digitalio.DigitalInOut(board.D21)
lcd_d5 = digitalio.DigitalInOut(board.D6)
lcd_d4 = digitalio.DigitalInOut(board.D13)
lcd_backlight = digitalio.DigitalInOut(board.D2)
lcd_columns = 16
lcd_rows    = 2
lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)


id = (None, None)
points_new = 0
counter = False
reader = SimpleMFRC522.SimpleMFRC522()


def btn1_push():
    global points_new
    global counter
    points_new +=1
    counter = True

    
button1 = gpiozero.Button(btn1)
button1.when_released = btn1_push


print("Connecting to Database")
lcd.clear()
lcd.message = "Connecting to \nDatabase" 


try:
    con = connector.connect(user='alicjamus_baza1', password='cQ2Qvg8U23', host='95.216.64.27', database='alicjamus_baza1')
    cursor = con.cursor()
    time.sleep(2.0)        
except connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Access denied')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print('DB does not exist')
    else:
        print(err)
finally:
    print('connected')

class CardThread(threading.Thread):
    def __init__(self):
        super(CardThread, self).__init__()
    def run(self):
        while True:
            global id
            id = reader.read_id()
            print(id)


thread1 = CardThread()
thread1.setDaemon(True)
thread1.start()

try:
    lcd.clear()
    while True:
            lcd.message = "Przyloz Karte"
            #id = reader.read_id_no_block()
            print("imalive")
            if counter == True:
                lcd.clear()
                while True:
                    lcd.message = "Points +{}".format(points_new)
                    if id != (None, None):
                        counter = False
                        break
            if id != (None, None):
                cursor.execute("select points from Users where cardId='{}'".format(id))
                points = cursor.fetchall()
                id = None 
                if(not points):
                    cursor.execute("insert into Users (cardId) values ({})".format(id))
                    con.commit()
                    lcd.clear()
                    lcd.message= "Dodano karte\nklienta"
                    print(cursor.rowcount,"Not in database, adding")
                    time.sleep(5.0)
                elif(points):
                    points = points[0][0]
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
        




