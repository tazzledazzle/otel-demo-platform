"""Temporal worker with OpenTelemetry tracing."""

import asyncio
import logging

from temporalio.client import Client
from temporalio.contrib.opentelemetry import TracingInterceptor
from temporalio.worker import Worker

from llm_workflow_orchestrator.activities.call_llm import call_llm
from llm_workflow_orchestrator.activities.call_tool import call_tool
from llm_workflow_orchestrator.config import get_temporal_host, get_temporal_task_queue
from llm_workflow_orchestrator.otel_setup import setup_otel
from llm_workflow_orchestrator.workflows.linear_chain import LinearChainWorkflow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_worker() -> None:
    setup_otel()
    host = get_temporal_host()
    task_queue = get_temporal_task_queue()

    client = await Client.connect(
        host,
        interceptors=[TracingInterceptor()],
    )

    worker = Worker(
        client,
        task_queue=task_queue,
        workflows=[LinearChainWorkflow],
        activities=[call_llm, call_tool],
        interceptors=[TracingInterceptor()],
    )

    logger.info("Worker starting on %s task queue %s", host, task_queue)
    await worker.run()


def main() -> None:
    asyncio.run(run_worker())


if __name__ == "__main__":
    main()
