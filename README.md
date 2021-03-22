# SCM-Rechner

## Lokal laufen lassen
- Sicherste Methode um etwaigen Serverproblemen vorzubeugen
- Wenn du das schon mal gemacht hast ists super einfach. 
- Nutze am besten Python 3.8 auf 3.9 läuft noch nicht alles 
- venv erstellen
- requirements.txt installieren
- main.py laufen lassen (kein app.run() benötigt. Einfach ganz normal wie ein Python Programm)
- auf dem localhost:5000 läuft das Ding dann. Bekommst aber auch einen Link in der Kommandozeile angezeigt


## Todos:
Weitere Feauteres die noch ganz gut wären:
- Dualoc und dual ascent verfahren, greedy Verfahren
- Kompaktheit
- Von Thünen Kreise
- Die Punkte auf einem Graphen darstellen, inklusive der Kreise (Super unnötig)
- Website mit eigener Domain verbinden um zu testen, wie das so funktioniert


## Notiz an mich zum Deployment
Um den ganzen bums bei der GCloud zu hosten musst du das mit App-Service machen.
mit "gcloud app deploy" wird das ganze Ding hochgeladen
