# 🧳 AI Travel Planner Agent – Workspace Instructions

## Project Overview
**AI Travel Planner** is an LLM-powered agentic application that helps users plan trips with real-world data (weather, locations, expenses, currency conversion). Built with **LangGraph**, **FastAPI**, and **Streamlit**.

- **Purpose**: AI-driven trip planning with tool-augmented search capabilities  
- **Architecture**: Agent-based ReAct pattern with external tool integration  
- **Frontend**: Streamlit UI → Backend: FastAPI REST API → Agent: LangGraph workflow  

---

## 🏗️ Architecture & Component Structure

### Core Layers

| Layer | Components | Responsibility |
|-------|-----------|-----------------|
| **UI Layer** | `streamlit_app.py` | ChatUI for trip queries |
| **API Layer** | `main.py` | FastAPI endpoints (/query) with CORS |
| **Agent Layer** | `agent/agentic_workflow.py` | LangGraph StatεGraph with tool routing |
| **Tools Layer** | `tools/*` | Weather, Places, Expenses, Currency tools |
| **Utils Layer** | `utils/*` | LLM loading, config parsing, API calls |
| **Config Layer** | `config/config.yaml` | LLM providers and model selection |

### Data Flow
```
User Query (Streamlit) 
  → POST /query (FastAPI)
  → GraphBuilder.build_graph() 
  → Agent chooses tools
  → Tools execute (parallel/sequential)
  → LLM synthesizes response
  → JSON response → Streamlit renders
```

---

## 🛠️ Development Setup

### Prerequisites
- **Python 3.13+** (as per `pyproject.toml`)
- **uv package manager** (recommended) - faster than pip
- **Environment variables** (`.env`): API keys for Groq/OpenAI, Google Places, Tavily

### Environment Setup
```bash
# Clone/Navigate to project
cd /Users/stim/Desktop/Trip_Planner

# Activate uv (or use Python venv)
uv venv env --python 3.13
source env/bin/activate  # macOS/Linux
# OR: env\Scripts\activate  # Windows

# Install dependencies
uv pip install -r requirements.txt
# OR: pip install -r requirements.txt

# Verify installation
python -c "import langgraph; import streamlit; import fastapi; print('✅ All imports OK')"
```

### Running the Application

**Option A: Parallel Terminals (Recommended)**
```bash
# Terminal 1 - Backend API
python -m uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend UI
python -m streamlit run streamlit_app.py
```
Then open `http://localhost:8501` (Streamlit default port)

**Option B: Single Terminal**
```bash
# Start backend in background
python -m uvicorn main:app --reload --port 8000 &

# Start frontend (foreground)
python -m streamlit run streamlit_app.py
```

### Testing
```bash
# Test agent locally (no UI)
python -c "
from agent.agentic_workflow import GraphBuilder
graph = GraphBuilder('groq')()
result = graph.invoke({'messages': ['Plan a 3-day trip to Paris']})
print(result['messages'][-1].content)
"

# Test individual tool
python -c "
from tools.weather_info_tool import WeatherInfoTool
tool = WeatherInfoTool()
print(tool.weather_tool_list)  # List available tools
"
```

---

## 📁 Project Structure & Patterns

### Tool Creation Pattern
All external tools follow a consistent pattern in `tools/`:

```python
# tools/my_custom_tool.py
from langchain_core.tools import tool

class MyCustomTool:
    def __init__(self):
        self.my_custom_tool_list = [self.fetch_data]
    
    @tool
    def fetch_data(self, input_param: str) -> str:
        """Tool docstring (used in agent context)"""
        # Implementation
        return "result"
```

**How tools integrate into agent:**
1. Tool class instantiated in `GraphBuilder.__init__()`
2. Tool list appended to `self.tools`
3. Tools bound to LLM: `self.llm_with_tools = self.llm.bind_tools(tools=self.tools)`
4. ToolNode in graph routes tool calls automatically

### Config Management
- `config/config.yaml`: LLM provider/model selection
- `utils/config_loader.py`: YAML parsing utility
- **Pattern**: Add new configs to YAML → Load in relevant utils → Access via `load_config()`

### Exception Handling
- `exception/exceptionhandeling.py`: Centralized error handling (create custom exceptions here)
- **Pattern**: Raise domain-specific exceptions in tools/utils, catch in FastAPI endpoints

