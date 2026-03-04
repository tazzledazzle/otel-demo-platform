package dev.otel.demo.api.routes

import io.ktor.client.request.get
import io.ktor.client.statement.bodyAsText
import io.ktor.serialization.jackson.jackson
import io.ktor.server.testing.testApplication
import io.ktor.server.application.install
import io.ktor.server.plugins.contentnegotiation.ContentNegotiation
import io.ktor.server.routing.routing
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Test

class HealthRoutesTest {
    @Test
    fun `GET health returns OK`() = testApplication {
        application {
            install(ContentNegotiation) {
                jackson()
            }
            routing {
                healthRoutes()
            }
        }
        val response = client.get("/health")
        assertEquals("OK", response.bodyAsText())
    }
}
