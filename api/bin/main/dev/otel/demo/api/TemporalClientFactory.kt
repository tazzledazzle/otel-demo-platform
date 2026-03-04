package dev.otel.demo.api

import dev.otel.demo.contracts.AgentWorkflow
import io.temporal.client.WorkflowClient
import io.temporal.client.WorkflowClientOptions
import io.temporal.client.WorkflowOptions
import io.temporal.serviceclient.WorkflowServiceStubs
import io.temporal.serviceclient.WorkflowServiceStubsOptions

object TemporalClientFactory {
    private const val TASK_QUEUE = "agent-task-queue"

    fun create(): AgentWorkflowClient {
        val endpoint = System.getenv("TEMPORAL_ADDRESS") ?: "localhost:7233"
        val service = WorkflowServiceStubs.newServiceStubs(
            WorkflowServiceStubsOptions.newBuilder().setTarget(endpoint).build()
        )
        val client = WorkflowClient.newInstance(
            service,
            WorkflowClientOptions.newBuilder().build()
        )
        return AgentWorkflowClient(client)
    }
}

class AgentWorkflowClient(private val client: WorkflowClient) {
    private val taskQueue = System.getenv("TEMPORAL_TASK_QUEUE") ?: "agent-task-queue"

    fun runAgentWorkflow(message: String): String {
        val workflow = client.newWorkflowStub(
            AgentWorkflow::class.java,
            WorkflowOptions.newBuilder()
                .setTaskQueue(taskQueue)
                .setWorkflowId("agent-${System.currentTimeMillis()}")
                .build()
        )
        return workflow.run(message)
    }
}
