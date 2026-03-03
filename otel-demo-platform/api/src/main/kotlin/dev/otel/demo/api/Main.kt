package dev.otel.demo.api

import dev.otel.demo.api.plugins.configureRouting
import dev.otel.demo.api.plugins.configureSerialization
import io.ktor.server.application.Application
import io.ktor.server.engine.embeddedServer
import io.ktor.server.netty.Netty
import java.net.BindException

fun main() {
    val otelEndpoint = System.getenv("OTEL_EXPORTER_OTLP_ENDPOINT") ?: "http://localhost:4317"
    initOpenTelemetry("otel-demo-api", otelEndpoint)
    val port = resolvePort()
    try {
        System.err.println("API starting on http://0.0.0.0:$port (POST /chat, GET /health)")
        embeddedServer(Netty, port = port) {
            configureSerialization()
            configureRouting()
        }.start(wait = true)
    } catch (e: BindException) {
        System.err.println("API could not bind to port $port. Set API_PORT to a different port or stop the other process.")
        throw e
    }
}

/** Port from API_PORT env, or 8080 when unset. Fails fast if 8080 in use when unset. */
private fun resolvePort(): Int {
    val envPort = System.getenv("API_PORT")
    if (envPort != null) return envPort.toIntOrNull() ?: 8080
    return 8080
}
