package dev.otel.demo.api

import dev.otel.demo.api.plugins.configureRouting
import dev.otel.demo.api.plugins.configureSerialization
import io.ktor.server.application.Application
import io.ktor.server.engine.embeddedServer
import io.ktor.server.netty.Netty
import java.net.BindException
import java.net.ServerSocket

fun main() {
    val otelEndpoint = System.getenv("OTEL_EXPORTER_OTLP_ENDPOINT") ?: "http://localhost:4317"
    initOpenTelemetry("otel-demo-api", otelEndpoint)
    val port = resolvePortWithDiscovery()
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

/**
 * Port resolution:
 * - When API_PORT is set: use it as-is (with a simple parse fallback to 8080).
 * - When API_PORT is unset: try 8080 first, then probe subsequent ports until a free one is found.
 */
private fun resolvePortWithDiscovery(): Int {
    val envPort = System.getenv("API_PORT")
    if (envPort != null) {
        return envPort.toIntOrNull() ?: 8080
    }

    val basePort = 8080
    val maxAttempts = 20

    for (offset in 0 until maxAttempts) {
        val candidate = basePort + offset
        if (isPortAvailable(candidate)) {
            if (candidate != basePort) {
                System.err.println("API_PORT not set and 8080 unavailable; using discovered port $candidate.")
            }
            return candidate
        }
    }

    throw IllegalStateException("Unable to find an available port starting at $basePort (tried $maxAttempts ports).")
}

private fun isPortAvailable(port: Int): Boolean {
    return try {
        ServerSocket(port).use { socket ->
            socket.reuseAddress = true
        }
        true
    } catch (e: Exception) {
        false
    }
}
