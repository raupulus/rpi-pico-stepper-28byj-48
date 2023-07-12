#! /usr/bin/env python3

from machine import Pin
from time import sleep


led = Pin(25, Pin.OUT)
led.on()

from Models.Stepper28byj48 import Stepper28byj48

stepper = Stepper28byj48(pinArray=[2,3,4,5], debug = True, speed='hight', motorSpeed=2400, direction='clockwise', stepsPerRev=2038)


print('Iniciando programa')

#stepper.start()


stepper.moveToDegrees(180)

"""
exit()

sleep(7)
stepper.moveToDegrees(60)
sleep(2)
stepper.setDirection('counterclockwise')
stepper.moveToDegrees(90)
sleep(2)
stepper.setDirection('clockwise')
stepper.moveToDegrees(180)
sleep(2)
stepper.setDirection('counterclockwise')
stepper.moveToDegrees(30)
sleep(2)
stepper.setDirection('clockwise')
stepper.moveToDegrees(360)
"""
