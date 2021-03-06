# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import base64
from datetime import date, time

from botbuilder.core import MessageFactory
from botbuilder.dialogs import (
    WaterfallDialog,
    DialogTurnResult,
    WaterfallStepContext,
    ComponentDialog,
    ConfirmPrompt, Choice, ChoicePrompt, ChoiceFactory, FindChoicesOptions, ListStyle, DialogTurnStatus)
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt

from data_models import UserProfile
from data_models import PersonalData
from dialogs.contact_to_infected import ContactsSelectionDialog
from dialogs.symptoms_selection_dialog import SymptomsSelectionDialog
from dialogs.riskcountry_selection_dialog import RiskCountrySelectionDialog
from dialogs.personaldata import PersonalDataDialog




class TopLevelDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(TopLevelDialog, self).__init__(dialog_id or TopLevelDialog.__name__)

        # Key name to store this dialogs state info in the StepContext
        self.USER_INFO = "value-userInfo"

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))

        choice = ChoicePrompt(ChoicePrompt.__name__)
        choice.recognizer_options = FindChoicesOptions(allow_partial_matches=True)
        self.add_dialog(choice)

        self.add_dialog(SymptomsSelectionDialog(SymptomsSelectionDialog.__name__))
        self.add_dialog(ContactsSelectionDialog(ContactsSelectionDialog.__name__))
        self.add_dialog(PersonalDataDialog(PersonalDataDialog.__name__))
        self.add_dialog(RiskCountrySelectionDialog(RiskCountrySelectionDialog.__name__))

        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.name_step,
                    self.age_step,
                    self.confirm_riskcountry_step,
                    self.start_riskcountry_selection_step,
                    self.start_symptom_selection_step,
                    self.temparature_step,
                    self.start_contacts_step,
                    self.job_claim_step,
                    self.job_type_step,
                    self.personal_data_step,
                    self.acknowledgement_step,
                ],
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def name_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Create an object in which to collect the user's information within the dialog.
        step_context.values[self.USER_INFO] = UserProfile()

        # Ask the user to enter their name.
        prompt_options = PromptOptions(
            prompt=MessageFactory.text("Wie heißen Sie denn?")
        )
        return await step_context.prompt(TextPrompt.__name__, prompt_options)

    async def age_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Set the user's name to what they entered in response to the name prompt.
        user_profile = step_context.values[self.USER_INFO]
        user_profile.name = step_context.result

        # Ask the user to enter their age.
        prompt_options = PromptOptions(
            prompt=MessageFactory.text("Hallo " + user_profile.name + "! Wie alt sind Sie?"),
            retry_prompt=MessageFactory.text("Bitte geben Sie Ihr Alter als Zahl an.")
        )
        return await step_context.prompt(NumberPrompt.__name__, prompt_options)

    async def confirm_riskcountry_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        user_profile: UserProfile = step_context.values[self.USER_INFO]
        user_profile.age = int(step_context.result)

        prompt_options = PromptOptions(
            choices = [Choice("Ja"), Choice("Nein")],
            prompt = MessageFactory.text("Waren Sie dieses Jahr bereits im Ausland?")
        )

        return await step_context.begin_dialog(ChoicePrompt.__name__, prompt_options)

    async def start_riskcountry_selection_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        print("[DEBUG] Received by German choice prompt: " + step_context.result.value)
        riskcountry_true = step_context.result.value == "Ja"

        if not riskcountry_true:
            print("[DEBUG] Skipping risk country selection")
            return await step_context.next([[],[]])
        else:
            print("[DEBUG] Entering risk country selection")
            return await step_context.begin_dialog(RiskCountrySelectionDialog.__name__)



    async def start_symptom_selection_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # Set the user's age to what they entered in response to the age prompt.
        print("[DEBUG] Arrived in symptom selection")
        print("[DEBUG] Risk countries dialog result is " + str(step_context.result))
        user_profile: UserProfile = step_context.values[self.USER_INFO]
        user_profile.risk_countries = step_context.result[0]
        user_profile.risk_country_returndates = step_context.result[1]

        if user_profile.risk_countries is not None and len(user_profile.risk_countries) > 0:
            for single_date in user_profile.risk_country_returndates:
                print("[DEBUG] Looking at return date " + single_date)
                print("[DEBUG] Time diff return date: " + str(
                    int(date.today().strftime("%Y%m%d")) - int(single_date.replace("-", ""))))
                if int(date.today().strftime("%Y%m%d")) - int(single_date.replace("-", "")) <= 14:
                    print("[DEBUG] Set risk country bool to True")
                    user_profile.risk_countries_bool = True

        print("[DEBUG] Risk countries and returndates are\n" + str(user_profile.risk_countries) + "\n" + str(user_profile.risk_country_returndates))

        # Otherwise, start the review selection dialog.
        return await step_context.begin_dialog(SymptomsSelectionDialog.__name__)

    async def temparature_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Set the user's name to what they entered in response to the name prompt.
        user_profile: UserProfile = step_context.values[self.USER_INFO]
        user_profile.symptoms = step_context.result[0]
        user_profile.symptoms_dates = step_context.result[1]
        print("[DEBUG] Symptoms are " + str(user_profile.symptoms))
        print("[DEBUG] Corresponding dates are " + str(user_profile.symptoms))
        if user_profile.symptoms is not None and len(user_profile.symptoms) > 0 and (any(user_profile.symptoms) is x for x in ['Husten', 'Lungenentzündung', 'Fieber']):
            print("[DEBUG] Setting critical symtoms bool to true with symptoms " + str(user_profile.symptoms))
            user_profile.critical_symptoms_bool = True

        if "Fieber" in user_profile.symptoms:
            prompt_options = PromptOptions(
                prompt=MessageFactory.text("Wie hoch ist Ihr Fieber in Grad Celsius (°C)?")
            )
            return await step_context.prompt(TextPrompt.__name__, prompt_options)
        else:
            print("[DEBUG] Skipping fever temparature input")
            return await step_context.next("0")

    async def start_contacts_step(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # Set the user's age to what they entered in response to the age prompt.
        user_profile: UserProfile = step_context.values[self.USER_INFO]
        user_profile.fever_temp = float(step_context.result.replace(",", "."))

        # tart the contacts dialog.
        return await step_context.begin_dialog(ContactsSelectionDialog.__name__)

    async def job_claim_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_profile: UserProfile = step_context.values[self.USER_INFO]
        # Storing contacts and setting bools
        contact_dates = step_context.result
        user_profile.contact_risk_1_date = contact_dates[0]
        user_profile.contact_risk_2_date = contact_dates[1]
        print("[DEBUG] Current date " + date.today().strftime("%Y%m%d"))
        if contact_dates[0] is not None:
            print("[DEBUG] " + contact_dates[0])
            print("[DEBUG] Time diff risk contact 1: " + str(int(date.today().strftime("%Y%m%d")) - int(user_profile.contact_risk_1_date.replace("-", ""))))
            if int(date.today().strftime("%Y%m%d")) - int(user_profile.contact_risk_1_date.replace("-", "")) <= 14:
                user_profile.contact_risk_1_bool = True
        if contact_dates[1] is not None:
            print("[DEBUG] " + contact_dates[1])
            print("[DEBUG] Time diff risk contact 2: " + str(int(date.today().strftime("%Y%m%d")) - int(user_profile.contact_risk_2_date.replace("-", ""))))
            if int(date.today().strftime("%Y%m%d")) - int(user_profile.contact_risk_2_date.replace("-", "")) <= 14:
                user_profile.contact_risk_2_bool = True

        return await step_context.begin_dialog(ChoicePrompt.__name__, PromptOptions(
            prompt=MessageFactory.text("Arbeiten Sie in einem systemkritischen Bereich?"),
            choices=[Choice("Ja"), Choice("Nein")]
        ))

    async def job_type_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if step_context.result.value == "Ja":
            print("[DEBUG] Recognized system cricital job claim")
            return await step_context.begin_dialog(ChoicePrompt.__name__, PromptOptions(
                prompt=MessageFactory.text("Zu welcher systemkritischen Gruppe gehören Sie?"),
                choices=["Polizei", "Feuerwehr", "RichterIn", "Staatsanwälte", "Justizvollzug", "Rettungsdienst", "THW",
                         "Katastrophenschutz", "Mediziner", "Pfleger", "Apotheher", "**Keine**"],
                style=ListStyle.list_style
            ))
        else:
            return await step_context.next(Choice("**Keine**"))



    async def personal_data_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Set the user's company selection to what they entered in the review-selection dialog.
        user_profile: UserProfile = step_context.values[self.USER_INFO]
        if step_context.result.value != "**Keine**":
            user_profile.critical_job = step_context.result.value

        # If the user was in contact with a confirmed case in the past 14 days, he needs to add his personal data and contact the GA
        if user_profile.contact_risk_1_bool is True:
            # Thank them for participating.
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"Da Sie als Kontaktperson der Kategorie 1 eingestuft werden, **melden Sie sich bitte sofort bei Ihrem zuständigen Gesundheitsamt**. Außerdem bitten wir Sie noch einige persönliche Daten für die Übermittlung an das Gesundheitsamt bereitzustellen. **Überwachen Sie bitte zudem Ihre Symptome**, **verlassen Sie Ihre Wohnung so wenig wie möglich** und **reduzieren Sie Ihren Kontakt zu anderen Personen auf das Nötigste**. Empfehlungen zu Ihrem weiteren Handeln finden Sie auf den Seiten des Robert Koch-Instituts (rki.de)")
            )
            # Start the personal data dialog.
            return await step_context.begin_dialog(PersonalDataDialog.__name__)

        if user_profile.risk_countries_bool is True and user_profile.critical_symptoms_bool is True:
            # Thank them for participating.
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"Da Sie sich in den letzten 14 Tagen in einer Risikoregion aufgehalten haben und für Covid-19-typische Symptome zeigen, **melden Sie sich bitte bei Ihrem zuständigen Gesundheitsamt**. Außerdem bitten wir Sie noch einige persönliche Daten für die Übermittlung an das Gesundheitsamt bereitzustellen. **Überwachen Sie bitte zudem Ihre Symptome**, **verlassen Sie Ihre Wohnung so wenig wie möglich** und **reduzieren Sie Ihren Kontakt zu anderen Personen auf das Nötigste**. Empfehlungen zu Ihrem weiteren Handeln finden Sie auf den Seiten des Robert Koch-Instituts (rki.de)")
            )
            # Start the personal data dialog.
            return await step_context.begin_dialog(PersonalDataDialog.__name__)

        if user_profile.contact_risk_2_bool is True:
            # Thank them for participating.
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"Bitte warten Sie ab, ob sich Ihre Kontaktperson als bestätigter Fall herausstellt. Sollte sich der Fall bestätigen, melden Sie sich bitte bei Ihrem zuständigen Gesundheitsamt. Für diesen Fall bitten wir Sie noch einige persönliche Daten für die Übermittlung an das Gesundheitsamt bereitzustellen. **Überwachen Sie zudem bitte Ihre Symptome**, **verlassen Sie Ihre Wohnung so wenig wie möglich** und **reduzieren Sie Ihren Kontakt zu anderen Personen auf das Nötigste**. Empfehlungen zu Ihrem weiteren Handeln finden Sie auf den Seiten des Robert Koch-Instituts (rki.de)")
            )
            # Start the personal data dialog.
            return await step_context.begin_dialog(PersonalDataDialog.__name__)

        if user_profile.critical_symptoms_bool is True and user_profile.critical_job is True:
            # Thank them for participating.
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"Sie gelten nicht als Kontaktperson, arbeiten jedoch in einem systemkritischen Beruf. Bitte **melden Sie sich bei Ihrem zuständigen Gesundheitsamt**. Außerdem bitten wir Sie noch einige persönliche Daten für die Übermittlung an das Gesundheitsamt bereitzustellen. Empfehlungen zu Ihrem weiteren Handeln finden Sie auf den Seiten des Robert Koch-Instituts (rki.de)")
            )
            # Start the personal data dialog.
            return await step_context.begin_dialog(PersonalDataDialog.__name__)

        if user_profile.risk_countries_bool is True:
            # Thank them for participating.
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"Da Sie sich in den letzten 14 Tagen in einer Risikoregion aufgehalten haben, **überwachen Sie bitte ob Sie Covid-19 typische Symptome entwickeln**, **verlassen Sie Ihre Wohnung so wenig wie möglich** und **reduzieren Sie Ihren Kontakt zu anderen Personen auf das Nötigste**. Empfehlungen zu Ihrem weiteren Handeln finden Sie auf den Seiten des Robert Koch-Instituts (rki.de)")
            )
            # Start the personal data dialog.
            return await step_context.next(PersonalData())

        if user_profile.critical_symptoms_bool is True and user_profile.age > 59:
            # Thank them for participating.
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"Sie gelten nicht als Kontaktperson, gehören jedoch zu einer erhöhten Risikogruppe. Bitte **überwachen Sie Ihre Symptome**, **verlassen Sie Ihre Wohnung so wenig wie möglich** und **reduzieren Sie Ihren Kontakt zu anderen Personen auf das Nötigste**. Empfehlungen zu Ihrem weiteren Handeln finden Sie auf den Seiten des Robert Koch-Instituts (rki.de)")
            )
            # No personal data required. Return empty personal data.
            return await step_context.next(PersonalData())

        if user_profile.critical_symptoms_bool is True:
            # Thank them for participating.
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"Sie gelten nicht als Kontaktperson. Bitte **überwachen Sie Ihre Symptome**, **verlassen Sie Ihre Wohnung so wenig wie möglich** und **reduzieren Sie Ihren Kontakt zu anderen Personen auf das Nötigste**. Empfehlungen zu Ihrem weiteren Handeln finden Sie auf den Seiten des Robert Koch-Instituts (rki.de)")
            )
            # No personal data required. Return empty personal data.
            return await step_context.next(PersonalData())

            # No personal data required. Return empty personal data.
        else:
            return await step_context.next(PersonalData())


    async def acknowledgement_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # Set the user's personal data to what they entered in the personal data dialog.
        user_profile: UserProfile = step_context.values[self.USER_INFO]
        user_profile.personal_data = None       #SCHAUEN OB NÖTIG
        user_profile.personal_data = step_context.result

        #time.sleep(1)
        # Thank them for participating.
        await step_context.context.send_activity(
            MessageFactory.text(f"Danke für Ihre Mithilfe und das Beantworten der Fragen, {user_profile.name}. Bitte halten Sie sich an die aktuell geltenden Regelungen und Empfehlungen der Behörden und des Robert Koch-Instituts (rki.de).")
        )
        #time.sleep(1)
        await step_context.context.send_activity(
            MessageFactory.text(f"Bei weiterer Kommunikation mit Behörden können Sie folgende Zusammenfassung anhängen und sparen "
                                f"sich lästige erneute Nachfragen.")
        )
        ausgabe = "**Wichtige Daten für Ihr Gesundheitsamt**\n\n"
        #ausgabe = "Ihre Angaben:"

        try:

            ausgabe += "\n\nName, Vorname: " + user_profile.personal_data.family_name + ", " + user_profile.personal_data.first_name
            ausgabe += "\n\nGeburtsdatum: " + user_profile.personal_data.birthday
            ausgabe += "\n\nGeschlecht: " + user_profile.personal_data.gender
            ausgabe += "\n\nAdresse: " + user_profile.personal_data.street + ", " + user_profile.personal_data.zipcode + " " + user_profile.personal_data.city
            ausgabe += "\n\nTelefonnr.: " + user_profile.personal_data.telephone
            ausgabe += "\n\nEmail: " + user_profile.personal_data.email
        
        except:

            print("[DEBUG] no personal_data")

        take_out = ""
        take_out += "\n\nSymptome: "
        if (len(user_profile.symptoms) > 0):
            for i in range(0,len(user_profile.symptoms)):
                take_out += user_profile.symptoms[i] + " seit " + user_profile.symptoms_dates[i] + ", "#
            take_out = take_out[0:len(take_out)-2]
        else:
            take_out += "keine"

        if (user_profile.fever_temp != 0.0):
            take_out += "\n\nFiebertemperatur: " + str(user_profile.fever_temp).replace(".", ",") + "°C"
        
        take_out += "\n\nBesuchte Risikogebiete: "
        if (user_profile.risk_countries_bool):
            for i in range(0, len(user_profile.risk_countries)):
                take_out += user_profile.risk_countries[i] + " bis " + user_profile.risk_country_returndates[i] + ", "
            take_out = take_out[0:len(take_out)-2]
        else:
            take_out += "keine"
        
        ausgabe += take_out

        ausgabe += "\n\nKontakt mit infizierter Person: " 
        if user_profile.contact_risk_1_date is not None:
            ausgabe += "ja, am " + str(user_profile.contact_risk_1_date)
        else:
            ausgabe += "nein"

        ausgabe += "\n\nKontakt mit Verdachtsperson: " 
        if user_profile.contact_risk_2_date is not None:
            ausgabe += "ja, am " + str(user_profile.contact_risk_2_date)
        else:
            ausgabe += "nein"

        ausgabe += "\n\nFunktionsträger: "
        if user_profile.critical_job is not None:
            ausgabe += user_profile.critical_job
        else:
            ausgabe += "nein"

        #time.sleep(1)
        await step_context.context.send_activity(

            MessageFactory.text(ausgabe) 
        )


        print("[DEBUG] Final user object created:\n" + str(user_profile.__dict__))

        # Exit the dialog, returning the collected user information.
        return await step_context.end_dialog(user_profile)


