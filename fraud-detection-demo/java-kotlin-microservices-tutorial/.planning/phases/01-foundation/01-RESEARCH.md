# Phase 1: Foundation — Research

**Researched:** 2026-02-25
**Domain:** JVM HTTP microservice (Java/Kotlin), single endpoint, minimal runnable service
**Confidence:** HIGH

## Summary

Phase 1 needs one runnable JVM service with one HTTP endpoint, single-command build/run, no persistence or external calls. The two main options are **Spring Boot** (Java or Kotlin) and **Ktor** (Kotlin). Spring Boot is the dominant choice for JVM microservices: start.spring.io, mature docs, and a single dependency (`spring-boot-starter-web`) plus `./gradlew bootRun` or `./mvnw spring-boot:run`. Ktor is lighter and Kotlin-native, with faster startup and minimal boilerplate; run via `./gradlew run` and either `embeddedServer` (config in code) or EngineMain + `application.conf`. For a tutorial that may add resilience and observability later, Spring Boot’s ecosystem (actuator, resilience4j, etc.) is a strong fit; Ktor fits if the goal is Kotlin-first and minimal surface area.

**Primary recommendation:** Use **Spring Boot 3.x with Gradle** (Java or Kotlin). One endpoint (e.g. `GET /health` or `GET /api/example`), `./gradlew bootRun` to run, success = `curl http://localhost:8080/...` returns a response. If the tutorial is explicitly Kotlin-first and minimal, **Ktor 3.x with Gradle** and `embeddedServer` is a solid alternative.

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions
- One HTTP endpoint (e.g. GET /health or GET /api/example); returns simple response.
- No database or external calls in Phase 1.
- Java or Kotlin (single choice for the tutorial); framework TBD (Spring Boot, Ktor, or other).
- Engineer-oriented: minimal boilerplate, clear project layout.
- Single-command or minimal-step build and run (e.g. `./gradlew run` or `mvn spring-boot:run`).
- Success = learner runs the service and gets a response (e.g. curl or browser).

### Claude's Discretion
- Exact framework and language; endpoint path and response body; build tool (Maven vs Gradle).

### Deferred Ideas (OUT OF SCOPE)
- Persistence, resilience, observability, multi-service — later phases.

</user_constraints>

## Standard Stack

### Option A: Spring Boot (recommended for broad tutorial)

| Library / tool | Version | Purpose | Why standard |
|----------------|---------|---------|--------------|
| Spring Boot | 3.2.x or 3.3.x | Web app + embedded server | De facto JVM microservice framework; start.spring.io, strong docs |
| spring-boot-starter-web | (via BOM) | HTTP, Tomcat, Jackson | Single dependency for REST |
| Java | 17+ | Language (or Kotlin 1.9+) | Spring Boot 3 requirement |
| Gradle | 8.x | Build | Single command: `./gradlew bootRun`; wrapper in repo |

**Run:** `./gradlew bootRun` or `./gradlew build && java -jar build/libs/<name>.jar`  
**Maven alternative:** `./mvnw spring-boot:run` or `./mvnw clean package && java -jar target/<name>.jar`

### Option B: Ktor (Kotlin-first, minimal)

| Library / tool | Version | Purpose | Why standard |
|----------------|---------|---------|--------------|
| Ktor server-core | 3.x | HTTP routing, engine abstraction | Official Kotlin HTTP toolkit |
| Ktor server-netty | 3.x | Netty engine | Default engine in Ktor docs |
| Kotlin | 2.0+ | Language | Ktor 3 targets Kotlin 2 |
| Gradle | 8.x | Build | `./gradlew run`; Application plugin |

**Run:** `./gradlew run` (requires `application { mainClass.set("...") }` or EngineMain).

### Build tool choice
- **Gradle** recommended for both: wrapper ensures one-command run without pre-installed Maven/Gradle; Kotlin DSL optional for Ktor.
- Maven: use `./mvnw` and `spring-boot-maven-plugin` (Spring) or exec-maven-plugin / ktor setup (Ktor).

### Alternatives considered

| Instead of | Could use | Tradeoff |
|------------|-----------|----------|
| Spring Boot | Ktor | Ktor: lighter, Kotlin-native; Spring: ecosystem, Java/Kotlin, more “enterprise” patterns |
| Spring Boot | Micronaut / Quarkus | Smaller ecosystem for a tutorial; Spring has more guides and jobs |
| Gradle | Maven | Both fine; Gradle wrapper + single `run` task is very clear for learners |

