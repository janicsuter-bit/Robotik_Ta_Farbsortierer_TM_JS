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
Aktuelle_Zeit = StopWatch()
Loggdatei = DataLog("Aktuelle Zeit", "AktuelleFarbe", "Anzahl Rot", "Anzahl Grün", "Anzahl Blau", "Anzahl Gelb")

        
# Write your program here.
class Farbsortierer:
    def __init__(self, Auswurfs_Motor, Foerderband_Motor, Farb_Sensor, Beruehrungs_Sensor):
        self.Auswurfs_Motor = Auswurfs_Motor
        self.Foerderband_Motor = Foerderband_Motor
        self.Farb_Sensor = Farb_Sensor
        self.Beruehrungs_Sensor = Beruehrungs_Sensor
        self.None_Zaehler = 0
        self.Rot_Zaehler = 0
        self.Gruen_Zaehler = 0
        self.Blau_Zaehler = 0
        self.Gelb_Zaehler = 0
        self.Letzte_Farbe = Color.BLACK
        self.Zuerueckliegende_Farbe = Color.BLACK
        self.Sperre_Kein_Baustein = False
        
    def Farberkennung(self):
        print("Farberkennung gestartet")
        if self.Beruehrungs_Sensor.pressed():
            self.Letzte_Farbe = self.Farb_Sensor.color()
            print("Erkannte Farbe: " + str(self.Letzte_Farbe))
            if self.Letzte_Farbe != Color.RED and self.Letzte_Farbe != Color.GREEN and self.Letzte_Farbe != Color.BLUE and self.Letzte_Farbe != Color.YELLOW:
                self.Letzte_Farbe = Color.BLACK
                print("Keine Farbe erkannt")
            
    #Die Farbverarbeitung entscheidet durch die erkannte Farbe welche Aktion ausgeführt wird. 
    def Farbverarbeitung(self):
        self.Farberkennung()
        if self.Letzte_Farbe == Color.RED:
            #Motor bewegt sich in den 3/4
            print("Rot erkannt")
            ev3.screen.clear()
            ev3.screen.draw_text(0, 64, "Rot erkannt") # Noch einmitteln mit folgender formelx = (screen.width - text_width) // 2)
            self.Ton_Wiedergabe("Rot erkannt")
        elif self.Letzte_Farbe == Color.GREEN:
            #Motor bewegt sich in den 1/4
            print("Grün erkannt")
            ev3.screen.clear()
            ev3.screen.draw_text(0, 64, "Grün erkannt")# Noch einmitteln mit folgender formelx = (screen.width - text_width) // 2)
            self.Ton_Wiedergabe("Grün erkannt")
        elif self.Letzte_Farbe == Color.BLUE:
            #Motor bewegt sich in den 1/4
            print("Blau erkannt")
            ev3.screen.clear()
            ev3.screen.draw_text(0, 64, "Blau erkannt")# Noch einmitteln mit folgender formelx = (screen.width - text_width) // 2)
            self.Ton_Wiedergabe("Blau erkannt")
        elif self.Letzte_Farbe == Color.YELLOW:
            #Motor bewegt sich in den 1/4
            print("Gelb erkannt")
            ev3.screen.clear()
            ev3.screen.draw_text(0, 64, "Gelb erkannt")# Noch einmitteln mit folgender formelx = (screen.width - text_width) // 2)
            self.Ton_Wiedergabe("Gelb erkannt")
        elif self.Letzte_Farbe == Color.BLACK:
            print("Kein Auswurfobjekt erkannt")
            self.None_Zaehler += 1
            if self.None_Zaehler == 2 and self.Sperre_Kein_Baustein == False:
                print("Kein Auswurfobjekt erkannt, wird wiedergegeben")
                ev3.screen.clear()
                self.None_Zaehler = 0
                ev3.screen.draw_text(0, 64, "Kein Auswurfobjekt erkannt") # Noch einmitteln mit folgender formelx = (screen.width - text_width) // 2)
                self.Ton_Wiedergabe("Kein Auswurfobjekt erkannt")
                self.Sperre_Kein_Baustein = True
                
                
    def Farb_Zaehler(self):
        if self.Letzte_Farbe == Color.RED:
            self.Rot_Zaehler += 1
        elif self.Letzte_Farbe == Color.GREEN:
            self.Gruen_Zaehler += 1
        elif self.Letzte_Farbe == Color.BLUE:
            self.Blau_Zaehler += 1
        elif self.Letzte_Farbe == Color.YELLOW:
            self.Gelb_Zaehler += 1
    
    #Die Ton_Wiedergabe gibt den übergebenen Text in der Sprache Deutsch wieder.
    def Ton_Wiedergabe(self, Wiedergabetext):
        ev3.speaker.set_volume(100)
        ev3.speaker.set_speech_options(language='de', voice='M3')#Sprache und Wiedergabe anpassen
        ev3.speaker.say(Wiedergabetext)
        
    # Ausgabe_Bauteilanzahl gibt die Anzahl der erkannten Bauteile jeder Farbe auf dem Display aus.
    def Ausgabe_Bauteilanzahl(self):
        print("Ausgabe der Liste der erkannten Farben")
        ev3.screen.clear()
        ev3.screen.draw_text(0, 0, "Letzte erkannte Farbe: " + str(self.Letzte_Farbe))
        ev3.screen.draw_text(0, 25, "Rot: " + str(self.Rot_Zaehler))
        ev3.screen.draw_text(0, 51, "Grün: " + str(self.Gruen_Zaehler))
        ev3.screen.draw_text(0, 77, "Blau: " + str(self.Blau_Zaehler))
        ev3.screen.draw_text(0, 103, "Gelb: " + str(self.Gelb_Zaehler))
    
    #Die Auswurfmethode sobald die Farbe Blau, Gelb oder Grün erkannt wird.
    def Ein_Viertel_Auswurf(self):
        print("Auswurfarm fährt in die 1/4 Position")
        if self.Letzte_Farbe == Color.GREEN or self.Letzte_Farbe == Color.BLUE or self.Letzte_Farbe == Color.YELLOW:
            self.Foerderband_Motor.run_angle(100, 720, Stop.HOLD, True) #geschwindigkeit und winkel noch anpassen
            self.Auswurfs_Motor.run_angle(100, 360, Stop.HOLD, True) #geschwindigkeit noch anpassen
            
            
    #Die Auswurfmethode sobald die Farbe Rot erkannt wird.
    def Drei_Viertel_Auswurf(self):
        print("Auswurfarm fährt in die 3/4 Position")
        if self.Letzte_Farbe == Color.RED:
            self.Foerderband_Motor.run_angle(100, 2160, Stop.HOLD, True) #geschwindigkeit und winkel noch anpassen
            self.Auswurfs_Motor.run_angle(100, 360, Stop.HOLD, True) #geschwindigkeit noch anpassen
            
    
    #Auswurfsarm fährt in Ausgangsposition zurück.
    def Ausgangspunkt_Auswurfsarm(self):
        print("Auswurfsarm fährt in Ausgangsposition zurück")
        if self.Beruehrungs_Sensor.pressed():
            self.Foerderband_Motor.brake()
            print("Auswurfsarm in Ausgangsposition angekommen")
            self.Zuerueckliegende_Farbe = self.Letzte_Farbe
        else:
            self.Foerderband_Motor.run(-100)#geschwindigkeit noch anpassen
            print("Auswurfsarm fährt in Ausgangsposition zurück")

    #Verbindung von der Bewegung, erkennung und verarbeitung der farbe
    def Foerderband(self):
        if self.Beruehrungs_Sensor.pressed():
            self.Farbverarbeitung()
            if self.Beruehrungs_Sensor.pressed() and self.Letzte_Farbe == Color.BLACK:
                print("Foerderband wartet auf neuen Baustein")
            elif (self.Beruehrungs_Sensor.pressed() and (self.Letzte_Farbe == Color.GREEN or self.Letzte_Farbe == Color.BLUE or self.Letzte_Farbe == Color.YELLOW)):
                print("Foerderband fährt in die Stellung für den 1/4 Auswurf")
                self.Sperre_Kein_Baustein = False
                self.None_Zaehler = 0
                self.Ein_Viertel_Auswurf()
                self.Farb_Zaehler()
                self.Ausgabe_Bauteilanzahl()
                self.Ausgangspunkt_Auswurfsarm()
            elif self.Beruehrungs_Sensor.pressed() and self.Letzte_Farbe == Color.RED:
                self.Sperre_Kein_Baustein = False
                self.None_Zaehler = 0
                print("Foerderband fährt in die Stellung für den 3/4 Auswurf")
                self.Drei_Viertel_Auswurf()
                self.Farb_Zaehler()
                self.Ausgabe_Bauteilanzahl()
                self.Ausgangspunkt_Auswurfsarm()
            
    def DataLog(self):
        if (self.Letzte_Farbe != self.Zuerueckliegende_Farbe) and (self.Letzte_Farbe != Color.BLACK or self.Zuerueckliegende_Farbe == Color.BLACK   ):
            Loggdatei.log(Aktuelle_Zeit.time(), self.Letzte_Farbe, self.Rot_Zaehler, self.Gruen_Zaehler, self.Blau_Zaehler, self.Gelb_Zaehler)
        
        
Farbsortierer1 = Farbsortierer(Motor(Port.A),Motor(Port.B),ColorSensor(Port.S1),TouchSensor(Port.S2))

while True:
    Farbsortierer1.Foerderband()
    Farbsortierer1.DataLog()
    wait(200)
             
