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
        val ctx = context
        fun chatLog(msg: String) = System.err.println("[chat] $msg")
        chatLog("POST /chat: request received")
        val body = runCatching { ctx.receive<ChatRequest>() }.getOrElse { e ->
            chatLog("POST /chat: failed to parse body - ${e.message}")
            throw e
        }
        chatLog("POST /chat: body received message=${body.message}")
        val client = TemporalClientFactory.create()
        chatLog("POST /chat: calling agent workflow")
        val result = runCatching { client.runAgentWorkflow(body.message) }.getOrElse { e ->
            chatLog("POST /chat: workflow failed - ${e.message}")
            throw e
        }
        chatLog("POST /chat: responding reply length=${result.length}")
        ctx.respond(ChatResponse(result))
    }
}
