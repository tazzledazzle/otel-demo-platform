"""Linear chain workflow: one or more LLM steps in sequence."""

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from llm_workflow_orchestrator.activities.call_llm import call_llm
    from llm_workflow_orchestrator.activities.call_tool import call_tool


@workflow.defn
class LinearChainWorkflow:
    """Run a single LLM call and return the content. Extensible to multiple steps."""

    @workflow.run
    async def run(self, prompt: str) -> str:
        result = await workflow.execute_activity(
            call_llm,
            args=[prompt],
            start_to_close_timeout=60,
        )
        content = result.get("content") or ""
        return content
