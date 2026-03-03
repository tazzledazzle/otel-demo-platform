package dev.otel.demo.api.routes

import dev.otel.demo.api.TemporalClientFactory
import dev.otel.demo.api.models.ChatRequest
import dev.otel.demo.api.models.ChatResponse
import io.opentelemetry.api.GlobalOpenTelemetry
import io.opentelemetry.api.trace.Span
import io.opentelemetry.api.trace.SpanKind
import io.ktor.server.request.receive
import io.ktor.server.response.respond
import io.ktor.server.routing.Routing
import io.ktor.server.routing.post

private fun logStructured(
    service: String,
    traceId: String,
    spanId: String,
    outcome: String,
    workflowId: String? = null,
    taskQueue: String? = null
) {
    val extra = mutableListOf<String>()
    workflowId?.let { extra.add(""""workflow_id":"$it"""") }
    taskQueue?.let { extra.add(""""task_queue":"$it"""") }
    val suffix = if (extra.isEmpty()) "" else "," + extra.joinToString(",")
    System.err.println("""{"service":"$service","trace_id":"$traceId","span_id":"$spanId","outcome":"$outcome"$suffix}""")
}

fun Routing.chatRoutes() {
    val tracer = GlobalOpenTelemetry.get().getTracer("otel-demo-api", "1.0")
    post("/chat") {
        val ctx = context
        val span = tracer.spanBuilder("POST /chat").setSpanKind(SpanKind.SERVER).startSpan()
        span.setAttribute("message.type", "chat")
        try {
            span.makeCurrent().use {
                val sc = Span.current().spanContext
                logStructured("otel-demo-api", sc.traceId, sc.spanId, "start")
                val body = runCatching { ctx.receive<ChatRequest>() }.getOrElse { e ->
                    span.recordException(e)
                    logStructured("otel-demo-api", sc.traceId, sc.spanId, "error")
                    throw e
                }
                val client = TemporalClientFactory.create()
                val result = runCatching { client.runAgentWorkflowDetailed(body.message) }.getOrElse { e ->
                    span.recordException(e)
                    logStructured("otel-demo-api", sc.traceId, sc.spanId, "error")
                    throw e
                }
                span.setAttribute("workflow.id", result.workflowId)
                span.setAttribute("task.queue", result.taskQueue)
                logStructured("otel-demo-api", sc.traceId, sc.spanId, "ok", result.workflowId, result.taskQueue)
                ctx.respond(ChatResponse(result.reply, result.workflowId, result.taskQueue))
            }
        } finally {
            span.end()
        }
    }
}
