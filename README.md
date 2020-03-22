*Dieses Projekt ist WORK IN PROGRESS und nur zu Testzwecken zu verwenden.*
# Corobot 

![WirVsVirus Hackathon Logo](assets/Logo_Projekt_01.png)

## Problem
Während des [WirVsVirus](https://wirvsvirushackathon.org/) Hackathon haben wir Gesundheitsämter gefragt, welche Probleme bei der Identifizierung von Fällen von COVID-19 bestehen. Wir hatten eine Antwortrate von unglaublichen 1%! Zum Glück haben wir über 400 Gesundheitsämter kontaktiert. 😉

Die Ergebnisse: 
* Viele Riskikofaktoren werden wimmer wieder abgefragt: Auslandsaufenthalte, Kontakte zu Infizierten der Risikoklassen 1 und 2, Symptome
* Es gibt unterschiedlichste Registrierungsverfahren bei Kommunen und Ländern und bisher fehlt oftmals ein nutzbarer Best Practice
* Es herrschen signifikant unterschiedliche Technologiestandards: Einige Komunen fragen Daten bereits automatisiert über Websiten ab während andere telefonisch (und auf Papier!) Stammdaten aufnehmen
* Viel zu viel Zeit wird für die Aufnahme und Korrektur der Personendaten verbraucht

Ein besonderer Dank gebührt folgenden Gesundheitsämtern. Sie haben sich trotz der besonderen Situation die Zeit genommen und sich die Mühe gemacht, uns bei der Konkretisierung der Problempunkte zu helfen.

* Gesundheitsamt Berlin-Spandau
* Gesundheitsamt Emden
* Gesundheitsamt Helmstedt
* Gesundheitsamt Hof
* Gesundheitsamt Main-Taunus-Kreis
* Gesundheitsamt Neustadt Bad-Dürkheim
* Gesundheitsamt Soest

## Lösung

**Corobot** ermöglicht die automatisierte Datenaufnahme und -auswertung bei Menschen, die aufgrund der COVID-19-Pandemie in Deutschland die lokalen Gesundheitsämter kontaktieren. **Corobot** ist mit jedem beliebigem Frontend verknüpfbar und kann dadurch auf einer [Website](https://corobot2020.z16.web.core.windows.net/), in einem [Telegram-Bot](t.me/Corobotbot) oder am Telefon als Sprachcomputer kontaktiert werden. Die Möglichkeit zur Integration als Sprachcomputer ist besonders für Menschen ohne Internetzugang sowie zur Integration in Bürgerhotlines extrem wichtig. 

Abhängig von den angegebenen Risikofaktoren werden peronalisierte Informationen und Verhaltensratschläge angezeigt. Das ermittelte Risikoprofil und die Stammdaten werden bei Bedarf als Data Takeout angeboten statt zentral gespeichert, um diese maschinen- und menschenlesbar, gesammelt und datenschutzfreundlich an das lokale Gesundheitsamt übermittelbar zu machen. Dadurch wird **Corobot** die Gespräche in Hotlines verkürzen, einen höheren Durchsatz erzugen und damit die Wartezeiten für BügerInnen verkürzen.

## How To

### Ausführen des Programs
- Repository klonen
```bash
git clone https://github.com/Maxwingber/corobot.git
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
