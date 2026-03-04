package dev.otel.demo.api.models

data class ChatRequest(val message: String)

data class ChatResponse(val reply: String)