**Installation (Spring Boot, Gradle):** Use [start.spring.io](https://start.spring.io): Java or Kotlin, Gradle, Jar, Spring Web, generate then unzip. No manual `install` step.

**Installation (Ktor):** Use [start.ktor.io](https://start.ktor.io) or Ktor CLI (`ktor new`); or add `io.ktor:ktor-server-*` to `build.gradle.kts` and Application plugin.

## Architecture Patterns

### Recommended project structure (Spring Boot)

```
<project>/
├── build.gradle[.kts]
├── settings.gradle[.kts]
├── gradlew, gradlew.bat
├── gradle/
└── src/
    └── main/
        ├── java/   (or kotlin/)
        │   └── com/example/<app>/
        │       ├── <App>Application.java   # @SpringBootApplication + main
        │       └── (controller package/)
        │           └── HealthController.java
        └── resources/
            └── application.properties   # optional: server.port=8080
```

- Root package must be **named** (e.g. `com.example.demo`). Do not use the default package.
- Main class in root package; controllers in same package or subpackages so component scan finds them.

### Recommended project structure (Ktor, minimal)

```
<project>/
├── build.gradle.kts
├── settings.gradle.kts
├── gradlew, gradlew.bat
├── gradle/
└── src/
    └── main/
        ├── kotlin/
        │   └── com/example/<app>/
        │       └── Application.kt   # main() + embeddedServer + routing
        └── resources/
            # optional: application.conf if using EngineMain
```

- For Phase 1 minimal, **config in code** with `embeddedServer` avoids `application.conf` and module wiring.

### Pattern 1: Spring Boot — one GET endpoint

**What:** Single REST controller, GET returns body (string or JSON).  
**When:** Phase 1 single endpoint.

**Example (Java):**

```java
// Source: https://spring.io/guides/gs/rest-service/
package com.example.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController {

  @GetMapping("/health")
  public String health() {
    return "OK";
  }
}
```

**Example (Kotlin):**

```kotlin
@RestController
class HealthController {

  @GetMapping("/health")
  fun health(): String = "OK"
}
```

Main class: `@SpringBootApplication` and `SpringApplication.run(...)` or `runApplication<RestServiceApplication>(*args)`.

### Pattern 2: Ktor — one GET endpoint (config in code)

**What:** `embeddedServer(Netty, port = 8080) { routing { get("/health") { ... } } }.start(wait = true)`.  
**When:** Phase 1 with Ktor, no external config file.

**Example:**

```kotlin
// Source: https://ktor.io/docs/server-configuration-code.html, https://ktor.io/docs/server-create-a-new-project.html
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.ktor.server.response.*
import io.ktor.server.routing.*

fun main() {
  embeddedServer(Netty, port = 8080, host = "0.0.0.0") {
    routing {
      get("/health") {
        call.respondText("OK")
      }
    }
  }.start(wait = true)
}
```

### Anti-patterns to avoid
- **Default package (Spring):** Do not put `@SpringBootApplication` or controllers in the default package; component scan can hit every JAR and cause slow startup or odd beans. Use a root package (e.g. `com.example.demo`).
- **Ktor EngineMain without application.conf:** If using EngineMain, `application.conf` must exist in `src/main/resources` and list the module (e.g. `modules = [ com.example.ApplicationKt.module ]`). For Phase 1, prefer `embeddedServer` to avoid this.
- **Hand-rolling HTTP or JSON:** Use the framework’s HTTP and serialization; do not implement a raw server or manual JSON for this phase.

## Don't Hand-Roll

| Problem | Don't build | Use instead | Why |
|---------|-------------|-------------|-----|
| HTTP server | Raw ServerSocket / Netty pipeline | Spring Boot or Ktor | Port, threading, request parsing, lifecycle |
| JSON serialization | Manual string concat / parser | Jackson (Spring) or ktor-serialization (Ktor) | Encoding, dates, nulls, content-type |
| Build / run | Custom scripts or “install JAR manually” | Gradle/Maven wrapper + `bootRun` / `run` | Reproducible, single command |

**Key insight:** A single HTTP endpoint still needs a servlet/engine, port binding, and request/response handling. Frameworks provide this; hand-rolling is out of scope for Phase 1.

## Common Pitfalls

### Pitfall 1: Spring Boot — default package
**What goes wrong:** Slow startup, unwanted beans, or BeanDefinitionStoreException.  
**Why:** Component scan has no base package and scans the whole classpath.  
**How to avoid:** Put main and all components under a named root package (e.g. `com.example.demo`).  
**Warning signs:** No `package` declaration; main class in `src/main/java/Main.java` with no package folder.

### Pitfall 2: Ktor — EngineMain module not found
**What goes wrong:** Runtime error that the configured module (e.g. `ApplicationKt.module`) is not found.  
**Why:** `application.conf` lists a fully qualified name that doesn’t match the actual `fun Application.module()` (Kotlin exposes it as `ApplicationKt.module` from file `Application.kt`).  
**How to avoid:** Use `embeddedServer` for Phase 1; or ensure `application.conf` `modules` entry matches the file and package (e.g. `com.example.ktor.ApplicationKt.module`).  
**Warning signs:** Using EngineMain and no or wrong `application.conf` in `src/main/resources`.

### Pitfall 3: Port already in use
**What goes wrong:** BindException: Address already in use.  
**Why:** Another process (or previous run) on 8080.  
**How to avoid:** Change port in `application.properties` (Spring: `server.port=8081`) or in code (Ktor: `port = 8081`), or stop the other process.  
**Warning signs:** Run fails immediately with “port” or “bind” in the message.

### Pitfall 4: Gradle wrapper not executable
**What goes wrong:** `Permission denied` on `./gradlew`.  
**How to avoid:** `chmod +x gradlew` (or commit wrapper with +x).  
**Warning signs:** Learner on macOS/Linux runs `./gradlew run` and gets permission error.

## Code Examples

### Spring Boot: minimal build.gradle (Groovy)

```groovy
plugins {
  id 'java'
  id 'org.springframework.boot' version '3.2.x'
  id 'io.spring.dependency-management' version '1.1.4'
}
group = 'com.example'
version = '0.0.1-SNAPSHOT'
java { sourceCompatibility = '17' }
repositories { mavenCentral() }
dependencies {
  implementation 'org.springframework.boot:spring-boot-starter-web'
}
```

(Use Spring Boot Gradle plugin’s version from current docs; 3.2.x/3.3.x both valid.)

### Spring Boot: run commands

```bash
./gradlew bootRun
# or
./gradlew build && java -jar build/libs/<artifact>-<version>.jar
```

### Ktor: minimal build.gradle.kts (excerpt)

```kotlin
plugins {
  application
  kotlin("jvm") version "2.0.x"
}
application { mainClass.set("com.example.ktor.ApplicationKt") }
repositories { mavenCentral() }
dependencies {
  implementation("io.ktor:ktor-server-core:3.x.x")
  implementation("io.ktor:ktor-server-netty:3.x.x")
}
```

(Exact Ktor 3.x version from [Ktor docs](https://ktor.io/docs/gradle.html) or start.ktor.io.)

### Ktor: run command

```bash
./gradlew run
```

### Verification (both)

```bash
curl -s http://localhost:8080/health
# expect: OK (or chosen response)
```

## State of the Art

| Old approach | Current approach | When / impact |
|--------------|------------------|----------------|
| Spring Boot 2.x, Java 8/11 | Spring Boot 3.x, Java 17+ | SB 3 requires Jakarta namespace, Java 17+ |
| Ktor 2.x | Ktor 3.x | 3.x is current; check docs for engine/API tweaks |
| Manual Gradle/Maven install | Wrapper (gradlew/mvnw) in repo | Single-command run without global install |

**Deprecated / avoid:** Spring Boot 2.x for new tutorials (move to 3.x). Putting application class in default package.

## Open Questions

1. **Java vs Kotlin for the tutorial**  
   - Known: Both work with Spring Boot; Ktor is Kotlin-only.  
   - Unclear: Audience preference.  
   - Recommendation: Spring Boot + Java keeps the door open for Kotlin in a later phase; Spring Boot + Kotlin or Ktor + Kotlin if the tutorial is Kotlin-first.

2. **Exact endpoint path and body**  
   - Known: One GET endpoint; simple response.  
   - Unclear: Naming convention.  
   - Recommendation: `GET /health` returning `OK` or `{"status":"UP"}` is widely recognized; `GET /api/example` with a short JSON body is also fine. Planner can pick one and document it.

## Sources

### Primary (HIGH confidence)
- Spring official: [Building a RESTful Web Service](https://spring.io/guides/gs/rest-service/) — controller, main, Gradle/Maven run.
- Spring Boot: [Getting Started](https://docs.spring.io/spring-boot/docs/current/reference/html/getting-started.html) (reference).
- Ktor: [Create, open and run a new Ktor project](https://ktor.io/docs/server-create-a-new-project.html) — project layout, `./gradlew build` / `./gradlew run`, default port 8080.
- Ktor: [Configuration in code](https://ktor.io/docs/server-configuration-code.html) — `embeddedServer(Netty, port = 8080) { routing { get("/") { call.respondText("Hello, world!") } } }.start(wait = true)`.
- Ktor: [Configuration in a file](https://ktor.io/docs/server-configuration-file.html) — `application.conf` in resources, `ktor.application.modules`.

### Secondary (MEDIUM confidence)
- Spring Boot structuring: [Structuring Your Code](https://docs.spring.io/spring-boot/docs/current/reference/html/using.html#using.structuring-your-code) (root package, avoid default package).
- Web search: Spring Boot 3 minimal HTTP + Gradle; Ktor minimal GET + Gradle; Spring Boot vs Ktor 2024; default package pitfalls; Ktor application.conf modules — cross-checked with official docs.

### Tertiary (LOW confidence)
- Web search: “Spring Boot 3.4 / 3.3 latest” and “Ktor 3.4” version hits (version numbers change; planner should take current from start.spring.io / start.ktor.io or official dependency lists).

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — official guides and docs for both stacks; versions from official sites.
- Architecture: HIGH — standard layout and run commands documented.
- Pitfalls: HIGH — default package and EngineMain/config are documented; port and gradlew are common knowledge.

**Research date:** 2026-02-25  
**Valid until:** ~30 days (stable stacks); re-check exact plugin/dependency versions when implementing.

---

## RESEARCH COMPLETE
