# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import MessageFactory
from botbuilder.dialogs import (
    WaterfallDialog,
    DialogTurnResult,
    WaterfallStepContext,
    ComponentDialog,
    ConfirmPrompt, Choice, ChoicePrompt, ChoiceFactory, FindChoicesOptions, ListStyle, DialogTurnStatus)
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt

from data_models import UserProfile
from dialogs.contact_to_infected import ContactsSelectionDialog
from dialogs.symptoms_selection_dialog import SymptomsSelectionDialog
from dialogs.riskcountry_selection_dialog import RiskCountrySelectionDialog



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
            prompt=MessageFactory.text("Bitte nennen Sie mir Ihren vollen Namen.")
        )
        return await step_context.prompt(TextPrompt.__name__, prompt_options)

    async def age_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Set the user's name to what they entered in response to the name prompt.
        user_profile = step_context.values[self.USER_INFO]
        user_profile.name = step_context.result

        # Ask the user to enter their age.
        prompt_options = PromptOptions(
            prompt=MessageFactory.text("Wie alt sind Sie?"),
            retry_prompt=MessageFactory.text("Bitte geben Sie Ihr Alter als Zahl an.")
        )
        return await step_context.prompt(NumberPrompt.__name__, prompt_options)

    async def confirm_riskcountry_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        user_profile: UserProfile = step_context.values[self.USER_INFO]
        user_profile.age = step_context.result

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

    async def temparature_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Set the user's name to what they entered in response to the name prompt.
        user_profile = step_context.values[self.USER_INFO]
        user_profile.risk_countries = step_context.result

        if "Fieber" in user_profile.risk_countries:
            prompt_options = PromptOptions(
                prompt=MessageFactory.text("Wie hoch ist Ihr Fieber in Grad Celsius (°C)?")
            )
            return await step_context.prompt(NumberPrompt.__name__, prompt_options)
        else:
            print("[DEBUG] Skipping fever temparature input")
            return await step_context.next(0)

    async def start_contacts_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # Set the user's age to what they entered in response to the age prompt.
        user_profile: UserProfile = step_context.values[self.USER_INFO]
        user_profile.fever_temp = step_context.result

        # Otherwise, start the review selection dialog.
        return await step_context.begin_dialog(ContactsSelectionDialog.__name__)

    async def start_symptom_selection_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # Set the user's age to what they entered in response to the age prompt.
        print("[DEBUG] Arrived in symptom selection")
        user_profile: UserProfile = step_context.values[self.USER_INFO]
        # TODO save contacts dates

        # Otherwise, start the review selection dialog.
        return await step_context.begin_dialog(SymptomsSelectionDialog.__name__)

    async def job_claim_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_profile: UserProfile = step_context.values[self.USER_INFO]
        user_profile.symptoms = step_context.result
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

    async def acknowledgement_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # Set the user's company selection to what they entered in the review-selection dialog.
        user_profile: UserProfile = step_context.values[self.USER_INFO]
        if step_context.result.value != "**Keine**":
                user_profile.critical_job = step_context.result

        # Thank them for participating.
        await step_context.context.send_activity(
            MessageFactory.text(f"Danke für Ihre Mithilfe und das Beantworten der Fragen, {user_profile.name}. ")
        )

        await step_context.context.send_activity(
            MessageFactory.text(f"Bei weiterer Kommunikation mit Behörden können Sie folgende Zeile anhängen und sparen "
                                f"sich lästige erneute Nachfragen.")
        )

        await step_context.context.send_activity(
            MessageFactory.text(user_profile.__dict__)
        )

        print("[DEBUG] Final user object created:\n" + str(user_profile.__dict__))

        # Exit the dialog, returning the collected user information.
        return await step_context.end_dialog(user_profile)


