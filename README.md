# 🇫🇷 France UNSC Crisis Command

> AI-Powered UN Security Council Intelligence, Training & Diplomatic Simulation Platform

---

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Configure AI provider
# Copy and edit the .env file — add your GEMINI_API_KEY
# (The .env file is already created — just add your API key)

# Start the server
python run.py
# Runs at: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
# Runs at: http://localhost:5173
```

---

## 🔑 Configure Your Gemini API Key

Edit `backend/.env` and replace `YOUR_GOOGLE_API_KEY_HERE`:

```
GEMINI_API_KEY="your-actual-gemini-api-key"
```

Get your key at: https://aistudio.google.com/app/apikey

---

## 👤 Default Login

| Field    | Value                      |
|----------|---------------------------|
| Email    | `admin@france-unsc.org`   |
| Password | `admin123`                 |
| Role     | Admin                      |

---

## 🏗 Project Structure

```
mun/
├── backend/               # FastAPI Python backend
│   ├── app/
│   │   ├── ai/            # AI agents & providers (Gemini, Claude, OpenAI, Local)
│   │   │   ├── agents/    # country_agent, france_coach, orchestrator, research
│   │   │   └── providers/ # gemini, claude, openai, local, factory
│   │   ├── api/v1/        # REST endpoints (auth, chat, crisis, practice, training, ...)
│   │   ├── models/        # SQLAlchemy DB models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── data/          # Database seeders
│   ├── .env               # ← Add your API keys here
│   └── requirements.txt
│
└── frontend/              # React + Vite + Tailwind frontend
    └── src/
        ├── components/    # 9 major UI views
        ├── lib/api.ts     # API client with auth
        └── types/         # TypeScript types
```

---

## 🎯 Features

| Module               | Description |
|----------------------|-------------|
| 🌍 World Intelligence | Real-time global crisis map, alerts, region intel |
| 🎓 Crisis Trainer     | AI-guided step-by-step crisis training |
| ⚔️ Practice Arena    | Full diplomatic simulation with AI country delegates |
| 🇫🇷 France Command   | France's doctrine, veto history, diplomatic positions |
| 🗃 UNSC Database     | Members, resolutions, votes, peacekeeping missions |
| 🧪 Diplomacy Labs    | Speech analyzer, resolution validator, EB Q&A |
| 📊 Analytics         | Performance metrics, learning progress |
| 🔐 Auth System       | Multi-user login, roles (student/delegate/coach/admin) |

---

## 🤖 AI System

The platform uses a **4-specialist agent architecture**:

- **Research Agent** — Gemini 3.8 Flash — geopolitical analysis
- **Country Agent** — Gemini 3.5 Flash-Lite — country delegate simulation  
- **France Coach** — Gemini 3.8 Flash — MUN coaching & feedback
- **Orchestrator** — Gemini 3.8 Flash — multi-agent coordination

---

## 🔐 Auth API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register` | POST | Create account |
| `/api/v1/auth/login` | POST | Login & get token |
| `/api/v1/auth/me` | GET | Get current user |
| `/api/v1/auth/status` | GET | Check token validity |
| `/api/v1/auth/change-password` | POST | Change password |
| `/api/v1/auth/users` | GET | List users (admin only) |

---

## 📋 User Roles

| Role      | Access |
|-----------|--------|
| `student` | Basic access |
| `delegate`| Full practice arena |
| `coach`   | + Training management |
| `admin`   | Full system access |
