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
Loggdatei = DataLog("Aktuelle Zeit", "Aktuelle Farbe", "Anzahl Rot", "Anzahl Grün", "Anzahl Blau", "Anzahl Gelb")


# Write your program here.
class Farbsortierer:
    def __init__(self, Auswurfs_Motor, Foerderband_Motor, Farb_Sensor, Beruehrungs_Sensor_S1, Beruehrungs_Sensor_S4):
        self.Auswurfs_Motor = Auswurfs_Motor
        self.Foerderband_Motor = Foerderband_Motor
        self.Farb_Sensor = Farb_Sensor
        self.Beruehrungs_Sensor_S1 = Beruehrungs_Sensor_S1
        self.Beruehrungs_Sensor_S4 = Beruehrungs_Sensor_S4
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
        self.Laenge_Foerderband = 0
        self.Wert_Ein_Fuenftel_Auswurf_von_Links = 0
        self.Wert_Zwei_Fuenftel_Auswurf_von_Links = 0
        self.Wert_Drei_Fuenftel_Auswurf_von_Links = 0
        self.Wert_Vier_Fuenftel_Auswurf_von_Links = 0
        self.Wert_Ein_Fuenftel_Auswurf_von_Rechts = 0
        self.Wert_Zwei_Fuenftel_Auswurf_von_Rechts = 0
        self.Wert_Drei_Fuenftel_Auswurf_von_Rechts = 0
        self.Wert_Vier_Fuenftel_Auswurf_von_Rechts = 0
        self.Ausgangssensor_Bestimmung = 0
        self.Farbname = {
        Color.RED: "Rot",
        Color.GREEN: "Gruen",
        Color.BLUE: "Blau",
        Color.YELLOW: "Gelb",
        }

    # Längenmessung des Förderbandes und Bestimmung der fünf Zonen.
    # Start immer bei S1 (links), da von dort auch die Auswurfsstellen definiert werden.
    def Foerderbandlaenge_Bestimmen(self):
        self.Jetzt_Gedrueckt = self.Beruehrungs_Sensor_S1.pressed()
        if self.Jetzt_Gedrueckt == True and self.War_Gedrueckt == False:
            self.Foerderband_Motor.reset_angle(0)
            while not self.Beruehrungs_Sensor_S4.pressed():
                self.Foerderband_Motor.run(100)
            self.Foerderband_Motor.brake()
            self.Laenge_Foerderband = self.Foerderband_Motor.angle()
            print(self.Laenge_Foerderband)

            self.Wert_Ein_Fuenftel_Auswurf_von_Links = self.Laenge_Foerderband / 5
            self.Wert_Zwei_Fuenftel_Auswurf_von_Links = (self.Laenge_Foerderband / 5) * 2
            self.Wert_Drei_Fuenftel_Auswurf_von_Links = (self.Laenge_Foerderband / 5) * 3
            self.Wert_Vier_Fuenftel_Auswurf_von_Links = (self.Laenge_Foerderband / 5) * 4
            print(self.Wert_Ein_Fuenftel_Auswurf_von_Links)
            print(self.Wert_Zwei_Fuenftel_Auswurf_von_Links)
            print(self.Wert_Drei_Fuenftel_Auswurf_von_Links)
            print(self.Wert_Vier_Fuenftel_Auswurf_von_Links)

            self.Wert_Ein_Fuenftel_Auswurf_von_Rechts = -(self.Laenge_Foerderband / 5) 
            self.Wert_Zwei_Fuenftel_Auswurf_von_Rechts = -(self.Laenge_Foerderband / 5) * 2
            self.Wert_Drei_Fuenftel_Auswurf_von_Rechts = -(self.Laenge_Foerderband / 5) * 3
            self.Wert_Vier_Fuenftel_Auswurf_von_Rechts = -(self.Laenge_Foerderband / 5) * 4
            print(self.Wert_Ein_Fuenftel_Auswurf_von_Rechts)
            print(self.Wert_Zwei_Fuenftel_Auswurf_von_Rechts)
            print(self.Wert_Drei_Fuenftel_Auswurf_von_Rechts)
            print(self.Wert_Vier_Fuenftel_Auswurf_von_Rechts)

            self.Ausgangssensor_Bestimmung = 2
            print("Ausgangsstellung Rechts(2)")
            self.War_Gedrueckt = False

    def Farberkennung(self):
        print("Farberkennung gestartet")
        if self.Beruehrungs_Sensor_S1.pressed() or self.Beruehrungs_Sensor_S4.pressed():
            self.Letzte_Farbe = self.Farb_Sensor.color()
            print("Erkannte Farbe: " + str(self.Letzte_Farbe))
            if self.Letzte_Farbe != Color.RED and self.Letzte_Farbe != Color.GREEN and self.Letzte_Farbe != Color.BLUE and self.Letzte_Farbe != Color.YELLOW:
                self.Letzte_Farbe = Color.BLACK
                print("Keine Farbe erkannt")

    # Die Farbverarbeitung entscheidet durch die erkannte Farbe welche Aktion ausgeführt wird.
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
            if self.None_Zaehler >= 2 and self.Sperre_Kein_Baustein == False:
                print("Kein Auswurfobjekt erkannt, wird wiedergegeben")
                ev3.screen.clear()
                self.None_Zaehler = 0
                ev3.screen.draw_text(0, 42, "Kein Auswurf-")
                ev3.screen.draw_text(0, 84, "objekt erkannt")
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

    # Die Ton_Wiedergabe gibt den übergebenen Text in der Sprache Deutsch wieder.
    def Ton_Wiedergabe(self, Wiedergabetext):
        ev3.speaker.set_volume(100)
        ev3.speaker.set_speech_options(language='de', voice='m3')
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

    def Auswurf_Mechanismus(self):
        print("Auswurf Baustein")
        self.Auswurfs_Motor.run_angle(160, -180)  # hoch
        print("Auswurfsmechanismus in die Ausgangslage")
        self.Auswurfs_Motor.run_angle(160, 180)  # runter

    # Die Auswurfmethode sobald die Farbe Blau erkannt wird (1/5, näher an S1).
    def Ein_Fuenftel_Auswurf(self):
        print("Auswurfarm fährt in die 1/5 Position")
        self.Foerderband_Motor.reset_angle(0)
        if self.Ausgangssensor_Bestimmung == 1:
            while self.Foerderband_Motor.angle() <= self.Wert_Ein_Fuenftel_Auswurf_von_Links:
                self.Foerderband_Motor.run(150)
                wait(20)
        elif self.Ausgangssensor_Bestimmung ==2:
            while self.Foerderband_Motor.angle() >= self.Wert_Vier_Fuenftel_Auswurf_von_Rechts:
                self.Foerderband_Motor.run(-150)
                wait(20)
        self.Foerderband_Motor.hold()
        print("Förderband stopt")
        print(self.Foerderband_Motor.angle())
        self.Auswurf_Mechanismus()
        self.Ausgangspunkt_Auswurfsarm(self.Beruehrungs_Sensor_S1)
        self.War_Gedrueckt = False

    # Die Auswurfmethode sobald die Farbe Gelb erkannt wird (2/5, näher an S1).
    def Zwei_Fuenftel_Auswurf(self):
        print("Auswurfarm fährt in die 2/5 Position")
        self.Foerderband_Motor.reset_angle(0)
        if self.Ausgangssensor_Bestimmung == 1:
            while self.Foerderband_Motor.angle() <= self.Wert_Zwei_Fuenftel_Auswurf_von_Links:
                self.Foerderband_Motor.run(150)
                wait(20)
        elif self.Ausgangssensor_Bestimmung ==2:
            while self.Foerderband_Motor.angle() >= self.Wert_Drei_Fuenftel_Auswurf_von_Rechts:
                self.Foerderband_Motor.run(-150)
                wait(20)
        self.Foerderband_Motor.hold()
        print("Förderband stopt")
        print(self.Foerderband_Motor.angle())
        self.Auswurf_Mechanismus()
        self.Ausgangspunkt_Auswurfsarm(self.Beruehrungs_Sensor_S1)
        self.War_Gedrueckt = False

    # Die Auswurfmethode sobald die Farbe Grün erkannt wird (3/5, näher an S4).
    def Drei_Fuenftel_Auswurf(self):
        print("Auswurfarm fährt in die 3/5 Position")
        self.Foerderband_Motor.reset_angle(0)
        if self.Ausgangssensor_Bestimmung == 1:
            print("Fährt vom Sensor S1")
            while self.Foerderband_Motor.angle() <= self.Wert_Drei_Fuenftel_Auswurf_von_Links:
                self.Foerderband_Motor.run(150)
                wait(20)
        elif self.Ausgangssensor_Bestimmung ==2:
            print("Fährt vom Sensor S4")
            while self.Foerderband_Motor.angle() >= self.Wert_Zwei_Fuenftel_Auswurf_von_Rechts:
                self.Foerderband_Motor.run(-150)
                wait(20)
        self.Foerderband_Motor.hold()
        print("Förderband stopt")
        print(self.Foerderband_Motor.angle())
        self.Auswurf_Mechanismus()
        self.Ausgangspunkt_Auswurfsarm(self.Beruehrungs_Sensor_S4)
        self.War_Gedrueckt = False

    # Die Auswurfmethode sobald die Farbe Rot erkannt wird (4/5, näher an S4).
    def Vier_Fuenftel_Auswurf(self):
        print("Auswurfarm fährt in die 4/5 Position")
        self.Foerderband_Motor.reset_angle(0)
        if self.Ausgangssensor_Bestimmung == 1:
            while self.Foerderband_Motor.angle() <= self.Wert_Vier_Fuenftel_Auswurf_von_Links:
                self.Foerderband_Motor.run(150)
                wait(20)
        elif self.Ausgangssensor_Bestimmung ==2:
            while self.Foerderband_Motor.angle() >= self.Wert_Ein_Fuenftel_Auswurf_von_Rechts:
                self.Foerderband_Motor.run(-150)
                wait(20)
        self.Foerderband_Motor.hold()
        print("Förderband stopt")
        print(self.Foerderband_Motor.angle())
        self.Auswurf_Mechanismus()
        self.Ausgangspunkt_Auswurfsarm(self.Beruehrungs_Sensor_S4)
        self.War_Gedrueckt = False

    # Auswurfsarm fährt zum übergebenen Ziel-Sensor zurück (S1 oder S4).
    def Ausgangspunkt_Auswurfsarm(self, Ziel_Sensor):
        print("Auswurfsarm fährt in Ausgangsposition zurück")
        if Ziel_Sensor == self.Beruehrungs_Sensor_S1:
            while not self.Beruehrungs_Sensor_S1.pressed():
                self.Foerderband_Motor.run(-100)
        else:
            while not self.Beruehrungs_Sensor_S4.pressed():
                self.Foerderband_Motor.run(100)
        self.Foerderband_Motor.brake()
        if self.Beruehrungs_Sensor_S1.pressed():
            self.Ausgangssensor_Bestimmung = 1
        elif self.Beruehrungs_Sensor_S4.pressed():
            self.Ausgangssensor_Bestimmung = 2
        print("Auswurfsarm in Ausgangsposition angekommen")

    # Verbindung von Bewegung, Erkennung und Verarbeitung der Farbe.
    def Foerderband(self):
        self.Jetzt_Gedrueckt = self.Beruehrungs_Sensor_S1.pressed() or self.Beruehrungs_Sensor_S4.pressed()
        if self.Jetzt_Gedrueckt:
            self.Farbverarbeitung()
            print(self.Jetzt_Gedrueckt)
            print(self.War_Gedrueckt)
            if self.Jetzt_Gedrueckt == True and self.War_Gedrueckt == False and self.Letzte_Farbe == Color.BLACK:
                print("Foerderband wartet auf neuen Baustein")
            elif self.Jetzt_Gedrueckt == True and self.War_Gedrueckt == False and self.Letzte_Farbe == Color.BLUE:
                print("Foerderband fährt in die Stellung für den 1/5 Auswurf")
                self.Sperre_Kein_Baustein = False
                self.None_Zaehler = 0
                self.Ein_Fuenftel_Auswurf()
                self.Farb_Zaehler()
                self.Ausgabe_Bauteilanzahl()
                wait(1000)
                
            elif self.Jetzt_Gedrueckt == True and self.War_Gedrueckt == False and self.Letzte_Farbe == Color.YELLOW:
                self.Sperre_Kein_Baustein = False
                self.None_Zaehler = 0
                print("Foerderband fährt in die Stellung für den 2/5 Auswurf")
                self.Zwei_Fuenftel_Auswurf()
                self.Farb_Zaehler()
                self.Ausgabe_Bauteilanzahl()
                wait(1000)
                
            elif self.Jetzt_Gedrueckt == True and self.War_Gedrueckt == False and self.Letzte_Farbe == Color.GREEN:
                self.Sperre_Kein_Baustein = False
                self.None_Zaehler = 0
                print("Foerderband fährt in die Stellung für den 3/5 Auswurf")
                self.Drei_Fuenftel_Auswurf()
                self.Farb_Zaehler()
                self.Ausgabe_Bauteilanzahl()
                wait(1000)
                
            elif self.Jetzt_Gedrueckt == True and self.War_Gedrueckt == False and self.Letzte_Farbe == Color.RED:
                self.Sperre_Kein_Baustein = False
                self.None_Zaehler = 0
                print("Foerderband fährt in die Stellung für den 4/5 Auswurf")
                self.Vier_Fuenftel_Auswurf()
                self.Farb_Zaehler()
                self.Ausgabe_Bauteilanzahl()
                wait(1000)
                
    def DataLog(self):
        if (self.Letzte_Farbe != self.Zuerueckliegende_Farbe) and (self.Letzte_Farbe != Color.BLACK or self.Zuerueckliegende_Farbe == Color.BLACK):
            Loggdatei.log(Aktuelle_Zeit.time() / 1000, self.Farbname[self.Letzte_Farbe], self.Rot_Zaehler, self.Gruen_Zaehler, self.Blau_Zaehler, self.Gelb_Zaehler)
            self.Zuerueckliegende_Farbe = self.Letzte_Farbe
            
    def Links_fahren(self):
        while not self.Beruehrungs_Sensor_S1.pressed():
            self.Foerderband_Motor.run(-150)
        self.Foerderband_Motor.brake()
        self.Ausgangssensor_Bestimmung = 0
        print("Starten mit dem ausmessen")
        
        

Farbsortierer1 = Farbsortierer(Motor(Port.B), Motor(Port.A), ColorSensor(Port.S2), TouchSensor(Port.S1), TouchSensor(Port.S4))


Farbsortierer1.Links_fahren()
Farbsortierer1.Foerderbandlaenge_Bestimmen()
while True:
    Farbsortierer1.Foerderband()
    Farbsortierer1.DataLog()
    wait(200)
    