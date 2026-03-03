# Phase 1: Foundation — Research

**Researched:** 2026-02-25
**Domain:** REST and GraphQL API implementation (minimal first endpoint; framework/language choice)
**Confidence:** HIGH

## Summary

Phase 1 requires one runnable API (REST or GraphQL, single choice), minimal schema, one or two operations, single-command run, and no auth/versioning. Research compared REST (FastAPI, Express, Spring Boot) and GraphQL (Apollo Server, graphql-js + graphql-http) for minimal first-endpoint tutorials.

**REST:** FastAPI gives the shortest path: one file, one command (`fastapi dev main.py`), automatic OpenAPI docs at `/docs`, and JSON by default. Express is one file + `node app.js` but no built-in docs or validation. Spring Boot requires project setup (Initializr, multiple files, Gradle/Maven) and has the most concepts (controllers, beans, build).

**GraphQL:** Apollo Server 4 with `startStandaloneServer` is the minimal path: schema + resolvers in one file, `npm start`, Apollo Sandbox at the server URL. The official GraphQL.org stack is graphql-js + graphql-http (Express); express-graphql is deprecated (archived 2023)—use graphql-http.

**Primary recommendation:** Use **REST with FastAPI** for Phase 1: one Python file, one command, learner hits the root or `/docs`, sees JSON response and interactive docs. If the tutorial should introduce GraphQL first, use **Apollo Server** with `startStandaloneServer` (Node, one entry file, `npm start`, Sandbox for queries).

## User Constraints (from CONTEXT.md)

### Locked Decisions
- Either REST or GraphQL for Phase 1 (not both); one or two operations (e.g. GET resource, or query + mutation).
- Single-command or minimal-step run; learner can call the API (curl, browser, or simple client) and see a response.
- Success = request in, response back; no auth or versioning in Phase 1.
- Code-first; minimal theory. Prerequisites and project layout clear.

### Claude's Discretion
- REST vs GraphQL; framework and language; example resource/query shape.

### Deferred Ideas (OUT OF SCOPE)
- The other API style (GraphQL if REST first, or vice versa), auth, versioning — later phases.

---

## Standard Stack

### REST options (pick one for Phase 1)

| Stack        | Version / runtime | Purpose              | Why use in Phase 1                         |
|-------------|-------------------|----------------------|--------------------------------------------|
| FastAPI     | 0.115+ (Python 3.10+) | Minimal REST API     | One file, one command, /docs, type hints   |
| Express     | 4.x (Node 18+)    | Minimal REST API     | One file, `node app.js`; JS ecosystem      |
| Spring Boot | 3.x (Java 17+)    | REST controller      | When JVM/Java is required; more setup      |

### GraphQL options (pick one for Phase 1)

| Stack              | Version      | Purpose              | Why use in Phase 1                    |
|--------------------|-------------|----------------------|---------------------------------------|
| Apollo Server      | 4.x         | GraphQL server       | Standalone server, Sandbox, one file  |
| graphql-js + graphql-http | graphql 16+, graphql-http 1.x | GraphQL over HTTP with Express | Official GraphQL.org stack; use instead of deprecated express-graphql |

### Single-command run (per stack)

| Choice        | Run command              | Test (browser/curl)                    |
|---------------|--------------------------|----------------------------------------|
| FastAPI       | `fastapi dev main.py`    | http://127.0.0.1:8000 or /docs         |
| Express       | `node app.js` or `npm start` | http://localhost:3000                  |
| Spring Boot   | `./gradlew bootRun` or `./mvnw spring-boot:run` | http://localhost:8080/greeting         |
| Apollo Server | `npm start`              | http://localhost:4000 (Sandbox)         |
| graphql-http  | `node server.js`         | http://localhost:4000/graphql (POST) or add ruru for IDE |

**Installation (examples):**
```bash
# REST - FastAPI
pip install "fastapi[standard]"

# REST - Express
npm init -y && npm install express

# GraphQL - Apollo Server
npm init -y && npm pkg set type="module" && npm install @apollo/server graphql

# GraphQL - graphql-http + Express
npm install express graphql-http graphql
```

## Architecture Patterns

### Recommended project structure (minimal Phase 1)

**REST (FastAPI):**
```
/
├── main.py          # app, single GET (and optional second op)
├── requirements.txt or pyproject.toml
└── README.md        # run command, how to call API
```

