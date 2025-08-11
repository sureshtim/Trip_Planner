# 🧳 AI Travel Planner Agent

An AI-powered trip planning assistant built using the **LangGraph** framework.  
This agent can help you plan your trip, suggest itineraries, and manage your travel preferences.

---

## 🚀 Quick Start

| Step | Command | Description |
|------|---------|-------------|
| 1️⃣ | `uv --version` | Check if `uv` is installed |
| 2️⃣ | `pip install uv` | Install `uv` package manager |
| 3️⃣ | `uv init Travel_Planner` | Create project structure |
| 4️⃣ | `uv pip list` | View installed Python libraries |
| 5️⃣ | `uv python list` | Check available Python versions |
| 6️⃣ | `uv python install cpython-3.10.18-windows-x86_64-none` | Install CPython 3.10.18 |
| 7️⃣ | `conda deactivate` *(if Conda is active)* | Deactivate Conda to avoid conflicts |
| 8️⃣ | `uv venv env --python cpython-3.10.18-windows-x86_64-none` | Create virtual environment |
| 9️⃣ | `Trip_Planner\env\Scripts\activate.bat` | Activate environment (Windows) |
| 🔟 | `uv add pandas` | Install dependencies |

---

## ▶️ Running the Application

**Run FastAPI backend:**
uvicorn main:app --reload --port 8000

**Run Streamlit frontend:**
streamlit run streamlit_app.py
