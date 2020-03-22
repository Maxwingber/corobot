# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import base64
from datetime import date

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
            prompt = MessageFactory.text("Waren Sie seit 01.01.2020 im Ausland?")
        )

        return await step_context.begin_dialog(ChoicePrompt.__name__, prompt_options)

    async def start_riskcountry_selection_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        print("[DEBUG] Received by German choice prompt: " + step_context.result.value)
        riskcountry_true = step_context.result.value == "Ja"

        if not riskcountry_true:
            print("[DEBUG] Skipping risk country selection")
            return await step_context.next([])
        else:
            print("[DEBUG] Entering risk country selection")
            return await step_context.begin_dialog(RiskCountrySelectionDialog.__name__)



    async def start_symptom_selection_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # Set the user's age to what they entered in response to the age prompt.
        print("[DEBUG] Arrived in symptom selection")
        user_profile: UserProfile = step_context.values[self.USER_INFO]
        user_profile.risk_countries = step_context.result
        if user_profile.risk_countries is not None and len(user_profile.risk_countries) > 0:
            user_profile.risk_countries_bool = True

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
                choices=["Polizei", "Feuerwehr", "Richter", "Staatsanwälte", "Justizvollzug", "Rettungsdienst", "THW",
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
                    f"Da Sie als Kontaktperson der Kategorie 1 eingestuft werden, **melden Sie sich bitte sofort bei Ihrem zuständigen Gesundheitsamt**. Außerdem bitten wir Sie noch einige persönliche Daten für die Übermittlung an das Gesundheitsamt bereitzustellen. **Überwachen Sie bitte zudem Ihre Symptome** und **begeben Sie sich in häusliche Quarantäne**. Empfehlungen zu Ihrem weiteren Handeln finden Sie auf rki.de")
            )
            # Start the personal data dialog.
            return await step_context.begin_dialog(PersonalDataDialog.__name__)

        if user_profile.risk_countries_bool is True and user_profile.critical_symptoms_bool is True:
            # Thank them for participating.
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"Da Sie sich in den letzten 14 Tagen in einer Risikoregion aufgehalten haben und für Covid-19-typische Symptome zeigen, **melden Sie sich bitte bei Ihrem zuständigen Gesundheitsamt**. Außerdem bitten wir Sie noch einige persönliche Daten für die Übermittlung an das Gesundheitsamt bereitzustellen. **Überwachen Sie bitte zudem Ihre Symptome** und **begeben Sie sich in häusliche Quarantäne**. Empfehlungen zu Ihrem weiteren Handeln finden Sie auf rki.de")
            )
            # Start the personal data dialog.
            return await step_context.begin_dialog(PersonalDataDialog.__name__)

        if user_profile.contact_risk_2_bool is True:
            # Thank them for participating.
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"Bitte warten Sie ab, ob sich Ihre Kontaktperson als bestätigter Fall herausstellt. Sollte sich der Fall bestätigen, melden Sie sich bitte bei Ihrem zuständigen Gesundheitsamt. Für diesen Fall bitten wir Sie noch einige persönliche Daten für die Übermittlung an das Gesundheitsamt bereitzustellen. **Überwachen Sie zudem bitte Ihre Symptome** und **begeben Sie sich in häusliche Quarantäne**. Empfehlungen zu Ihrem weiteren Handeln finden Sie auf rki.de")
            )
            # Start the personal data dialog.
            return await step_context.begin_dialog(PersonalDataDialog.__name__)

        if user_profile.critical_symptoms_bool is True and user_profile.critical_job is True:
            # Thank them for participating.
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"Sie gelten nicht als Kontaktperson, arbeiten jedoch in einem systemkritischen Beruf. Bitte **melden Sie sich bei Ihrem zuständigen Gesundheitsamt**. Außerdem bitten wir Sie noch einige persönliche Daten für die Übermittlung an das Gesundheitsamt bereitzustellen. **Überwachen Sie zudem bitte Ihre Symptome** und **begeben Sie sich in häusliche Quarantäne**. Empfehlungen zu Ihrem weiteren Handeln finden Sie auf rki.de")
            )
            # Start the personal data dialog.
            return await step_context.begin_dialog(PersonalDataDialog.__name__)

        if user_profile.risk_countries_bool is True:
            # Thank them for participating.
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"Da Sie sich in den letzten 14 Tagen in einer Risikoregion aufgehalten haben, **überwachen Sie bitte ob Sie Covid-19-typische Symptome entwickeln** und **begeben Sie sich in häusliche Quarantäne**. Empfehlungen zu Ihrem weiteren Handeln finden Sie auf rki.de")
            )
            # Start the personal data dialog.
            return await step_context.next(PersonalData())

        if user_profile.critical_symptoms_bool is True and user_profile.age > 59:
            # Thank them for participating.
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"Sie gelten nicht als Kontaktperson, gehören jedoch zu einer erhöhten Risikogruppe. Bitte **überwachen Sie Ihre Symptome** und **begeben Sie sich in häusliche Quarantäne**. Empfehlungen zu Ihrem weiteren Handeln finden Sie auf rki.de")
            )
            # No personal data required. Return empty personal data.
            return await step_context.next(PersonalData())

        if user_profile.critical_symptoms_bool is True:
            # Thank them for participating.
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"Sie gelten nicht als Kontaktperson. Bitte **überwachen Sie Ihre Symptome** und **begeben Sie sich in häusliche Quarantäne**. Empfehlungen zu Ihrem weiteren Handeln finden Sie auf rki.de")
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

        # Thank them for participating.
        await step_context.context.send_activity(
            MessageFactory.text(f"Danke für Ihre Mithilfe und das Beantworten der Fragen, {user_profile.name}. Bitte bleiben Sie wenn möglich zu Hause und verlassen Sie Ihr zu Hause nur wenn absolut notwendig.")
        )

        await step_context.context.send_activity(
            MessageFactory.text(f"Bei weiterer Kommunikation mit Behörden können Sie folgende Zeile anhängen und sparen "
                                f"sich lästige erneute Nachfragen.")
        )

        try:

            await step_context.context.send_activity(
                #symptoms_str: str = None
                #if str(user_profile.symptoms) == "[]":
                #    symptoms_str = "keine"
                #else:
                #    symptoms_str = str(user_profile.symptoms) + " seit " + user_profile.symptoms_date

                # MessageFactory.text(base64.b64encode(bytearray(str(user_profile.__dict__), 'utf-8'))) TODO
                #MessageFactory.text(str(user_profile.__dict__) + "\n" + str(user_profile.personal_data.__dict__))
                
                MessageFactory.text("Ihre Angaben:\n\nName, Vorname: " + user_profile.personal_data.family_name + ", " + user_profile.personal_data.first_name +\
                "\n\nGeburtsdatum: " + user_profile.personal_data.birthday +\
                "\n\nGeschlecht: " + user_profile.personal_data.gender +\
                "\n\nAdresse: " + user_profile.personal_data.street + ", " + user_profile.personal_data.zipcode + " " + user_profile.personal_data.city +\
                "\n\nTelefonnr.: " + user_profile.personal_data.telephone +\
                "\n\nEmail: " + user_profile.personal_data.email +\
                "\n\n\n\nSymptome: " + str(user_profile.symptoms) if len(user_profile.symptoms) is not 0 else "keine" +\
                ("Fiebertemparatur: " + user_profile.fever_temp) if 'Fieber' in user_profile.symptoms else "" +\
                "\n\nBesuchte Risikogebiete: " + str(user_profile.risk_countries) +\
                "\n\nKontakt mit infizierter Person: " + ("ja, am " + user_profile.contact_risk_1_date) if user_profile.contact_risk_1_bool else "nein" +\
                "\n\n")
                
                
            )

        except:

            await step_context.context.send_activity(
                MessageFactory.text("Ihre Angaben:\n\nSymptome: " + str(user_profile.symptoms) if len(user_profile.symptoms) is not 0 else "keine" +\
                ("Fiebertemparatur: " + user_profile.fever_temp) if 'Fieber' in user_profile.symptoms else "" +\
                "\n\nBesuchte Risikogebiete: " + str(user_profile.risk_countries) +\
                "\n\nKontakt mit infizierter Person: " + ("ja, am " + user_profile.contact_risk_1_date) if user_profile.contact_risk_1_bool else "nein" +\
                "\n\n")
            )

        print("[DEBUG] Final user object created:\n" + str(user_profile.__dict__))

        # Exit the dialog, returning the collected user information.
        return await step_context.end_dialog(user_profile)


