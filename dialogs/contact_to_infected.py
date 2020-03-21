# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.dialogs import (
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    ComponentDialog,
    NumberPrompt, ConfirmPrompt)
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
                    #self.close_contact_step,
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

    #async def close_contact_step(
    #        self, step_context: WaterfallStepContext
    #) -> DialogTurnResult:
    #    await step_context.context.send_activity(
    #        MessageFactory.text(f"Als enger Kontakt gilt ...")
    #    )

    async def confirm_confirmedcasecontact_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:

        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Hatten Sie Kontakt zu einem bestätigten Fall?")
            ),
        )

    async def date_confirmedcasecontact_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:

        if step_context.result:
            # User said "yes" so we will be prompting for the date of their contact.
            # WaterfallStep always finishes with the end of the Waterfall or with another dialog,
            # here it is a Prompt Dialog.
            return await step_context.prompt(
                DateTimePrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("An welchem Tag hatten Sie das letzte Mal Kontakt (Format TTMMJJJJ)?."),
                ),
            )

            # User said "no" so we will skip the next step. Give 00000000 as the date.
        return await step_context.next()



