package dev.otel.demo.api

import dev.otel.demo.api.plugins.configureRouting
import dev.otel.demo.api.plugins.configureSerialization
import io.ktor.server.application.Application
import io.ktor.server.engine.embeddedServer
import io.ktor.server.netty.Netty
import com.fasterxml.jackson.databind.ObjectMapper
import java.net.BindException
import java.net.InetAddress
import java.net.ServerSocket
import java.nio.file.Files
import java.nio.file.Paths
import java.nio.file.StandardOpenOption

private val debugMapper = ObjectMapper()
private const val DEBUG_LOG_PATH = "/Users/terenceschumacher/dev/.cursor/debug-591c58.log"
private fun debugLog(location: String, message: String, data: Map<String, Any?>, hypothesisId: String, runId: String? = null) {
    try {
        val payload = mutableMapOf<String, Any?>(
            "sessionId" to "591c58", "location" to location, "message" to message,
            "data" to data, "hypothesisId" to hypothesisId, "timestamp" to System.currentTimeMillis()
        )
        runId?.let { payload["runId"] = it }
        val path = Paths.get(DEBUG_LOG_PATH)
        Files.createDirectories(path.parent)
        Files.write(path, listOf(debugMapper.writeValueAsString(payload)), StandardOpenOption.CREATE, StandardOpenOption.APPEND)
    } catch (e: Exception) {
        System.err.println("DEBUG_LOG write failed: ${e.message}")
    }
}

fun main() {
    // #region agent log
    debugLog("Main.kt:main", "main entered", mapOf(), "H0")
    // #endregion
    val otelEndpoint = System.getenv("OTEL_EXPORTER_OTLP_ENDPOINT") ?: "http://localhost:4317"
    initOpenTelemetry("otel-demo-api", otelEndpoint)
    val port = resolvePort()
    // #region agent log
    debugLog("Main.kt:main", "port resolved", mapOf("port" to port, "API_PORT_env" to (System.getenv("API_PORT") ?: "__unset__")), "H1")
    debugLog("Main.kt:main", "about to start server", mapOf("port" to port), "H2")
    // #endregion
    try {
        embeddedServer(Netty, port = port) {
            configureSerialization()
            configureRouting()
        }.start(wait = true)
    } catch (e: BindException) {
        // #region agent log
        debugLog("Main.kt:main", "bind failed", mapOf("port" to port, "message" to (e.message)), "H3")
        // #endregion
        throw e
    }
}

/** Port from API_PORT env, or first available in 8080..8089 when unset (avoids BindException). */
private fun resolvePort(): Int {
    val envPort = System.getenv("API_PORT")
    if (envPort != null) return envPort.toIntOrNull() ?: 8080
    for (p in 8080..8089) {
        val available = portAvailable(p)
        // #region agent log
        debugLog("Main.kt:resolvePort", "port check", mapOf("port" to p, "available" to available), "H1")
        // #endregion
        if (available) return p
    }
    return 8080
}

/** Bind to 0.0.0.0 to match Ktor Netty default and avoid IPv4/IPv6 mismatch. */
private fun portAvailable(port: Int): Boolean =
    try {
        ServerSocket(port, 0, InetAddress.getByName("0.0.0.0")).close()
        true
    } catch (_: Exception) {
        false
    }
