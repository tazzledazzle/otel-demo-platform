package dev.otel.demo.api.routes

import io.ktor.server.response.respondText
import io.ktor.server.routing.Routing
import io.ktor.server.routing.get

fun Routing.healthRoutes() {
    get("/health") {
        context.respondText("OK")
    }
}