**REST (Express):**
```
/
├── app.js or index.js
├── package.json     # "start": "node app.js"
└── README.md
```

**GraphQL (Apollo):**
```
/
├── index.js (or src/index.js)   # typeDefs, resolvers, startStandaloneServer
├── package.json                 # "type": "module", "start": "node index.js"
└── README.md
```

**GraphQL (graphql-http):**
```
/
├── server.js        # buildSchema, createHandler, express, ruru optional
├── package.json
└── README.md
```

### Pattern: One GET (REST)

**FastAPI** — return dict for JSON; path operation per method/path:
```python
# Source: https://fastapi.tiangolo.com/tutorial/first-steps/
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

**Express** — use `res.json()` for REST JSON (explicit Content-Type and edge cases):
```javascript
// Source: https://expressjs.com/en/starter/hello-world.html (adapted for JSON)
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.json({ message: 'Hello World' });
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
```

**Spring Boot** — controller returns domain object; Jackson serializes to JSON:
```java
// Source: https://spring.io/guides/gs/rest-service/
@RestController
public class GreetingController {
  @GetMapping("/greeting")
  public Greeting greeting(@RequestParam(defaultValue = "World") String name) {
    return new Greeting(counter.incrementAndGet(), template.formatted(name));
  }
}
```

### Pattern: One query (GraphQL)

**Apollo Server** — schema string + resolvers object + startStandaloneServer:
```javascript
// Source: https://www.apollographql.com/docs/apollo-server/getting-started
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

const typeDefs = `#graphql
  type Query { hello: String }
`;
const resolvers = { Query: { hello: () => 'Hello world!' } };

const server = new ApolloServer({ typeDefs, resolvers });
const { url } = await startStandaloneServer(server, { listen: { port: 4000 } });
console.log(`Server ready at ${url}`);
```

**graphql-js + graphql-http (Express)** — buildSchema + root + createHandler:
```javascript
// Source: https://graphql.org/graphql-js/running-an-express-graphql-server
import { buildSchema } from 'graphql';
import { createHandler } from 'graphql-http/lib/use/express';
import express from 'express';

const schema = buildSchema(`type Query { hello: String }`);
const root = { hello: () => 'Hello world!' };
const app = express();
app.all('/graphql', createHandler({ schema, rootValue: root }));
app.listen(4000);
```

### Anti-patterns to avoid
- **Hand-rolling an HTTP server** — use the framework’s run command (FastAPI/uvicorn, Express listen, Spring Boot main, Apollo startStandaloneServer).
- **Using express-graphql** — deprecated/archived; use graphql-http with Express.
- **REST in Express with res.send(object)** for APIs — prefer `res.json()` for explicit JSON and edge cases.
- **Multiple frameworks in Phase 1** — pick one API style and one stack per phase.

## Don't Hand-Roll

| Problem              | Don't build              | Use instead              | Why                          |
|----------------------|--------------------------|---------------------------|------------------------------|
| HTTP server          | Raw Node http.createServer / Java ServerSocket | Framework (Express, FastAPI, Spring, Apollo) | Port, parsing, threading     |
| Request validation   | Manual query/body checks | Framework (FastAPI types, Express middleware, Spring @Valid) | Edge cases, security         |
| OpenAPI schema       | Hand-written YAML/JSON   | FastAPI automatic /docs   | Drift, effort                |
| GraphQL execution    | Custom parser/executor   | graphql-js (via Apollo or graphql-http) | Spec compliance, safety       |

**Key insight:** All stacks provide a single-command run and a minimal one- or two-operation example; avoid custom servers or manual schema/validation for Phase 1.

## Common Pitfalls

### Pitfall 1: Choosing Spring Boot for “quickest” Phase 1
**What goes wrong:** More files (main class, controller, model, build config), build tool, and concepts (DI, component scan).
**Why:** Spring is optimized for larger apps; minimal REST is still more setup than FastAPI or Express.
**How to avoid:** Use Spring only if the tutorial targets JVM/Java; otherwise prefer FastAPI or Express for Phase 1.
**Warning signs:** Need to explain Initializr, Gradle/Maven, or package structure before the first response.

### Pitfall 2: Using express-graphql for GraphQL
**What goes wrong:** Deprecated package, archived repo (March 2023); docs and ecosystem moved to graphql-http.
**Why:** GraphQL Foundation adopted graphql-http as the reference GraphQL-over-HTTP implementation.
**How to avoid:** Use `graphql-http` with Express, or Apollo Server (which handles HTTP itself).
**Warning signs:** Tutorial or sample code importing `express-graphql`.

### Pitfall 3: No way for learner to “see” the response
**What goes wrong:** GraphQL is POST-only; visiting /graphql in browser may show “Method Not Allowed” or empty page.
**Why:** Browsers do GET by default; GraphQL queries are sent in POST body.
**How to avoid:** Provide a one-line “how to run and test”: for REST, curl or browser GET; for GraphQL, document Apollo Sandbox (Apollo) or add ruru/GraphiQL (graphql-http) so the learner can run a query in the browser.
**Warning signs:** README only says “run the server” without a concrete request example or Sandbox URL.

### Pitfall 4: Two operations without a second path or mutation
**What goes wrong:** Phase says “one or two operations” but only one is implemented, or the second is unclear.
**How to avoid:** If two ops: REST = e.g. GET / and GET /items (or GET /greeting); GraphQL = one query + one mutation (or two queries), each with a resolver. Document both in the phase deliverable.
**Warning signs:** Only one route or one query and no mention of the second.

## Code Examples

Verified patterns from official sources:

### REST — FastAPI minimal (official)
```python
# Source: https://fastapi.tiangolo.com/tutorial/first-steps/
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```
Run: `fastapi dev main.py` → http://127.0.0.1:8000 and http://127.0.0.1:8000/docs

### REST — Express minimal (official)
```javascript
// Source: https://expressjs.com/en/starter/hello-world.html
const express = require('express');
const app = express();
const port = 3000;
app.get('/', (req, res) => { res.send('Hello World!'); });
app.listen(port, () => { console.log(`Example app listening on port ${port}`); });
```
Run: `node app.js` → http://localhost:3000. For JSON API use `res.json({ message: 'Hello World' })`.

### REST — Spring Boot greeting (official)
```java
// Source: https://spring.io/guides/gs/rest-service/
@RestController
public class GreetingController {
  private static final String template = "Hello, %s!";
  private final AtomicLong counter = new AtomicLong();

