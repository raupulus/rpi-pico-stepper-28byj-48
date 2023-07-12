#! /usr/bin/env python3

from machine import Pin

led = Pin(25, Pin.OUT)
led.on()

from Models.Stepper28byj48 import Stepper28byj48

stepper = Stepper28byj48(pinArray=[2,3,4,5], debug = True, speed='hight', motorSpeed=2400)


print('Iniciando programa')

stepper.start()
