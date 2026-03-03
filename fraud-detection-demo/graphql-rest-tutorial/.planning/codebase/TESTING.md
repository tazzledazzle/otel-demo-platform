# Testing Patterns

**Analysis Date:** 2025-02-25

## Test Framework

**Runner:** Not applicable. No application code or test framework is present.

**Config:** None. When the first phase introduces code, add a framework (e.g. Jest/vitest for Node, pytest for Python, JUnit for Java) and document the config path here.

**Run Commands:** To be defined when tests exist, e.g.:
```bash
# Placeholder—replace with actual commands per stack
npm test              # or pytest, ./gradlew test, etc.
npm run test:watch   # watch mode if applicable
npm run test:coverage
```

## Test File Organization

**Location:** Not applicable. When tests are added, prefer either co-located (e.g. `*.test.ts` next to source) or a dedicated `tests/` directory; document the choice in the phase plan and here.

**Naming:** Use the convention of the chosen framework (e.g. `*.test.ts`, `*_spec.py`, `*Test.java`).

## Test Structure

**Suite organization:** Not applicable. When adding tests, structure by feature or by API surface (e.g. "GraphQL resolvers", "REST /users") so tutorial learners can follow.

## Mocking

**Framework:** To be chosen with the stack. For GraphQL/REST tutorials, typical needs: mock data for resolvers, mock HTTP for client examples.

**What to mock:** External services, databases (if out of scope for the lesson). Prefer in-memory or fixture-based data for tutorial clarity.

**What NOT to mock:** The unit under test (resolver, handler); mock only boundaries.

## Fixtures and Factories

**Test data:** Not applicable. When added, place under `tests/fixtures/` or next to test files; keep sample queries, JSON payloads, and schema snippets versioned for reproducibility.

## Coverage

**Requirements:** None enforced. When code exists, aim for at least critical paths (e.g. main resolvers or REST handlers) and document the target in this file.

## Test Types

**Unit tests:** To be added for resolvers, handlers, and shared logic when the stack is introduced.

**Integration tests:** Optional for tutorial; useful for "full request → response" examples (e.g. GraphQL endpoint, REST resource).

**E2E tests:** Not required for a tutorial scaffold; optional if the roadmap includes client integration.

## Common Patterns

**Async testing:** Follow the chosen framework’s pattern (e.g. async/await in Jest, pytest-asyncio for async Python).

**Error testing:** Assert on HTTP status and error shape (REST) or GraphQL errors array and extensions (GraphQL) when testing failure cases.

---

*Testing analysis: 2025-02-25*
