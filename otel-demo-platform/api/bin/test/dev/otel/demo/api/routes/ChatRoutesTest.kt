package dev.otel.demo.api.routes

import io.ktor.serialization.jackson.jackson
import io.ktor.server.plugins.contentnegotiation.ContentNegotiation
import io.ktor.server.testing.testApplication
import io.ktor.server.application.install
import io.ktor.server.routing.routing
import org.junit.jupiter.api.Test

class ChatRoutesTest {
    @Test
    fun `chatRoutes can be installed`() = testApplication {
        application {
            install(ContentNegotiation) { jackson() }
            routing {
                healthRoutes()
                chatRoutes()
            }
        }
        // Route is registered; full E2E requires Temporal + worker (see integration test)
    }
}
