# 📚 Knowledge Hub – Intelligent Interest-Based Knowledge Aggregation Platform

## 🔥 Overview

**Knowledge Hub** is an AI-powered system that aggregates, processes, tags, summarizes, and delivers knowledge updates based on user interests.  
Users define their _interest tags_, and the system automatically fetches the latest content from curated sources, processes them through an LLM-driven engine, and generates daily updates.

The system is built as a **polyglot microservice architecture**:

- **Spring Boot (Java)** → Entity management, admin APIs, scheduling, metadata storage
- **Python Engine** → LLM workflows, summarization, scraping, tag inference
- **gRPC** → High-performance, strongly typed communication
- **PostgreSQL** → Central knowledge-base storage

This architecture supports both **enterprise reliability** and **AI-driven flexibility**.

---

# 🧩 Core Features

### ✔ Source Management

- Add blogs, docs, and private sources
- Auth strategies: public, API key, OAuth, custom
- Configurable fetch frequency
- Multi-tag assignment

### ✔ Interest Tag System

- Controlled tag list (hardcoded initially)
- Used for LLM grounding
- Centralized storage for consistency

### ✔ LLM-Powered Content Engine

Built using Python + LangGraph + MCP:

- Web scraping & content extraction
- Clean summary generation
- Tag inference using controlled list
- Importance ranking
- Metadata generation
- Daily digest creation

### ✔ Daily Knowledge Digest

For each tag, the system creates:

- Summary
- Key insights
- Relevant references
- Trend score

---

# 🏛 Architecture

+-----------------+ gRPC +--------------------------+
| Spring Boot | <-----------------> | Python Knowledge Engine |
| (Management API) | | (LLM + Scraping + Tags) |
+------------------+ +--------------------------+
| |
| CRUD + scheduling + admin UI |
+-------------------+--------------------+
|
PostgreSQL
(central knowledge base)

---

# ⚙️ Service Responsibilities

## 1️⃣ Java Service – Knowledge Manager

Handles:

- CRUD (sources, tags, auth strategies)
- Persistent storage & history
- Scheduling ingestion jobs
- Admin API / GraphQL
- Configuration management
- UI support
- Monitoring of Python engine

**Why Java?**  
Enterprise stability, concurrency, operational tooling, reliable background jobs.

---

## 2️⃣ Python Service – Knowledge Engine

Handles:

- Scraping & content cleaning
- LLM summarization
- Tag inference
- LangGraph agent workflows
- MCP integrations
- Metadata extraction
- Error recovery

**Why Python?**  
Fast iteration, strong LLM ecosystem, scraping libraries, agent frameworks.

---

## 3️⃣ gRPC Layer

Enables fast, typed communication.

**Key RPC Calls**

- `AnalyzeSource(url, auth)`
- `ExtractTags(summary)`
- `Summarize(raw_content)`
- `GenerateDailyDigest(tag)`
- `RefreshSource(sourceId)`

---

# 🗄 Database Schema (High Level)

### `source`

| Field           | Description                       |
| --------------- | --------------------------------- |
| id              | Primary key                       |
| url             | Website/blog/doc source           |
| tags            | List of controlled tags           |
| auth_strategy   | public / api_key / oauth / custom |
| auth_json       | JSON metadata                     |
| fetch_frequency | cron-like or enum                 |
| last_fetched_at | timestamp                         |

---

### `tag`

| Field       | Description |
| ----------- | ----------- |
| id          | Primary key |
| name        | Tag name    |
| description | Tag meaning |

---

### `source_ingestion`

| Field          | Description             |
| -------------- | ----------------------- |
| source_id      | FK to source            |
| raw_content    | Text / JSON             |
| summary        | LLM-generated summary   |
| extracted_tags | List of tags            |
| llm_metadata   | token usage, confidence |
| created_at     | timestamp               |

---

### `daily_digest`

| Field       | Description         |
| ----------- | ------------------- |
| tag_id      | FK to tag           |
| digest_text | Summary for the day |
| created_at  | timestamp           |

---

# 🔁 Workflows

## 🔹 Source Ingestion Pipeline

1. Java selects sources to refresh
2. Calls Python engine through gRPC
3. Python scrapes + processes content
4. Produces summary & metadata
5. Java stores ingestion history
6. Java updates timestamps

---

## 🔹 Daily Digest Pipeline

1. Scheduled job in Spring Boot
2. Python generates digest for each tag
3. Java stores digest
4. Users view digest through API/UI

---

# 🚀 Development Roadmap

### **Phase 1 — Core MVP**

- Source ingestion
- Controlled tags
- Basic summarization
- CRUD APIs
- Python gRPC engine

### **Phase 2 — LLM Enhancements**

- Tag refinement
- Better summaries
- Document chunking
- Trend analysis

### **Phase 3 — Automation**

- Auto-source discovery
- LLM-based noise filtering
- Embeddings for context persistence

### **Phase 4 — User Experience**

- Web UI
- Personalized interest feeds
- Saved digests

### **Phase 5 — Enterprise**

- Multi-tenancy
- RBAC
- Rate limiting
- Audit logs

---

# 🎯 Future Enhancements (Production-Grade)

### 🔹 Recommendation Engine

Suggest new tags or sources using ML.

### 🔹 Vector Search

Using PGVector / Pinecone for semantic search.

### 🔹 Autonomous Agents

LangGraph-driven continuous monitoring agents.

### 🔹 Plug-In Architecture (MCP)

Allow external tools to register:

- new scrapers
- new LLM pipelines
- new analysis modules

### 🔹 Multi-Lingual Support

Digest generation in:

- English
- Hindi
- Tamil
- Japanese  
  etc.

### 🔹 Mobile App

Push notifications for daily updates or critical releases.

### 🔹 Enterprise Security

- API key encryption
- Secrets manager
- SSO & OAuth
- Per-source access control

---

# 📦 Tech Stack Summary

**Backend (Java)**

- Java 21
- Spring Boot 3.x
- Spring Data JPA
- GraphQL (optional)

**AI Engine (Python)**

- Python 3.12
- LangGraph
- MCP
- OpenAI / Anthropic / Local LLMs
- Playwright / Requests / BeautifulSoup

**Communication**

- gRPC (Protocol Buffers v3)

**Database**

- PostgreSQL + JSONB
- Optional vector store

---
