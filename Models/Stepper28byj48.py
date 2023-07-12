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



    def __init__(self, pinArray, direction = 'clockwise', speed = 'slow', motorSpeed = 1200, stepsPerRev = 4076, debug = False):
        """
        Inicializa el motor
        @param pinArray: Array con los pines del motor en orden, [IN1, IN2, IN3, IN4]
        @param direction: Dirección del motor, clockwise o counterclockwise
        @param speed: Velocidad del motor, slow, medium o hight
        @param motorSpeed: Velocidad del motor en microsegundos, 1200 por defecto aunque me funciona mejor con 2400
        @param stepsPerRev: Pasos por revolución, 4076 por defecto. Debería ser 4096 pero en estos motores se descuentan (leer datasheet)
        @param debug: Muestra mensajes de debug
        """
        self.debug = debug
        self.active = False

        if motorSpeed and motorSpeed > 1200:
            self.motorSpeed = motorSpeed

        if stepsPerRev > 100:
            self.stepsPerRev = stepsPerRev

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


    def run(self, stepsLimit = None):
        """
        @param stepsLimit: Cantidad de pasos a ejecutar, None para infinito
        """
        self.active = True

        motorSpeed = self.motorSpeed
        stepsPerRev = self.stepsPerRev

        pins = self.pins # Instancia con los pines del motor
        speedSteps = self.speedSteps[self.speed] # Instancia con los pasos del motor para la velocidad seleccionada
        steps = len(speedSteps) # 4 u 8 dependiendo del modo de velocidad

        direction = self.direction

        if direction is 'clockwise':
            stepCounter = 0;
        else:
            stepCounter = steps - 1;



        while self.active:
            if not self.active:
                break

            for i in range(0, stepsPerRev):
                if not self.active or (stepsLimit and i >= (stepsLimit - 1)):
                    self.active = False
                    break

                if direction == 'clockwise' and stepCounter < (steps - 1):
                    stepCounter += 1
                elif direction == 'counterclockwise' and (stepCounter > 0):
                    stepCounter -= 1
                else:
                    if direction is 'clockwise':
                        stepCounter = 0
                    else:
                        stepCounter = steps - 1

                #print('pins: ', pins)
                #print('pins[0]: ', pins[0])
                #print('pins[0].value: ', pins[0].value())
                #print('speedSteps', speedSteps)
                #print('speedSteps[stepCounter]', speedSteps[stepCounter])


                pins[0].value(speedSteps[stepCounter][0])
                pins[1].value(speedSteps[stepCounter][1])
                pins[2].value(speedSteps[stepCounter][2])
                pins[3].value(speedSteps[stepCounter][3])

                sleep(motorSpeed / 1000000.0) # Microsegundos a Segundos

    def start(self):
        """
        Inicia el motor
        """

        if self.debug:
            print('Iniciando motor')

        self.run()
        #timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)



    def stop(self):
        """
        Detiene el motor apagando todos los pines y marca el estado como inactivo.
        """
        self.active = False
        sleep(0.1)

        pins = self.pins

        pins[0].off()
        pins[1].off()
        pins[2].off()
        pins[3].off()

    def setDirection(self, direction):
        if direction in ['clockwise', 'counterclockwise']:
            self.direction = direction

        if self.debug:
            print('Dirección: ', direction)


    def setSpeed(self, speed):
        if speed in ['slow', 'medium', 'hight']:
            self.speed = speed

        if self.debug:
            print('Velocidad: ', speed)

    def moveToDegrees(self, degrees):
        # Calcular a partir de los ciclos que necesita el motor para dar una vuelto el equivalente en grados.
        stepsPerRev = self.stepsPerRev

        stepsPerDegrees = (stepsPerRev * degrees) / 360

        self.run(stepsPerDegrees)
