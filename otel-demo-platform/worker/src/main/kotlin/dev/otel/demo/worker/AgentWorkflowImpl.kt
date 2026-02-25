package dev.otel.demo.worker

import dev.otel.demo.contracts.AgentWorkflow
import io.temporal.activity.ActivityOptions
import io.temporal.workflow.Workflow
import java.time.Duration

class AgentWorkflowImpl : AgentWorkflow {
    override fun run(message: String): String {
        val options = ActivityOptions.newBuilder()
            .setStartToCloseTimeout(Duration.ofMinutes(2))
            .build()
        val activity = Workflow.newActivityStub(RunAgentActivityInterface::class.java, options)
        return activity.run(message)
    }
}
