# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import MessageFactory
from botbuilder.dialogs import (
    WaterfallDialog,
    DialogTurnResult,
    WaterfallStepContext,
    ComponentDialog,
    ConfirmPrompt)
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
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__, default_locale="de"))

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
                    self.start_contacts_step,
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
            prompt=MessageFactory.text("Bitte nennen Sie Ihren vollen Namen.")
        )
        return await step_context.prompt(TextPrompt.__name__, prompt_options)

    async def age_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Set the user's name to what they entered in response to the name prompt.
        user_profile = step_context.values[self.USER_INFO]
        user_profile.name = step_context.result

        # Ask the user to enter their age.
        prompt_options = PromptOptions(
            prompt=MessageFactory.text("Bitte geben Sie Ihr Alter ein.")
        )
        return await step_context.prompt(NumberPrompt.__name__, prompt_options)

    async def confirm_riskcountry_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        user_profile: UserProfile = step_context.values[self.USER_INFO]
        user_profile.age = step_context.result

        prompt_options = PromptOptions(
            prompt=MessageFactory.text("Sind Sie seit 01.01.2020 gereist?")
        )

        return await step_context.begin_dialog(ConfirmPrompt.__name__, prompt_options)

    async def start_riskcountry_selection_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:

        user_profile: UserProfile = step_context.values[self.USER_INFO]
        riskcountry_true = step_context.result

        if not riskcountry_true:
            return await step_context.next([])
        else:
            print("[DEBUG] Entering risk country selection")
            return await step_context.begin_dialog(RiskCountrySelectionDialog.__name__)



    async def start_symptom_selection_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # Set the user's age to what they entered in response to the age prompt.
        user_profile: UserProfile = step_context.values[self.USER_INFO]
        user_profile.risk_countries = step_context.result

        # Otherwise, start the review selection dialog.
        return await step_context.begin_dialog(SymptomsSelectionDialog.__name__)



    async def acknowledgement_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # Set the user's company selection to what they entered in the review-selection dialog.
        user_profile: UserProfile = step_context.values[self.USER_INFO]
        user_profile.symptoms = step_context.result

        # Thank them for participating.
        await step_context.context.send_activity(
            MessageFactory.text(f"Danke für Ihre Mithilfe, {user_profile.name}.")
        )

        # Exit the dialog, returning the collected user information.
        return await step_context.end_dialog(user_profile)

    async def start_contacts_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # Set the user's age to what they entered in response to the age prompt.
        user_profile: UserProfile = step_context.values[self.USER_INFO]
        user_profile.contacts = step_context.result

        # Otherwise, start the review selection dialog.
        return await step_context.begin_dialog(ContactsSelectionDialog.__name__)