  @GetMapping("/greeting")
  public Greeting greeting(@RequestParam(defaultValue = "World") String name) {
    return new Greeting(counter.incrementAndGet(), template.formatted(name));
  }
}
```
Run: `./gradlew bootRun` or `./mvnw spring-boot:run` → http://localhost:8080/greeting

### GraphQL — Apollo Server minimal (official)
```javascript
// Source: https://www.apollographql.com/docs/apollo-server/getting-started
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

const typeDefs = `#graphql
  type Query { books: [Book] }
  type Book { title: String; author: String }
`;
const books = [{ title: 'The Awakening', author: 'Kate Chopin' }];
const resolvers = { Query: { books: () => books } };

const server = new ApolloServer({ typeDefs, resolvers });
const { url } = await startStandaloneServer(server, { listen: { port: 4000 } });
console.log(`Server ready at ${url}`);
```
Run: `npm start` → open URL in browser for Apollo Sandbox; run query `{ books { title author } }`.

### GraphQL — graphql-http + Express (official)
```javascript
// Source: https://graphql.org/graphql-js/running-an-express-graphql-server
import { buildSchema } from 'graphql';
import { createHandler } from 'graphql-http/lib/use/express';
import express from 'express';

const schema = buildSchema(`type Query { hello: String }`);
const root = { hello: () => 'Hello world!' };
const app = express();
app.all('/graphql', createHandler({ schema, rootValue: root }));
app.listen(4000);
```
Run: `node server.js`. Add ruru for browser IDE: `npm install ruru` and serve `ruruHTML({ endpoint: '/graphql' })` at GET `/`.

## State of the Art

| Old approach     | Current approach        | When changed | Impact                          |
|------------------|--------------------------|-------------|----------------------------------|
| express-graphql  | graphql-http (+ Express) | 2022–2023   | Use graphql-http; express-graphql archived |
| Manual OpenAPI   | FastAPI auto /docs       | N/A         | No hand-written OpenAPI for FastAPI |
| Apollo 3         | Apollo Server 4          | 2022        | Standalone server, framework integrations |
| Callback-only Express | async/await in Node    | Node 8+     | Can use async route handlers    |

**Deprecated/outdated:**
- **express-graphql:** Deprecated; repository archived March 2023. Use graphql-http with Express.

## Open Questions

1. **REST vs GraphQL for Phase 1**
   - Known: Both are viable; FastAPI (REST) has fewest steps; Apollo (GraphQL) has Sandbox and one-file setup.
   - Unclear: Whether the tutorial’s narrative prefers “REST first” or “GraphQL first.”
   - Recommendation: Default to **REST with FastAPI** for Phase 1 unless CONTEXT or PRODUCT explicitly favors GraphQL first; document Apollo as the alternative with the same research.

2. **Second operation**
   - Known: Phase allows “one or two” operations.
   - Unclear: Whether to ship one (e.g. GET /) or two (e.g. GET / and GET /greeting, or query + mutation).
   - Recommendation: Plan for two operations (e.g. root + one resource or one query + one mutation) so the learner sees two distinct operations; keep both minimal.

## Sources

### Primary (HIGH confidence)
- FastAPI First Steps — https://fastapi.tiangolo.com/tutorial/first-steps/ (minimal app, run command, /docs)
- Express Hello World — https://expressjs.com/en/starter/hello-world.html (minimal app, run command)
- Spring Building a RESTful Web Service — https://spring.io/guides/gs/rest-service/ (GreetingController, run with Gradle/Maven)
- Apollo Server Getting Started — https://www.apollographql.com/docs/apollo-server/getting-started (schema, resolvers, startStandaloneServer, Sandbox)
- GraphQL Running an Express GraphQL Server — https://graphql.org/graphql-js/running-an-express-graphql-server (graphql-http, createHandler, ruru)

### Secondary (MEDIUM confidence)
- express-graphql deprecated in favor of graphql-http (GraphQL Foundation 2022; express-graphql archived March 2023) — WebSearch + graphql.org blog
- FastAPI vs Express vs Spring learning curve / minimal endpoint — WebSearch (comparison articles)
- Apollo startStandaloneServer vs expressMiddleware — Apollo docs + Stack Overflow
- Express res.json vs res.send for JSON — Stack Overflow (prefer res.json for REST APIs)

### Tertiary (LOW confidence)
- Exact FastAPI CLI availability in all environments (fastapi dev) — documented in FastAPI docs; assume standard install includes it.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — official first-steps and getting-started guides for all five options.
- Architecture: HIGH — single-file patterns and run commands from official sources.
- Pitfalls: HIGH — express-graphql deprecation and graphql-http adoption are documented; learner “see response” and “two ops” are logic checks.

**Research date:** 2026-02-25
**Valid until:** ~30 days for stable stacks; re-check GraphQL docs if graphql-http or Apollo change.

---

## RESEARCH COMPLETE

**Phase:** 1 - Foundation  
**Confidence:** HIGH

### Key findings
- **REST:** FastAPI = one file + `fastapi dev main.py` + /docs; Express = one file + `node app.js` (use `res.json` for REST); Spring = multiple files + build, best when JVM required.
- **GraphQL:** Apollo Server 4 with `startStandaloneServer` = one file + `npm start` + Sandbox; graphql-js + graphql-http with Express = official replacement for deprecated express-graphql.
- **Single-command run** is supported by every stack; document the exact command and one way to call the API (curl or Sandbox).
- **Recommendation:** Use REST with FastAPI for Phase 1 unless the product choice is GraphQL-first; then use Apollo Server. Planner can lock one option and implement minimal schema + one or two operations.

### File created
`graphql-rest-tutorial/.planning/phases/01-foundation/01-RESEARCH.md`

### Confidence assessment
| Area          | Level | Reason                                              |
|---------------|-------|-----------------------------------------------------|
| Standard stack| HIGH  | Official first-steps for FastAPI, Express, Spring, Apollo, graphql-http |
| Architecture  | HIGH  | Single-file and run commands from official docs     |
| Pitfalls      | HIGH  | express-graphql deprecation and testing flow verified |

### Open questions
- REST vs GraphQL for Phase 1: recommend REST + FastAPI by default; Apollo if GraphQL-first.
- Second operation: plan for two minimal operations (e.g. GET / and GET /resource, or one query + one mutation).

### Ready for planning
Research complete. Planner can create PLAN.md with tasks for one chosen stack (REST+FastAPI or GraphQL+Apollo recommended), minimal schema, one or two operations, single-command run, and verification step (call API and see response).
