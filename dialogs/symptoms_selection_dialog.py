# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.dialogs import (
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    ComponentDialog,
    FindChoicesOptions, DateTimePrompt)
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions
from botbuilder.dialogs.choices import Choice, FoundChoice
from botbuilder.core import MessageFactory


class SymptomsSelectionDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(SymptomsSelectionDialog, self).__init__(
            dialog_id or SymptomsSelectionDialog.__name__
        )

        self.SYMPTOMS_SELECTED = "value-symptomsSelected"
        self.SYMPTOMS_DATES = "value-symptomsDates"
        self.DONE_OPTION = "Keins"

        self.symptom_options = [
            "Husten",
            "Fieber",
            "Schnupfen",
            "Kopfschmerzen",
            "Lungenentzündung",
        ]

        choice = ChoicePrompt(ChoicePrompt.__name__)
        choice.recognizer_options = FindChoicesOptions(allow_partial_matches=True)
        self.add_dialog(choice)
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__, [self.selection_step, self.loop_step, self.save_step]
            )
        )
        self.add_dialog(DateTimePrompt(DateTimePrompt.__name__))

        self.initial_dialog_id = WaterfallDialog.__name__

    async def selection_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        # step_context.options will contains the value passed in begin_dialog or replace_dialog.
        # if this value wasn't provided then start with an emtpy selection list.  This list will
        # eventually be returned to the parent via end_dialog.
        selected: [
            str
        ] = step_context.options[0] if step_context.options is not None and step_context.options[0] is not None else []
        step_context.values[self.SYMPTOMS_SELECTED] = selected

        dates: [
            str
        ] = step_context.options[1] if step_context.options is not None and step_context.options[1] is not None else []
        step_context.values[self.SYMPTOMS_DATES] = dates

        if len(selected) == 0:
            message = (
                f"Im Folgenden finden Sie eine Liste relevanter Symptome. Leiden Sie an einem der Symptome? Falls nicht, sagen Sie **{self.DONE_OPTION}**."
            )
        else:
            message = (
                f"Sie leiden an **{selected[len(selected)-1]}**. Leiden Sie an weiteren Symptomen? Falls nicht, sagen Sie **{self.DONE_OPTION}**."
            )

        # create a list of options to choose, with already selected items removed.
        options = self.symptom_options.copy()
        options.append(self.DONE_OPTION)
        if len(selected) > 0:
            options = [item for item in options if item not in selected]

        # prompt with the list of choices
        prompt_options = PromptOptions(
            prompt=MessageFactory.text(message),
            retry_prompt=MessageFactory.text("Bitte nennen Sie eines der relevanten Symptome oder **{self.DONE_OPTION}**."),
            choices=self._to_choices(options),
        )
        return await step_context.prompt(ChoicePrompt.__name__, prompt_options)


    def _to_choices(self, choices: [str]) -> List[Choice]:
        choice_list: List[Choice] = []
        for choice in choices:
            choice_list.append(Choice(value=choice))
        return choice_list

    async def loop_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        selected: List[str] = step_context.values[self.SYMPTOMS_SELECTED]
        dates: List[str] = step_context.values[self.SYMPTOMS_DATES]
        choice: FoundChoice = step_context.result
        done = choice.value == self.DONE_OPTION

        # If they chose a company, add it to the list.
        if not done:
            selected.append(choice.value)
            return await step_context.prompt(
                DateTimePrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(
                        "Seit wann leiden Sie an diesem Symptom? Bitte nennen Sie das Datum im Format TT.MM.JJJJ (z.B. 03.03.2020)."),
                ),
            )

        # If they're done, exit and return their list.
        if done or len(selected) >= len(self.symptom_options):
            print("[DEBUG] Symptoms selection ending now with " + str([selected, dates]))
            return await step_context.end_dialog([selected, dates])


    async def save_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        selected: List[str] = step_context.values[self.SYMPTOMS_SELECTED]
        dates: List[str] = step_context.values[self.SYMPTOMS_DATES]
        choice: FoundChoice = step_context.result
        date = str(choice[0].value)
        dates.append(date)
        return await step_context.replace_dialog(
            SymptomsSelectionDialog.__name__, [selected, dates]
        )

