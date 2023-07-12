#! /usr/bin/env python3

from machine import Pin
from time import sleep


class Stepper28byj48:
    direction = 'clockwise' # clockwise, counterclockwise
    speed = 'slow' # slow, medium, hight
    speedSteps = {
        'slow': [
            [1,0,0,0,],
            [0,1,0,0,],
            [0,0,1,0,],
            [0,0,0,1,],
        ],
        'medium': [
            [1,0,0,0,],
            [1,1,0,0,],
            [0,1,0,0,],
            [0,1,1,0,],
            [0,0,1,0,],
            [0,0,1,1,],
            [0,0,0,1,],
            [1,0,0,1,],
        ],
        'hight': [
            [1,1,0,0,],
            [0,1,1,0,],
            [0,0,1,1,],
            [1,0,0,1,],
        ],
    }



    def __init__(self, pinArray, direction = 'clockwise', speed = 'slow', debug = False):
        """
        Inicializa el motor
        @param pinArray: Array con los pines del motor en orden, [IN1, IN2, IN3, IN4]
        @param direction: Dirección del motor, clockwise o counterclockwise
        @param speed: Velocidad del motor, slow, medium o hight
        @param debug: Muestra mensajes de debug
        """
        self.debug = debug

        if len(pinArray) != 4:
            raise Exception('Error: Debe ingresar 4 pines')

        self.pinArray = pinArray

        self.pins = {}

        for pos, pin in enumerate(self.pinArray):
            self.pins[pos] = Pin(pin, Pin.OUT)
            self.pins[pos].off()


        if direction in ['clockwise', 'counterclockwise']:
            self.direction = direction

        if speed in ['slow', 'medium', 'hight']:
            self.speed = speed

        if self.debug:
            print('Stepper28byj48 iniciado')
            print('Dirección: ', self.direction)


    def start(self):
        """
        Inicia el motor
        """
        motorSpeed = 1200; # Microsegundos entre pasos
        stepCounter = 0;
        stepsPerRev = 4076;

        if self.debug:
            print('Iniciando motor')

        pins = self.pins # Instancia con los pines del motor
        speedSteps = self.speedSteps[self.speed] # Instancia con los pasos del motor para la velocidad seleccionada
        steps = len(speedSteps); # 4 u 8 dependiendo del modo de velocidad

        #timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)



        while True:
            print('steps: ', steps)
            print('speed:', self.speed)

            for i in range(0, (stepsPerRev * 2) - 1):

                if stepCounter < (steps - 1):
                    stepCounter += 1
                else:
                    stepCounter = 0

                #print('pins: ', pins)
                #print('pins[0]: ', pins[0])
                #print('pins[0].value: ', pins[0].value())
                #print('speedSteps', speedSteps)
                #print('speedSteps[stepCounter]', speedSteps[stepCounter])


                pins[0].value(speedSteps[stepCounter][0])
                pins[1].value(speedSteps[stepCounter][1])
                pins[2].value(speedSteps[stepCounter][2])
                pins[3].value(speedSteps[stepCounter][3])


                sleep(motorSpeed / 1000000.0) # Microsegundos a segundos










    def setDirection(self, direction):
        if self.debug:
            print('Dirección: ', direction)


    def setSpeed(self, speed):
        if self.debug:
            print('Velocidad: ', speed)
