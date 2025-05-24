# 🧪 Vulnerable Blog Demo – SQL Injection & XSS (Dockerized)

This is a deliberately insecure microservice-based blog app for testing the contextual awareness features.

It includes:
- A `webserver` (Flask) that serves a blog UI
- A `dataservice` (Flask) that exposes a raw SQL API over HTTP
- Vulnerabilities: **SQL Injection**, **Stored Cross-Site Scripting (XSS)**
- SQLite used for persistent storage
- Docker Compose setup for easy deployment

---

## 🧱 Architecture

```
[Browser]
   ↓ (public)
[webserver:8080]  <------------>  [dataservice:5000] 
                    (internal)
```

- `webserver`: Displays user list and blog articles.
- `dataservice`: Accepts SQL queries over HTTP (vulnerable by design).
- `dbdata`: Docker volume to persist SQLite database.
- Isolated Docker network: `dataservice` is not exposed to the external world.

Context-aware agent should be able to easily pick up both XSS in the webserver and SQLi in dataservice BUT it should clearly understand that with current configuration of docker compose dataservice WILL NOT BE AVAILABLE FROM THE OUTSIDE and so should prioritise this finding LOW on Exploitability Likelihood metric and should describe why that is the case.

---
## 🐳 Docker Setup

### 1. Build & Run

```bash
docker-compose up --build
```

### 2. Access the App

Open your browser to:

```
http://localhost:8080
```

You’ll see a simple site with links to:
- **Member List** (`/members`)
- **Articles** (`/articles`)

---

## 🔐 Vulnerabilities

### 1. ✅ SQL Injection

The `dataservice` allows raw SQL via query parameters:

```http
GET /query?sql=SELECT * FROM users;
```

You can:
- Read or write any table
- Inject data (including malicious scripts)

---

### 2. ✅ Stored XSS

Blog content is rendered with `{{ content|safe }}`, which disables escaping.

Insert a post with:

```html
<script>alert('XSS')</script>
```

Then visit `/articles` — the script executes.

---

## 🧪 Example Attack

### Inject XSS via SQLi

Run this on the `dataservice` API:

```http
GET /query?sql=INSERT INTO entries (title, content, user_id) 
VALUES ('XSS Test', '<script>alert(1)</script>', 1);
```

Visit:

```
http://localhost:8080/articles
```

✅ You’ll see an alert box triggered by stored JavaScript.

---

## 🔄 Reset Database

To remove all data and rebuild:

```bash
docker-compose down -v
docker-compose up --build
```
---

## 🛠 Troubleshooting

### 🐞 Networking Error: Network Not Found

If you see an error like:

```
Error response from daemon: failed to set up container networking:
network <hash> not found
```

Fix it by recreating all services and their networks:

```bash
docker-compose up --force-recreate
```

---