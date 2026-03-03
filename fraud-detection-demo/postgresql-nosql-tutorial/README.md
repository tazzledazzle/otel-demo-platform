# PostgreSQL + NoSQL Tutorial

Tutorial for software engineers: PostgreSQL and NoSQL (MongoDB). Phase 1 provides two separate runnable examples—one for Postgres, one for MongoDB.

## Prerequisites

- **PostgreSQL** — running locally, in Docker, or in the cloud.
- **MongoDB** — running locally, in Docker, or via [MongoDB Atlas](https://www.mongodb.com/atlas) (free tier).

### Running with Docker

```bash
# PostgreSQL (default port 5432)
docker run -d --name postgres-tutorial -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:16

# MongoDB (default port 27017)
docker run -d --name mongo-tutorial -p 27017:27017 mongo:7
```

### MongoDB Atlas

Create a free cluster at [MongoDB Atlas](https://www.mongodb.com/atlas), get the connection string, and set `MONGODB_URI` to that value (e.g. `mongodb+srv://user:pass@cluster.mongodb.net/`).

## Environment variables

| Variable       | Default                        | Description                |
|----------------|--------------------------------|----------------------------|
| `DATABASE_URL` | `postgresql://localhost/postgres` | PostgreSQL connection DSN |
| `MONGODB_URI`  | `mongodb://localhost:27017`    | MongoDB connection URI     |

Copy `.env.example` to `.env` and adjust if your Postgres or MongoDB are not on localhost or use auth.

## Run steps

```bash
# Install dependencies
pip install -r requirements.txt

# Set env vars if needed (or use .env)
# export DATABASE_URL=postgresql://user:pass@localhost/postgres
# export MONGODB_URI=mongodb://localhost:27017

# Run PostgreSQL example
python postgres_example.py

# Run MongoDB example
python mongodb_example.py
```

- **postgres_example.py** — Connects with `DATABASE_URL`, runs `SELECT now()`, prints server time.
- **mongodb_example.py** — Connects with `MONGODB_URI`, inserts a document into `tutorial.demo`, finds it, and prints it.
