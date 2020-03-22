# Corobot 

![WirVsVirus Hackathon Logo](assets/Logo_Projekt_01.png)

## Problem
Während des WirVsVirus Hackathon haben wir Gesundheitsämter gefragt, welche Probleme bei der Identifizierung von Fällen von COVID-19 bestehen. Wir hatten eine Antwortrate von unglaublichen 1%! Zum Glück haben wir über 400 Gesundheitsämter kontaktiert. ;-) 

Die Ergebnisse: 
* Riskikofaktoren die immer abgefragt werden: Auslandsaufenthalt, Kontakt zu Infizierten, Symptome
* 14 Tage pflicht Quarantäne für Funktionsträger, die aus Risikogebieten zurückkehren (Hessen)
* Unterschiedlichste Verfahren zwischen den Kommunen und Ländern, bisher fehlt eine BestPractice
* Erschrekend unterschiedliche Technologiestandards, einige Komunen fragen automatisiert über Web app ab, andere nutzen Excel mit         händischer eintragung und in einem fall füllten MitarbeiterInnen Papierformulare aus 

Vielen Dank an die Folgenden Gesundheitsämter. Sie haben sich trotz der besonderen Situation die Zeit genommen und Mühe gemacht, unsere Anfrage zu beantworten. 

* Gesundheitsamt Helmstedt
* Gesundheitsamt Berlin-Spandau
* Gesundheitsamt Main-Taunus-Kreis 
* Gesundheitsamt Emden
* Gesundheitsamt Hof
* Gesundheitsamt Soest
* Gesundheitsamt Neustadt Bad-Dürkheim

## Lösung

Automatisierte Abfrage und Datenaufnahme von Menschen die aufgrund des COVID-19 die lokalen Gesunheitsämter kontaktieren. Die Abfrage läuft zunächst Online, allerdings ist alles soweit vorbereitet um auch eine telefonische Abfrage zu implementieren.

## How To

### Ausführen des Programs
- Repository klonen
```bash
git clone https://github.com/Microsoft/botbuilder-samples.git
```
- In einem Terminal in den Ordner navigieren
- `pip install -r requirements.txt` ausführen um die Anforderungen zu installieren
- `python app.py` ausführen um den Bot lokal zu starten

### Bot Testen mit Framework Emulator
Mit dem [Microsoft Bot Framework Emulator](https://github.com/microsoft/botframework-emulator) kann der Bot lokal getestet werden. 

#### Mit dem Bot verbinden
- Bot Framework Emulator ausführen
- File -> Open Bot
- Die folgende URL im Emulator öffnen: http://localhost:3978/api/messages

### Den Bot auf Azure deployen

[Deploy your bot to Azure](https://aka.ms/azuredeployment)

## Weiterführende Informationen zum Microsoft Bot Framework und Azure

- [Bot Framework Documentation](https://docs.botframework.com)
- [Bot Basics](https://docs.microsoft.com/azure/bot-service/bot-builder-basics?view=azure-bot-service-4.0)
- [Dialogs](https://docs.microsoft.com/azure/bot-service/bot-builder-concept-dialog?view=azure-bot-service-4.0)
- [Azure Bot Service Introduction](https://docs.microsoft.com/azure/bot-service/bot-service-overview-introduction?view=azure-bot-service-4.0)
- [Azure Bot Service Documentation](https://docs.microsoft.com/azure/bot-service/?view=azure-bot-service-4.0)
- [Azure CLI](https://docs.microsoft.com/cli/azure/?view=azure-cli-latest)
- [Azure Portal](https://portal.azure.com)
