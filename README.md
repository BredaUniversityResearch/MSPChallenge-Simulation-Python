# ⚙️ Python Environment Setup & Technology Stack Mapping

This guide provides instructions for setting up the Python environment and outlines the equivalent Python stack for a C#-style backend system. The application involves components such as REST APIs, asynchronous task handling, event-driven simulation, and a state machine.

---

## 🐍 Python Version Requirement

> ✅ **Required Version**: `Python 3.12.9`

Before proceeding, make sure that you have **Python 3.12.9** installed on your system. You can [download it from the official Python site](https://www.python.org/downloads/release/python-3129/).

> ⚠️ Using other versions may lead to incompatibility issues with libraries used in the project.

---

## 🧪 Create a Virtual Environment (Windows)

To keep dependencies isolated and reproducible, it's recommended to create a **virtual environment** inside your project directory.

1. Open a terminal or PowerShell window.
2. Navigate to your project folder.
3. Run the following command to create a virtual environment:

```bash
python -m venv .venv
```

This will create a new folder named `.venv` in your current directory, containing a standalone Python environment.

---

## 🚀 Activate the Virtual Environment (Windows)

To activate the environment, run:

```bash
.\.venv\Scripts\Activate
```

After activation, your terminal prompt should change to show the environment is active (e.g., it may show `(.venv)`).

---

## 📦 Install Project Requirements

Once the environment is activated, install the required dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

This will install all the necessary libraries for running the project.

---

## 🧰 C# to Python Feature Mapping

This application was initially inspired by C#-based architectures (e.g., ASP.NET Core) and has been translated into Python using modern, equivalent tools.

Below is a mapping of key C# features to their Python counterparts:

| 💻 C# Feature                          | 🐍 Python Equivalent                                                                 |
|----------------------------------------|--------------------------------------------------------------------------------------|
| **ASP.NET Core (Web API)**            | [`FastAPI`](https://fastapi.tiangolo.com/) - High-performance REST API framework    |
| **State Machine (ProgramStateMachine)** | [`transitions`](https://github.com/pytransitions/transitions) - Lightweight FSM lib |
| **Async Tasks (Task, ContinueWith)**  | `asyncio`, `concurrent.futures` - Native Python async & futures execution           |
| **HTTP Requests (HttpPost)**          | [`httpx`](https://www.python-httpx.org/), [`requests`](https://requests.readthedocs.io/) |
| **Events (OnSimulationDefinitionsEvent)** | Python callbacks, `asyncio.Event` for async signaling                         |
| **Json Serialization (Newtonsoft.Json)** | [`pydantic`](https://docs.pydantic.dev/), `json` - Data validation & encoding    |
| **Dependency Injection (builder.Services)** | [`dependency_injector`](https://python-dependency-injector.ets-labs.org/)        |
| **Timers (Timer(Tick, ...))**         | `asyncio` loop and scheduled coroutines for timed execution                         |

---

## 🧪 Summary

By combining these tools, you can replicate many architectural and runtime behaviors from a C#-based backend within a modern Python ecosystem — including:
- RESTful APIs with FastAPI  
- Reactive simulations using state machines and asyncio  
- Event-driven logic and task scheduling  
- Strong data modeling and validation with Pydantic  
- Decoupled architecture using dependency injection  

