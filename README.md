# ---------------------------------------------------------------------------
# Read me zum Code Farbsortierer
# ---------------------------------------------------------------------------
# Aufbau: Der Code besteht aus zwei Teilen, der Klasse (Farbsortierer) mit allen
# Attributen und Methoden, und der While-True-Schleife (Hauptschleife), in der nur
# noch Foerderband() und DataLog() zyklisch aufgerufen werden.
#
# Komponenten:                    Funktion:                                        Port:
# Farbsensor:                     Farberkennung (Rot, Gruen, Blau, Gelb, Unbekannt)  S2
# Touchsensor links:              Referenz-/Ausgangspunkt und Endlage links          S1
# Touchsensor rechts:             Referenz-/Ausgangspunkt und Endlage rechts         S4
# Grosser Motor:                  Antrieb des Foerderbandes                          A
# Kleiner Motor:                  Auswurf der Bausteine                              B
# EV3-Display / Lautsprecher:     Visuelle und akustische Ausgabe                    -
# 
# Startablauf: Links_fahren() -> Foerderbandlaenge_Bestimmen() -> Hauptschleife.
#
# Farbzuordnung der Auswurfstellen (gemessen von S1 aus):
# Blau = 1/5, Gelb = 2/5, Gruen = 3/5, Rot = 4/5 der Foerderbandlaenge.
#
# Methoden:
# __init__(): Erstellt alle Variablen, Zaehler und uebergibt Motoren und Sensoren.
#   Enthaelt auch das Dictionary Farbname fuer die Textausgabe der Farben.
# Links_fahren(): Referenzfahrt nach links bis Touchsensor S1 betaetigt ist.
#   Setzt Ausgangssensor_Bestimmung auf 0 und gibt die Kalibrierung frei.
# Foerderbandlaenge_Bestimmen(): Faehrt von S1 bis S4 und misst die Bandlaenge in Grad.
#   Daraus werden die vier Auswurfstellen (1/5 bis 4/5) je von links und von rechts berechnet.
# Farberkennung_Pruefung(): Liest den Farbsensor fuenfmal aus und uebernimmt die
#   haeufigste Farbe. Ist diese nicht Rot, Gruen, Blau oder Gelb, wird Schwarz gesetzt.
# Farbverarbeitung(): Gibt die erkannte Farbe auf Display und Lautsprecher aus. Bei Schwarz
#   wird erst nach zwei Durchlaeufen "Kein Auswurfobjekt erkannt" gemeldet und gesperrt.
# Farb_Zaehler(): Erhoeht den Zaehler der zuletzt erkannten Farbe um eins.
# Ton_Wiedergabe(Wiedergabetext): Gibt den uebergebenen Text auf Deutsch aus und ist
#   dadurch im ganzen Code frei einsetzbar.
# Ausgabe_Bauteilanzahl(): Zeigt die letzte Farbe sowie die Zaehlerstaende aller vier Farben.
# Auswurf_Mechanismus(): Hebt den Auswurfarm und faehrt ihn wieder in die Ausgangslage.
# Ein_Fuenftel_Auswurf(): Faehrt das Band auf die 1/5-Position (Blau), wirft aus und
#   faehrt zurueck zu S1. Richtung je nach Ausgangssensor_Bestimmung.
# Zwei_Fuenftel_Auswurf(): Gleicher Ablauf auf der 2/5-Position (Gelb), Rueckfahrt zu S1.
# Drei_Fuenftel_Auswurf(): Gleicher Ablauf auf der 3/5-Position (Gruen), Rueckfahrt zu S4.
# Vier_Fuenftel_Auswurf(): Gleicher Ablauf auf der 4/5-Position (Rot), Rueckfahrt zu S4.
# Ausgangspunkt_Auswurfsarm(Ziel_Sensor): Faehrt das Band zum uebergebenen Endsensor
#   zurueck und merkt sich die neue Ausgangsseite (1 = S1 links, 2 = S4 rechts).
# Foerderband(): Zusammenspiel aller Methoden. Ist S1 oder S4 betaetigt, wird die Farbe
#   erkannt und die zugehoerige Auswurfmethode, der Zaehler und die Anzeige aufgerufen.
#   Bei Schwarz wartet das Band auf einen neuen Baustein.
# DataLog(): Loggt Zeit, aktuelle Farbe und die Zaehler von Rot, Gruen, Blau und Gelb,
#   sobald ein Farbwechsel stattgefunden hat.
#
# Aenderungsprotokoll:
# (12.08.26) Erweitern des Codes mit der Farberkennung, Verarbeitung, Zaehlen der Farbe
#            und der Ausgabe der Liste
# (13.08.26) Erweitern des Codes mit dem Foerderbandantrieb und dem Auswurf der Bauteile,
#            anschliessend bauen einer Funktion fuer den Foerderbandbetrieb und
#            anschliessende Ueberpruefung auf Funktionalitaet mit Claude
# (14.08.26) Erweitern des Codes mit der Logging-Funktion sowie Fehlerbehebung
# (18.08.26) Ausbauen Ultraschallsensor und Rueckbau Code
# (24.08.26) Kalibrierung und Fehlerbehebung Kalibrierung
# (26.08.26) Anpassungen Read me: Umstellung von zwei auf vier Auswurfstellen (Fuenftel),
#            Ergaenzung Links_fahren(), Foerderbandlaenge_Bestimmen() und
#            Auswurf_Mechanismus(), Nachfuehren der Komponententabelle (S4, Port A,
#            Ultraschallsensor entfernt)
# ---------------------------------------------------------------------------
