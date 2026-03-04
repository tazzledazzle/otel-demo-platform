package dev.otel.demo.worker

import dev.otel.demo.worker.client.agentInvoke

class RunAgentActivity(
    private val agentBaseUrl: String
) : RunAgentActivityInterface {
    override fun run(message: String): String {
        return agentInvoke(agentBaseUrl, message)
    }
}
