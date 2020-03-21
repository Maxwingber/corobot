# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.dialogs import (
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    ComponentDialog,
)
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions
from botbuilder.dialogs.choices import Choice, FoundChoice
from botbuilder.core import MessageFactory


class ContactsSelectionDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(ContactsDialog, self).__init__(
            dialog_id or ContactsDialog.__name__
        )


        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__, [self.confirmedCase, self.suspectedCase]
            )
        )

        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(
            NumberPrompt(NumberPrompt.__name__, UserProfileDialog.age_prompt_validator)
        )
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))


        self.initial_dialog_id = WaterfallDialog.__name__

    async def close_contact(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # We can send messages to the user at any point in the WaterfallStep.
        await step_context.context.send_activity(
            MessageFactory.text(f"Als enger Kontakt gilt ...")
        )

    async def confirmedCase(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # step_context.options will contains the value passed in begin_dialog or replace_dialog.
        # if this value wasn't provided then start with an emtpy selection list.  This list will
        # eventually be returned to the parent via end_dialog.


            return await step_context.prompt(
                ConfirmPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Hatten Sie engen Kontakt zu einem bestätigten Fall?"),
                    ),
            )

    async def confirmedCaseDate(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
            if step_context.result:
                return await step_context.prompt(
                    NumberPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("An welchem Tag war der letzte Kontakt? Bitte geben Sie ein Datum im Format TTMMJJJJ ein."),
                    ),
                )
    # Kein engerer Kontakt. Datum = 00000000
    return await step_context.next(00000000)



