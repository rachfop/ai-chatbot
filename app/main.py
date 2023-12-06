import asyncio

from activities.activities import process_and_respond, send_start_message
from temporalio.client import Client
from temporalio.worker import Worker
from workflows.workflows import HandleStartCommand, HandleUserMessage

interrupt_event = asyncio.Event()


async def main() -> None:
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="my-task-queue",
        workflows=[HandleStartCommand, HandleUserMessage],
        activities=[send_start_message, process_and_respond],
    )
    print("Starting worker")
    await worker.run()
    try:
        # Wait indefinitely until the interrupt event is set
        await interrupt_event.wait()
    finally:
        # The worker will be shutdown gracefully due to the async context manager
        print("\nShutting down the worker\n")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\nInterrupt received, shutting down...\n")
        interrupt_event.set()
        loop.run_until_complete(loop.shutdown_asyncgens())
