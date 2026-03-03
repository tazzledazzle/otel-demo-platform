"""Start a LinearChainWorkflow run (CLI)."""

import asyncio
import logging
import sys
import time

from temporalio.client import Client
from temporalio.contrib.opentelemetry import TracingInterceptor

from llm_workflow_orchestrator.config import get_temporal_host, get_temporal_task_queue
from llm_workflow_orchestrator.otel_setup import setup_otel
from llm_workflow_orchestrator.workflows.linear_chain import LinearChainWorkflow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_starter(prompt: str) -> str:
    """Start a LinearChainWorkflow and return the result."""
    setup_otel(service_name="llm-workflow-starter")
    host = get_temporal_host()
    task_queue = get_temporal_task_queue()

    client = await Client.connect(
        host,
        interceptors=[TracingInterceptor()],
    )

    workflow_id = f"linear-chain-{int(time.time() * 1000)}"
    handle = await client.start_workflow(
        LinearChainWorkflow.run,
        prompt,
        id=workflow_id,
        task_queue=task_queue,
    )
    logger.info("Started workflow id=%s", workflow_id)
    result = await handle.result()
    return result


def main() -> None:
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Say hello in one sentence."
    result = asyncio.run(run_starter(prompt))
    print(result)


if __name__ == "__main__":
    main()
