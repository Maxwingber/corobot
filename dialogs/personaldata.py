# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.dialogs import (
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    ComponentDialog, ListStyle)
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions, ConfirmPrompt, TextPrompt, NumberPrompt, DateTimePrompt
from botbuilder.dialogs.choices import Choice, FoundChoice
from botbuilder.core import MessageFactory, UserState

from data_models import PersonalData


class PersonalDataDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(PersonalDataDialog, self).__init__(
            dialog_id or PersonalDataDialog.__name__
        )

        # Key name to store this dialogs state info in the StepContext
        self.PERSONAL_DATA = "value-personalData"

        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.first_name_step,
                    self.family_name_step,
                    self.gender_step,
                    self.street_step,
                    self.zipcode_step,
                    self.city_step,
                    self.telephone_step,
                    self.email_step,
                    self.birthday_step,
                    self.final_step]
            )
        )

        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            NumberPrompt(NumberPrompt.__name__)
        )
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(DateTimePrompt(DateTimePrompt.__name__))

        self.initial_dialog_id = WaterfallDialog.__name__

    async def first_name_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Create an object in which to collect the personal data within the dialog.
        step_context.values[self.PERSONAL_DATA] = PersonalData()

        # Ask the user to enter their first name.
        prompt_options = PromptOptions(
            prompt=MessageFactory.text("Bitte nennen Sie mir Ihren Vornamen.")
        )
        return await step_context.prompt(TextPrompt.__name__, prompt_options)

    async def family_name_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
            # Set the user's first name to what they entered in response to the firstname prompt.
            personal_data = step_context.values[self.PERSONAL_DATA]
            personal_data.first_name = step_context.result

            # Ask the user to enter their family name.
            prompt_options = PromptOptions(
                prompt=MessageFactory.text("Bitte nennen Sie mir Ihren Nachnamen.")
            )
            return await step_context.prompt(TextPrompt.__name__, prompt_options)

    async def gender_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
             # Set the user's first name to what they entered in response to the firstname prompt.
            personal_data = step_context.values[self.PERSONAL_DATA]
            personal_data.family_name = step_context.result

            # Ask the user to choose their gender.
            return await step_context.begin_dialog(ChoicePrompt.__name__, PromptOptions(
                prompt=MessageFactory.text("Was ist Ihr Geschlecht?"),
                choices=["Männlich", "Weiblich", "Divers"],
                style=ListStyle.suggested_action
            ))

    async def street_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
            # Set the user's gender to what they entered in response to the gender prompt.
            personal_data = step_context.values[self.PERSONAL_DATA]
            personal_data.gender = step_context.result

            # Ask the user to enter their street and number.
            prompt_options = PromptOptions(
                prompt=MessageFactory.text("Bitte nennen Sie mir Ihre Straße und Hausnummer.")
            )
            return await step_context.prompt(TextPrompt.__name__, prompt_options)

    async def zipcode_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
            # Set the user's street to what they entered in response to the street prompt.
            personal_data = step_context.values[self.PERSONAL_DATA]
            personal_data.street = step_context.result

            # Ask the user to enter their zipcode.
            prompt_options = PromptOptions(
                prompt=MessageFactory.text("Bitte nennen Sie mir Ihre Postleitzahl.")
            )
            return await step_context.prompt(TextPrompt.__name__, prompt_options)

    async def city_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
            # Set the user's zip code to what they entered in response to the zip code prompt.
            personal_data = step_context.values[self.PERSONAL_DATA]
            personal_data.zipcode = step_context.result

            # Ask the user to enter their city.
            prompt_options = PromptOptions(
                prompt=MessageFactory.text("Bitte nennen Sie mir Ihre Stadt.")
            )
            return await step_context.prompt(TextPrompt.__name__, prompt_options)

    async def telephone_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
            # Set the user's city to what they entered in response to the city prompt.
            personal_data = step_context.values[self.PERSONAL_DATA]
            personal_data.city = step_context.result

            # Ask the user to enter their telephone number.
            prompt_options = PromptOptions(
                prompt=MessageFactory.text("Bitte nennen Sie mir Ihre Telefonnummer.")
            )
            return await step_context.prompt(TextPrompt.__name__, prompt_options)

    async def email_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
            # Set the user's first name to what they entered in response to the firstname prompt.
            personal_data = step_context.values[self.PERSONAL_DATA]
            personal_data.telephone = step_context.result

            # Ask the user to enter their name.
            prompt_options = PromptOptions(
                prompt=MessageFactory.text("Bitte nennen Sie mir Ihre E-Mail-Adresse.")
            )
            return await step_context.prompt(TextPrompt.__name__, prompt_options)

    async def birthday_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
            # Set the user's email adress to what they entered in response to the email prompt.
            personal_data = step_context.values[self.PERSONAL_DATA]
            personal_data.email = step_context.result

            # Ask the user to enter their birthday.
            prompt_options = PromptOptions(
                prompt=MessageFactory.text("Bitte nennen Sie mir Ihr Geburtsdatum im Format TT.MM.JJJJ.")
            )
            return await step_context.prompt(TextPrompt.__name__, prompt_options)


    async def final_step(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:

        # Set the user's birthday to what they entered in response to the birthday prompt.
        personal_data = step_context.values[self.PERSONAL_DATA]
        personal_data.birthday = step_context.result

        return await step_context.end_dialog(personal_data)