### Logging
- `logger/logging.py`: Structured logging setup
- **Usage**: Import and configure at module level for debugging

---

## 🎯 Common Development Tasks

### Add a New Tool
1. Create file: `tools/my_tool.py`
2. Implement tool class with `@tool` decorator
3. Add to `GraphBuilder.__init__()`:
   ```python
   self.my_tools = MyTool()
   self.tools.extend([*self.my_tools.my_tool_list])
   ```
4. Test with: `python -c "from tools.my_tool import MyTool; MyTool().tool_name({'param': 'value'})"`

### Add a New LLM Provider
1. Update `config/config.yaml` with new provider
2. Modify `utils/model_loader.py` to instantiate new provider's LLM
3. Pass provider name: `GraphBuilder(model_provider="new_provider")()`

### Modify System Prompt
- Edit: `prompt_library/prompt.py` → Update `SYSTEM_PROMPT`
- This is prepended to all agent messages in `agent_function()`

### Debug Agent Workflow
- Uncomment `print()` in `main.py` to see query requests
- Agent saves visualization: `my_graph.png` in project root
- Enable Streamlit logger: `streamlit run streamlit_app.py --logger.level=debug`

### Add Intermediate Nodes
If agent needs preprocessing/postprocessing between tool calls:
```python
# In GraphBuilder.build_graph():
graph_builder.add_node("preprocess", self.preprocess_function)
graph_builder.add_node("postprocess", self.postprocess_function)
# Then add edges to control flow
```

---

## ⚙️ Key Configuration Points

| Config | Location | Purpose | Example |
|--------|----------|---------|---------|
| LLM Model | `config/config.yaml` | Select Groq/OpenAI model | `groq`: `deepseek-r1-distill-llama-70b` |
| API Keys | `.env` (not in repo) | External service auth | `GROQ_API_KEY`, `OPENAI_API_KEY` |
| Backend Port | `main.py` | FastAPI server port | `--port 8000` |
| CORS Origins | `main.py` | Allowed frontend domains | `allow_origins=["*"]` (change in prod) |
| Base URL | `streamlit_app.py` | Backend endpoint | `BASE_URL = "http://localhost:8000"` |

---

## 🔑 Environment Variables Required
Create `.env` file in project root:
```bash
GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key  # if using OpenAI
GOOGLE_PLACES_API_KEY=your_places_key
TAVILY_API_KEY=your_tavily_key
```

---

## 🐛 Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError` for tools | Virtual env not activated | Run `source env/bin/activate` |
| API returns 401 | Missing/invalid API keys | Check `.env` file and API provider dashboards |
| Agent hangs | Tool stuck in infinite loop | Check tool docstring format and add timeouts |
| Port 8000 already in use | Another process owns it | `lsof -i :8000` and kill, or use `--port 8001` |
| Streamlit not connecting to API | CORS issue or wrong BASE_URL | Verify `BASE_URL` in `streamlit_app.py` matches actual backend |

---

## 📚 Key Files Reference

- **Entry Points**: `main.py` (API), `streamlit_app.py` (UI)  
- **Agent Logic**: `agent/agentic_workflow.py` (GraphBuilder & graph construction)  
- **System Prompt**: `prompt_library/prompt.py` (agent instructions)  
- **Tool Definitions**: `tools/*.py` (all tool implementations)  
- **Utilities**: `utils/model_loader.py` (LLM instantiation), `utils/config_loader.py` (config parsing)  

---

## 🚀 Best Practices

1. **Always test tools in isolation** before adding to GraphBuilder  
2. **Use type hints** in tool parameters for better LLM context  
3. **Keep tool docstrings clear** – the agent reads these to decide tool usage  
4. **Fail fast**: Raise exceptions early in tools, catch at API layer  
5. **Log important steps** in agent flow for debugging  
6. **Config over hardcoding**: Store API endpoints, ports, keys in config/env  
7. **Single Responsibility**: Each tool should do one thing well  

---

## 🔗 Related Documentation
- [README.md](../../README.md) – Project overview and quick start  
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/) – Agent workflow patterns  
- [FastAPI Docs](https://fastapi.tiangolo.com/) – API development  
- [Streamlit Docs](https://docs.streamlit.io/) – Frontend development  

---

**Last Updated**: March 2026  
**Python Version**: 3.13+  
**Package Manager**: uv (or pip)
