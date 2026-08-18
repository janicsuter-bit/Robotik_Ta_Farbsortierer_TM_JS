# Farbsortierer

#In diesem Projekt programmieren wir einen Farbsortierer. Die Struktur ist in zwei Teile unterteilt, Die Klasse(Farbsortierer) und die While-True Schleife(Hauptschleife). In der Klasse sind alle Attribute und Funktionen vorhanden. Während in der While-True Schleife nur wenige Funktion vorhanden sind. Es gibt die Funktionen:
#__init__():Erstellen aller Variablen und Sensor in der Klasse
#Farberkennung():Der Farbsensor wird ausgelesen, sobald der Berührungssensor betätig ist. Wird eine Farbe erkannt wird sie der variabel zugeordnet die den Wert Rot, Gelb, Grün oder Blau hat. Wird keine erkannt, ergo kein Baustein vorhanden wird die Farbe auf Schwarz gesetzt.
#Farbverarbeitung(): Hier werden die Farbenausgelesen, je nach Farbe wird «Farbe erkannte» auf dem Bildschirm und über den Lautsprecher ausgegeben. Nur bei keinem Baustein wird zuerst noch mal gescannt, um falsch Erkennungen zu vermeiden. Anschliessend wird «Kein Auswurfobjekt erkannt» ausgegeben.
#Farb_Zaehler(): Bei dieser Funktion wird so bald aufgerufen, bei der letzten gescannten Farbe ausser bei der Farbe schwarz der Zähler um eins erhöht.
#Ton_Wiedergabe(): In dieser Funktion werden die Einstellungen für die Akustischen wiedergaben gemacht, durch (self, Wiedergabetext) kann es in dem ganzen Code individuell eingesetzt werden.
#Ausgabe_Bauteilanzahl(): Es wird die letzte Farbe wiedergegeben und eine Liste aller eingescannten Bauteile/Farben.
#Ein_Viertel_Auswurf(): Der Auswurfsarm fährt zu ¼ der Länge des Förderbandes Bewegung und wirft den Baustein aus.
#Drei_Viertel_Auswurf(): Die Funktion ist identisch wie beim Ein_Viertel_Auswurf() Bewegung nur der Auswurfsarm fährt zu ¾ das Förderband.
#Ausgangspunkt_Auswurfsarm(): Der Auswurfsarm bewegt sich zurück zur Ausgangsposition bis der Berührungssensor betätigt wird und der Arm stoppt.
#Foerderband(): Das Förderband ist das Zusammenspiel aller vorhergenannten Funktionen. Die Variabel wird gestartet sobald der Berührungssensor gedrückt wird. Anschliessend wird die Farbe gescannt. Ist die Farbe Rot wird ¾ gefahren ausgeworfen oder ist sie Grün, Gelb oder Blau wird ¼ gefahren und ausgeworfen. Wird keine Farbe erkannt, wird nur visuell und akustisch der Befehl «Kein Auswurfobjekt erkannt» ausgegeben.
#Datalog(): Loggt in eine Exel Datei die aktuelle Zeit, die Aktuelle Farbe, Anzahl der Farbe Grün, Anzahl der Farbe Blau, Anzahl der Farbe Gelb und die Anzahl der Farbe Rot, sobald es einen Farbe Wechsel gegeben hat.

#Komponenten:	Funktion:	Port:
#Farbsensor:	Farberkennung (Rot, Blau, Grün, Gelb und Unbekannt)	S2
#Touchsensor:	Referenzpunkt und Home Position für den Auswurfarm	S1
#Kleiner Motor:	Auswurf der Bausteine	B
#Grosser Motor:	Antrieb des Förderbandes	A


