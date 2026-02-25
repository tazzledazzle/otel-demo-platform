package dev.otel.demo.api.routes

import dev.otel.demo.api.TemporalClientFactory
import dev.otel.demo.api.models.ChatRequest
import dev.otel.demo.api.models.ChatResponse
import io.ktor.server.request.receive
import io.ktor.server.response.respond
import io.ktor.server.routing.Routing
import io.ktor.server.routing.post

fun Routing.chatRoutes() {
    post("/chat") {
        val body = context.receive<ChatRequest>()
        val client = TemporalClientFactory.create()
        val result = client.runAgentWorkflow(body.message)
        context.respond(ChatResponse(result))
    }
}
