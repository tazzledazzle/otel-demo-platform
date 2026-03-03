package dev.otel.demo.worker.client

import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.engine.cio.CIO
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.request.post
import io.ktor.client.request.setBody
import io.ktor.http.ContentType
import io.ktor.http.contentType
import io.ktor.serialization.jackson.jackson
import kotlinx.coroutines.runBlocking

private val client = HttpClient(CIO) {
    install(ContentNegotiation) {
        jackson()
    }
}

fun agentInvoke(baseUrl: String, message: String): String = runBlocking {
    val url = baseUrl.trimEnd('/') + "/invoke"
    val body = mapOf("message" to message)
    val response: InvokeResponse = client.post(url) {
        contentType(ContentType.Application.Json)
        setBody(body)
    }.body()
    response.reply
}

private data class InvokeResponse(val reply: String)
