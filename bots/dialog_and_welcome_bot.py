# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from botbuilder.core import (
    ConversationState,
    MessageFactory,
    UserState,
    TurnContext,
)
from botbuilder.dialogs import Dialog
from botbuilder.schema import ChannelAccount

from .dialog_bot import DialogBot


class DialogAndWelcomeBot(DialogBot):
    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
    ):
        super(DialogAndWelcomeBot, self).__init__(
            conversation_state, user_state, dialog
        )

    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            # Greet anyone that was not the target (recipient) of this message.
            if member.id != turn_context.activity.recipient.id:
                turn_context.activity.locale = "de"
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Hallo, ich bin **Corobot**. Lassen Sie uns herausfinden, wie Sie mit COVID-19 umgehen sollten. Sind Sie soweit? "
                    )
                )
