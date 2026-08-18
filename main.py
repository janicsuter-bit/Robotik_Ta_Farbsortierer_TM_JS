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
        self.War_Gedrueckt = False
        self.Jetzt_Gedrueckt = False
        self.Wert_Ein_Viertel_Auswurf = 105
        self.Wert_Drei_Viertel_Auswurf = 505
        
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
            print("Rot erkannt")
            ev3.screen.clear()
            ev3.screen.draw_text(0, 64, "Rot erkannt")
            self.Ton_Wiedergabe("Rot erkannt")
        elif self.Letzte_Farbe == Color.GREEN:
            print("Grün erkannt")
            ev3.screen.clear()
            ev3.screen.draw_text(0, 64, "Grün erkannt")
            self.Ton_Wiedergabe("Grün erkannt")
        elif self.Letzte_Farbe == Color.BLUE:
            print("Blau erkannt")
            ev3.screen.clear()
            ev3.screen.draw_text(0, 64, "Blau erkannt")
            self.Ton_Wiedergabe("Blau erkannt")
        elif self.Letzte_Farbe == Color.YELLOW:
            print("Gelb erkannt")
            ev3.screen.clear()
            ev3.screen.draw_text(0, 64, "Gelb erkannt")
            self.Ton_Wiedergabe("Gelb erkannt")
        elif self.Letzte_Farbe == Color.BLACK:
            print("Kein Auswurfobjekt erkannt")
            self.None_Zaehler += 1
            if self.None_Zaehler == 2 and self.Sperre_Kein_Baustein == False:
                print("Kein Auswurfobjekt erkannt, wird wiedergegeben")
                ev3.screen.clear()
                self.None_Zaehler = 0
                ev3.screen.draw_text(0, 64, "Kein Auswurfobjekt erkannt")
                self.Ton_Wiedergabe("Kein Auswurfobjekt erkannt")
                self.Sperre_Kein_Baustein = True
                
                
    def Farb_Zaehler(self):
        print("Farbe gezählt")
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
        ev3.speaker.set_speech_options(language='de', voice='M3')
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
            self.Foerderband_Motor.reset_angle(0)   # Nullpunkt = aktuelle Home-Position
            while self.Foerderband_Motor.angle() <= self.Wert_Ein_Viertel_Auswurf:
                self.Foerderband_Motor.run(100)
                print("Winkel:", self.Foerderband_Motor.angle(), "/ Ziel:", self.Wert_Ein_Viertel_Auswurf)
                wait(20)
            self.Foerderband_Motor.hold()
            print("Auswurf Baustein")
            self.Auswurfs_Motor.run_angle(160, -180)#hoch
            print("Auswurfsmechanismus in die Ausgangslage")
            self.Auswurfs_Motor.run_angle(160, 180)#runter
            
            
    #Die Auswurfmethode sobald die Farbe Rot erkannt wird.
    def Drei_Viertel_Auswurf(self):
        print("Auswurfarm fährt in die 3/4 Position")
        if self.Letzte_Farbe == Color.RED:
            self.Foerderband_Motor.reset_angle(0)   
            while self.Foerderband_Motor.angle() <= self.Wert_Drei_Viertel_Auswurf:
                self.Foerderband_Motor.run(150)
                print("Winkel:", self.Foerderband_Motor.angle(), "/ Ziel:", self.Wert_Drei_Viertel_Auswurf)
                wait(20)
            self.Foerderband_Motor.hold()
            print("Auswurf Baustein")
            self.Auswurfs_Motor.run_angle(160, -180)#hoch
            print("Auswurfsmechanismus in die Ausgangslage")
            self.Auswurfs_Motor.run_angle(160, 180)#runter
            
    
    #Auswurfsarm fährt in Ausgangsposition zurück.
    def Ausgangspunkt_Auswurfsarm(self):
        print("Auswurfsarm fährt in Ausgangsposition zurück")
        while not self.Beruehrungs_Sensor.pressed():
            self.Foerderband_Motor.run(-100)
        self.Foerderband_Motor.brake()    
        print("Auswurfsarm in Ausgangsposition angekommen")

    #Verbindung von der Bewegung, erkennung und verarbeitung der farbe
    def Foerderband(self):
        if self.Beruehrungs_Sensor.pressed():
            self.Farbverarbeitung()
            self.Jetzt_Gedrueckt = self.Beruehrungs_Sensor.pressed()
            print(self.Jetzt_Gedrueckt)
            print(self.War_Gedrueckt)
            if self.Jetzt_Gedrueckt == True and self.War_Gedrueckt == False and self.Letzte_Farbe == Color.BLACK:
                print("Foerderband wartet auf neuen Baustein")
                self.War_Gedrueckt = self.Jetzt_Gedrueckt
            elif (self.Beruehrungs_Sensor.pressed() and (self.Letzte_Farbe == Color.GREEN or self.Letzte_Farbe == Color.BLUE or self.Letzte_Farbe == Color.YELLOW)):
                print("Foerderband fährt in die Stellung für den 1/4 Auswurf")
                self.Sperre_Kein_Baustein = False
                self.None_Zaehler = 0
                self.Ein_Viertel_Auswurf()
                self.Farb_Zaehler()
                self.Ausgabe_Bauteilanzahl()
                self.Ausgangspunkt_Auswurfsarm()
                self.War_Gedrueckt = self.Jetzt_Gedrueckt
            elif self.Jetzt_Gedrueckt == True and self.War_Gedrueckt == False and self.Letzte_Farbe == Color.RED:
                self.Sperre_Kein_Baustein = False
                self.None_Zaehler = 0
                print("Foerderband fährt in die Stellung für den 3/4 Auswurf")
                self.Drei_Viertel_Auswurf()
                self.Farb_Zaehler()
                self.Ausgabe_Bauteilanzahl()
                self.Ausgangspunkt_Auswurfsarm()
                self.War_Gedrueckt = self.Jetzt_Gedrueckt
            
    def DataLog(self):
        if (self.Letzte_Farbe != self.Zuerueckliegende_Farbe) and (self.Letzte_Farbe != Color.BLACK or self.Zuerueckliegende_Farbe == Color.BLACK):
            Loggdatei.log(Aktuelle_Zeit.time(), self.Letzte_Farbe, self.Rot_Zaehler, self.Gruen_Zaehler, self.Blau_Zaehler, self.Gelb_Zaehler)
            self.Zuerueckliegende_Farbe = self.Letzte_Farbe                
        
Farbsortierer1 = Farbsortierer(Motor(Port.B), Motor(Port.A), ColorSensor(Port.S2), TouchSensor(Port.S1))

while True:

    Farbsortierer1.Foerderband()
    Farbsortierer1.DataLog()
    wait(200)          
