# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

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
                    self.date_confirmedcasecontact_step]
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
                "Finden wir heraus, ob Sie Kontakt zu einem bestätigten Covid-19-Fall hatten.")
        )
        await step_context.context.send_activity(
            MessageFactory.text(
            f"Als enger Kontakt gilt Kontakt von Angesicht zu Angesicht länger als 15 Minuten, oder direkter, physischer Kontakt (Berührung, Händeschütteln, Küssen), oder Kontakt mit oder Austausch von Körperflüssigkeiten, oder Teilen einer Wohnung.")
        )

        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                choices=[Choice("Ja"), Choice("Nein")],
                prompt=MessageFactory.text("Hatten Sie engen Kontakt zu einem bestätigten Fall?")
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
        # User said "no" so we will skip the next step. Give 00000000 as the date.
        return await step_context.next("01.01.2000")



