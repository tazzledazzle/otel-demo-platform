package dev.otel.demo.api.routes

import dev.otel.demo.api.TemporalClientFactory
import dev.otel.demo.api.models.ChatRequest
import dev.otel.demo.api.models.ChatResponse
import io.opentelemetry.api.GlobalOpenTelemetry
import io.opentelemetry.api.trace.SpanKind
import io.ktor.server.request.receive
import io.ktor.server.response.respond
import io.ktor.server.routing.Routing
import io.ktor.server.routing.post

fun Routing.chatRoutes() {
    val tracer = GlobalOpenTelemetry.get().getTracer("otel-demo-api", "1.0")
    post("/chat") {
        val ctx = context
        val span = tracer.spanBuilder("POST /chat").setSpanKind(SpanKind.SERVER).startSpan()
        try {
            span.makeCurrent().use {
                val body = runCatching { ctx.receive<ChatRequest>() }.getOrElse { e ->
                    span.recordException(e)
                    throw e
                }
                val client = TemporalClientFactory.create()
                val result = runCatching { client.runAgentWorkflow(body.message) }.getOrElse { e ->
                    span.recordException(e)
                    throw e
                }
                ctx.respond(ChatResponse(result))
            }
        } finally {
            span.end()
        }
    }
}
