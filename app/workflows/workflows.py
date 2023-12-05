# workflows.py
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities.activities import BotParams, process_and_respond, send_start_message


@workflow.defn
class HandleStartCommand:
    @workflow.run
    async def run(self, bot_params: BotParams) -> str:
        return await workflow.execute_activity(
            send_start_message,
            bot_params,
            schedule_to_close_timeout=timedelta(seconds=60),
        )


@workflow.defn
class HandleUserMessage:
    @workflow.run
    async def run(self, bot_params: BotParams) -> str:
        return await workflow.execute_activity(
            process_and_respond,
            bot_params,
            schedule_to_close_timeout=timedelta(seconds=60),
        )
