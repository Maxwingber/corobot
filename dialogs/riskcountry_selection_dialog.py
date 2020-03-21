# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.dialogs import (
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    ComponentDialog, FindChoicesOptions)
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions
from botbuilder.dialogs.choices import Choice, FoundChoice
from botbuilder.core import MessageFactory


class RiskCountrySelectionDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(RiskCountrySelectionDialog, self).__init__(
            dialog_id or RiskCountrySelectionDialog.__name__
        )

        self.RISK_COUNTRIES_SELECTED = "value-symptomsSelected"
        self.DONE_OPTION = "Das war's"

        self.riskcountry_options = [
            "Ägypten",
            "Hubei (China)",
            "Region Grand Est (Frankreich)",
            "Iran",
            "Italien",
            "Tirol (Österreich)",
            "Madrid (Spanien)",
            "Gyeongsangbuk-do (Südkorea)",
            "Kalifornien, Washington oder New York (USA)",
        ]
        choice = ChoicePrompt(ChoicePrompt.__name__)
        choice.recognizer_options = FindChoicesOptions(allow_partial_matches=True)
        self.add_dialog(choice)
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__, [self.selection_step, self.loop_step]
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def selection_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # step_context.options will contains the value passed in begin_dialog or replace_dialog.
        # if this value wasn't provided then start with an emtpy selection list.  This list will
        # eventually be returned to the parent via end_dialog.
        selected: [
            str
        ] = step_context.options if step_context.options is not None else []
        step_context.values[self.RISK_COUNTRIES_SELECTED] = selected

        if len(selected) == 0:
            message = (
                f"Im Folgenden finden Sie eine Liste von Regionen. Waren Sie in letzter Zeit in einer dieser Regionen? Falls nicht, sagen Sie `{self.DONE_OPTION}`."
            )
        else:
            message = (
                f"Sie waren in **{selected[len(selected)-1]}**. Waren Sie in letzter Zeit in einer weiteren Region? Falls nicht, sagen Sie `{self.DONE_OPTION}`."
            )

        # create a list of options to choose, with already selected items removed.
        options = self.riskcountry_options.copy()
        options.append(self.DONE_OPTION)
        if len(selected) > 0:
            options = [item for item in options if item not in selected]

        # prompt with the list of choices
        prompt_options = PromptOptions(
            prompt=MessageFactory.text(message),
            retry_prompt=MessageFactory.text("Bitte wählen Sie eine Region oder sagen Sie " + self.DONE_OPTION + "."),
            choices=self._to_choices(options),
        )
        return await step_context.prompt(ChoicePrompt.__name__, prompt_options)

    def _to_choices(self, choices: [str]) -> List[Choice]:
        choice_list: List[Choice] = []
        for choice in choices:
            choice_list.append(Choice(value=choice))
        return choice_list

    async def loop_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        selected: List[str] = step_context.values[self.RISK_COUNTRIES_SELECTED]
        choice: FoundChoice = step_context.result
        done = choice.value == self.DONE_OPTION

        # If they chose a company, add it to the list.
        if not done:
            selected.append(choice.value)

        # If they're done, exit and return their list.
        if done or len(selected) >= len(self.riskcountry_options):
            return await step_context.end_dialog(selected)

        # Otherwise, repeat this dialog, passing in the selections from this iteration.
        return await step_context.replace_dialog(
            RiskCountrySelectionDialog.__name__, selected
        )
