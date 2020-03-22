# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from datetime import time
from typing import List

from botbuilder.dialogs import (
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    ComponentDialog)
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions, ConfirmPrompt, NumberPrompt, DateTimePrompt
from botbuilder.dialogs.choices import Choice, FoundChoice
from botbuilder.core import MessageFactory, UserState

from data_models import UserProfile


class ContactsSelectionDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(ContactsSelectionDialog, self).__init__(
            dialog_id or ContactsSelectionDialog.__name__
        )

        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.confirm_confirmedcasecontact_step,
                    self.date_confirmedcasecontact_step,
                    self.confirm_suspectedcasecontact_step,
                    self.date_suspectedcasecontact_step,
                    self.contacts_dates_step]
            )
        )

        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(
            NumberPrompt(NumberPrompt.__name__)
        )
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(DateTimePrompt(DateTimePrompt.__name__))

        self.initial_dialog_id = WaterfallDialog.__name__


    async def confirm_confirmedcasecontact_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:

        await step_context.context.send_activity(
            MessageFactory.text(
                "Finden wir heraus, ob Sie engen Kontakt zu einem bestätigten Covid-19-Fall hatten.")
        )
        #time.sleep(1)
        await step_context.context.send_activity(
            MessageFactory.text(
                f"Als enger Kontakt gilt Kontakt von Angesicht zu Angesicht länger als 15 Minuten, oder direkter, physischer Kontakt (Berührung, Händeschütteln, Küssen), oder Kontakt mit oder Austausch von Körperflüssigkeiten, oder Teilen einer Wohnung.")
        )
        #time.sleep(2)
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                choices=[Choice("Ja"), Choice("Nein")],
                prompt=MessageFactory.text("Hatten Sie engen Kontakt zu einem **bestätigten Covid-19-Fall**?")
            ),
        )

    async def date_confirmedcasecontact_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        print("[DEBUG] Received by German choice prompt: " + step_context.result.value)
        if step_context.result.value == "Ja":
            # User said "yes" so we will be prompting for the date of their contact.
            # WaterfallStep always finishes with the end of the Waterfall or with another dialog,
            # here it is a Prompt Dialog.
            return await step_context.prompt(
                DateTimePrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("An welchem Tag hatten Sie das letzte Mal Kontakt? Bitte nennen Sie es im Format TT.MM.JJJJ (z.B. 03.03.2020)."),
                ),
            )
        # User said "no" so we will skip the next step. Give 00000000 as the date and asks whether there was contact to a suspected case.
        return await step_context.next(None)

    async def confirm_suspectedcasecontact_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:

        # Set the last contact date to a confirmed case to what they entered in response to the name prompt.
        self.FIRST_DATE = "value-firstDate"
        if step_context.result:
            step_context.values[self.FIRST_DATE] = str(step_context.result[0].value)
        else:
            step_context.values[self.FIRST_DATE] = None

        print("[DEBUG] First date is " + str(step_context.values[self.FIRST_DATE]))

        await step_context.context.send_activity(
            MessageFactory.text(
                "Finden wir heraus, ob Sie engen Kontakt zu einem Covid-19-Verdachtsfall hatten.")
        )
        #time.sleep(1)
        await step_context.context.send_activity(
            MessageFactory.text(
                f"Als enger Kontakt gilt Kontakt von Angesicht zu Angesicht länger als 15 Minuten, oder direkter, physischer Kontakt (Berührung, Händeschütteln, Küssen), oder Kontakt mit oder Austausch von Körperflüssigkeiten, oder Teilen einer Wohnung.")
        )
        #time.sleep(2)
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                choices=[Choice("Ja"), Choice("Nein")],
                prompt=MessageFactory.text("Hatten Sie engen Kontakt zu einem **Covid-19-Verdachtsfall**?")
            ),
        )

    async def date_suspectedcasecontact_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        print("[DEBUG] Received by German choice prompt: " + step_context.result.value)
        if step_context.result.value == "Ja":
            # User said "yes" so we will be prompting for the date of their contact.
            # WaterfallStep always finishes with the end of the Waterfall or with another dialog,
            # here it is a Prompt Dialog.
            return await step_context.prompt(
                DateTimePrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("An welchem Tag hatten Sie das letzte Mal Kontakt? Bitte nennen Sie es im Format TT.MM.JJJJ (z.B. 03.03.2020)."),
                ),
            )
        # User said "no" so we will skip the next step. Give 00000000 as the date and asks whether there was contact to a suspected case.
        return await step_context.next(None)

    async def contacts_dates_step(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:

        # Set the last contact date to a confirmed case to what they entered in response to the name prompt.
        self.SECOND_DATE = "value-secondDate"
        if not step_context.result == None:
            step_context.values[self.SECOND_DATE] = str(step_context.result[0].value)
        else:
            step_context.values[self.SECOND_DATE] = None

        print("[DEBUG] Second date is " + str(step_context.values[self.SECOND_DATE]))

        dates = [step_context.values[self.FIRST_DATE], step_context.values[self.SECOND_DATE]]

        print("[DEBUG] The dates are " + str(dates[0]) + " and " + str(dates[1]))

        return await step_context.end_dialog(dates)

