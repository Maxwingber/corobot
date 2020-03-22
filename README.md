# Corobot 

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

## Lösung
Automatisierte Abfrage und Datenaufnahme von Menschen die aufgrund des COVID-19 die lokalen Gesunheitsämter kontaktieren. Die Abfrage läuft zunächst Online, allerdings ist alles soweit vorbereitet um auch eine telefonische Abfrage zu implementieren.

## How To

### Ausführen des Programs
- Clone the repository
```bash
git clone https://github.com/Microsoft/botbuilder-samples.git
```
- Bring up a terminal, navigate to `botbuilder-samples\samples\python\43.complex-dialog` folder
- Activate your desired virtual environment
- In the terminal, type `pip install -r requirements.txt`
- Run your bot with `python app.py`

### Bot Testen mit Framework Emulator
[Microsoft Bot Framework Emulator](https://github.com/microsoft/botframework-emulator) is a desktop application that allows bot developers to test and debug their bots on localhost or running remotely through a tunnel.

- Install the Bot Framework emulator from [here](https://github.com/Microsoft/BotFramework-Emulator/releases)

#### Mit dem Bot verbinden
- Launch Bot Framework Emulator
- File -> Open Bot
- Paste this URL in the emulator window - http://localhost:3978/api/messages

### Deploy the bot to Azure

To learn more about deploying a bot to Azure, see [Deploy your bot to Azure](https://aka.ms/azuredeployment) for a complete list of deployment instructions.

## Weiterführende Literatur

- [Bot Framework Documentation](https://docs.botframework.com)
- [Bot Basics](https://docs.microsoft.com/azure/bot-service/bot-builder-basics?view=azure-bot-service-4.0)
- [Dialogs](https://docs.microsoft.com/azure/bot-service/bot-builder-concept-dialog?view=azure-bot-service-4.0)
- [Azure Bot Service Introduction](https://docs.microsoft.com/azure/bot-service/bot-service-overview-introduction?view=azure-bot-service-4.0)
- [Azure Bot Service Documentation](https://docs.microsoft.com/azure/bot-service/?view=azure-bot-service-4.0)
- [Azure CLI](https://docs.microsoft.com/cli/azure/?view=azure-cli-latest)
- [Azure Portal](https://portal.azure.com)
