#! /usr/bin/env python3

from machine import Pin
from time import sleep


led = Pin(25, Pin.OUT)
led.on()

from Models.Stepper28byj48 import Stepper28byj48

# Inicializa el motor con los pines IN1, IN2, IN3, IN4 y velocidad de 2400 microsegundos teniendo en cuenta que el motor tiene 2038 pasos por revolución. Esto cambia según el motor y debes revisar el datasheet para ajustarlo correctamente.
stepper = Stepper28byj48(pinArray=[2,3,4,5], debug = True, speed='hight', motorSpeed=2400, direction='clockwise', stepsPerRev=2038)


print('Iniciando programa de Ejemplo')


stepper.moveToDegrees(180)
sleep(2)
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


# Se crea un loop Infinito

stepper.start()
