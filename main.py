#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import Font, SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()


# Write your program here.
class Farbsortierer:
    def __init__(self, Auswurfs_Motor, Foerderband_Motor, Farb_Sensor, Beruehrungs_Sensor):
        self.Auswurfs_Motor = Auswurfs_Motor
        self.Foerderband_Motor = Foerderband_Motor
        self.Farb_Sensor = Farb_Sensor
        self.Beruehrungs_Sensor = Beruehrungs_Sensor
        
    def Farberkennung(self):
        self.Letzte_Farbe = self.Farb_Sensor.color()
        if self.Letzte_Farbe != Color.RED and self.Letzte_Farbe != Color.GREEN and self.Letzte_Farbe != Color.BLUE and self.Letzte_Farbe != Color.YELLOW:
            self.Letzte_Farbe = Color.NONE
            
    #Die Farbverarbeitung entscheidet durch die erkannte Farbe welche Aktion ausgeführt wird. 
    def Farbverarbeitung(self):
        self.Farberkennung()
        if self.Letzte_Farbe == Color.RED:
            #Motor bewegt sich in den 3/4
            Rot_Zaehler += 1
            ev3.screen.draw_text(0, 64, "Rot erkannt") # Noch einmitteln mit folgender formelx = (screen.width - text_width) // 2)
        elif self.Letzte_Farbe == Color.GREEN:
            #Motor bewegt sich in den 1/4
            Gruen_Zaehler += 1
            ev3.screen.draw_text(0, 64, "Grün erkannt")# Noch einmitteln mit folgender formelx = (screen.width - text_width) // 2)
        elif self.Letzte_Farbe == Color.BLUE:
            #Motor bewegt sich in den 1/4
            Blau_Zaehler += 1
            ev3.screen.draw_text(0, 64, "Blau erkannt")# Noch einmitteln mit folgender formelx = (screen.width - text_width) // 2)
        elif self.Letzte_Farbe == Color.YELLOW:
            #Motor bewegt sich in den 1/4
            Gelb_Zaehler += 1
            ev3.screen.draw_text(0, 64, "Gelb erkannt")# Noch einmitteln mit folgender formelx = (screen.width - text_width) // 2)
        elif self.Letzte_Farbe == Color.NONE:
            None_Zaehler += 1
            if None_Zaehler == 2:
                None_Zaehler = 0
                ev3.screen.draw_text(0, 64, "Kein Auswurfobjekt erkannt") # Noch einmitteln mit folgender formelx = (screen.width - text_width) // 2)
    
    # Ausgabe_Farbe gibt die letzte erkannte Farbe und die Anzahl der erkannten Farben auf dem Display aus.
    def Ausgabe_Farbe(self):
        ev3.screen.clear()
        ev3.screen.draw_text(0, 0, "Letzte erkannte Farbe: " + str(self.Letzte_Farbe))
        ev3.screen.draw_text(0, 25, "Rot: " + str(self.Rot_Zaehler))
        ev3.screen.draw_text(0, 51, "Grün: " + str(self.Gruen_Zaehler))
        ev3.screen.draw_text(0, 77, "Blau: " + str(self.Blau_Zaehler))
        ev3.screen.draw_text(0, 103, "Gelb: " + str(self.Gelb_Zaehler))
    
    def Ein_Viertel_Auswurf(self):
        pass
    
    def Drei_Viertel_Auswurf(self):
        pass

        
        
Farbsortierer1 = Farbsortierer(Motor(Port.A),Motor(Port.B),ColorSensor(Port.S1),TouchSensor(Port.S2))


             
