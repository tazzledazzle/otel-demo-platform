package dev.otel.demo.worker

import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test

class RunAgentActivityTest {
    @Test
    fun `RunAgentActivity has run method`() {
        val activity = RunAgentActivity("http://localhost:8000")
        assertTrue(RunAgentActivityInterface::class.java.isInstance(activity))
    }
}
