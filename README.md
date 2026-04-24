# 🚀 AI-Powered DevSecOps PR Review Agent

An intelligent **DevSecOps automation agent** that analyzes pull requests in real-time, detects security & best practice issues, and posts **AI-generated review comments directly on GitHub PRs**.

---

## 🔥 Key Features

* 🔍 **Automated PR Analysis**

  * Fetches PR diffs via GitHub API
  * Parses code changes intelligently

* 🛡️ **Security & Best Practice Checks**

  * Detects secrets (API keys, tokens)
  * Dockerfile misconfigurations
  * Kubernetes security issues
  * Python code quality issues

* 🤖 **AI-Powered Code Review**

  * Generates human-like review feedback
  * Summarizes findings with actionable suggestions

* 💬 **Smart PR Commenting**

  * Creates or updates a single bot comment
  * Avoids duplicate spam using tagging system

* ⚡ **CI/CD Integrated**

  * GitHub Actions pipeline
  * Linting (Flake8)
  * Security scanning (Bandit)
  * Container scanning (Trivy)

---

## 🏗️ Architecture

```
GitHub PR Event (Webhook)
        ↓
FastAPI Webhook Server
        ↓
PR Diff Fetcher (GitHub API)
        ↓
Diff Parser
        ↓
Rule Engine (Security + Best Practices)
        ↓
AI Reviewer (LLM)
        ↓
PR Comment Bot (Create/Update)
```

---

## 🛠️ Tech Stack

* **Backend:** FastAPI, Python
* **DevOps:** Docker, GitHub Actions
* **Security Tools:** Bandit, Trivy
* **AI Integration:** OpenAI API
* **Parsing:** Custom diff parser
* **Version Control:** Git & GitHub

---

## 📂 Project Structure

```
AI-Powered-DevSecOps-PR-Review-Agent/
│
├── app/
│   ├── main.py              # FastAPI webhook server
│   ├── github_client.py     # GitHub API integration
│   ├── diff_parser.py       # PR diff parsing
│   └── ai_reviewer.py       # AI review generation
│
├── rules/
│   ├── secrets.py           # Secret detection
│   ├── docker.py            # Docker checks
│   ├── k8s.py               # Kubernetes checks
│   └── python.py            # Python lint checks
│
├── tests/                   # Unit tests
├── Dockerfile               # Container setup
├── requirements.txt         # Dependencies
├── .github/workflows/ci.yml # CI/CD pipeline
└── README.md
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Pooja160701/AI-Powered-DevSecOps-PR-Review-Agent.git
cd AI-Powered-DevSecOps-PR-Review-Agent
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure environment variables

Create a `.env` file:

```env
GITHUB_TOKEN=your_github_token
OPENAI_API_KEY=your_openai_api_key
```

---

### 5️⃣ Run the server

```bash
python -m uvicorn app.main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

---

## 🔗 Webhook Setup (GitHub)

1. Go to your repository → **Settings → Webhooks**
2. Add webhook:

   * **Payload URL:**

     ```
     http://<your-ngrok-url>/webhook
     ```
   * **Content Type:** `application/json`
   * **Events:** Select **Pull Requests**

---

## 🌐 Expose Local Server (ngrok)

```bash
ngrok http 8000
```

Copy the HTTPS URL into GitHub webhook.

---

## 🧪 Testing Webhook Locally

```bash
curl -X POST http://127.0.0.1:8000/webhook \
-H "Content-Type: application/json" \
-H "X-GitHub-Event: pull_request" \
-d '{
  "action": "opened",
  "pull_request": {"number": 1},
  "repository": {"full_name": "your-username/repo"}
}'
```

---

## ⚡ CI/CD Pipeline

GitHub Actions pipeline includes:

* ✅ **Flake8** → Code linting
* 🔐 **Bandit** → Python security scanning
* 🐳 **Trivy** → Docker image vulnerability scanning

---

## 🐳 Docker Usage

### Build image

```bash
docker build -t devsecops-agent .
```

### Run container

```bash
docker run -p 8000:8000 devsecops-agent
```

---