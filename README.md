# 🛰️ MSP Challenge – External Watchdog Simulation Example

This repository contains an **example implementation** of an *external watchdog server* that integrates with the [MSP Challenge](https://www.mspchallenge.info/) simulation platform. It showcases how to build an external simulation that connects to the MSP Challenge server and contributes simulated KPI data.

---

## 🧭 Project Overview

### 🌊 About MSP Challenge

[MSP Challenge](https://www.mspchallenge.info/) is a simulation platform designed to support **maritime spatial planning** through interactive, science-based tools. It consists of:

- A **server**, which hosts simulations and manages game sessions.
- A **client**, used by stakeholders to plan and evaluate maritime strategies.

Key server simulations include:
- [Ecology (MEL & EwE)](https://community.mspchallenge.info/wiki/Ecosystem_simulation_(MEL_%26_EwE))
- [Energy (CEL)](https://community.mspchallenge.info/wiki/Energy_simulation_(CEL))
- [Shipping (SEL)](https://community.mspchallenge.info/wiki/Shipping_simulation_(SEL))

As of version [5.1 (March 2025)](https://github.com/BredaUniversityResearch/MSPChallenge-Server/tags), the platform supports **external simulations** via a plugin system for *watchdog services*.

### ☀️ Example: Sun Hours Watchdog

This example implements a simulation that reports **sun hours per country** as KPIs each month. It demonstrates how to:
- Connect to a local MSP Challenge server
- Handle simulation events (setup, simulate, report)
- Send KPI results to the server using a REST API

A full walkthrough and installation instructions can be found in the original C# project ([MSP Challenge Simulation Example](https://github.com/BredaUniversityResearch/MSPChallenge-Simulation-Example/blob/main/README.md)).

---

## ⚙️ Python Stack Overview (for Reimplementation)

This project is a full Python equivalent implementation of the original C# sun hours example.

### 🐍 Python Version Requirement

> ✅ Required version: `Python 3.12.9`

Install [Python 3.12.9](https://www.python.org/downloads/release/python-3129/) before proceeding.

---

### 🧪 Setting up a Python Environment (Windows)

1. Open a terminal inside the project directory.
2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the environment:

```bash
.\.venv\Scripts\Activate
```

4. Install required dependencies:

```bash
pip install -r requirements.txt
```

---

### 🔁 C# to Python Feature Mapping

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

## 🚀 Getting Started with the Example Watchdog

### 📦 Prerequisites

1. Install [MSP Challenge Server 5.1+](https://github.com/BredaUniversityResearch/MSPChallenge-Server) using Docker
2. Install [MSP Challenge Client 5.1+](https://github.com/BredaUniversityResearch/MSPChallenge-Client/releases)
3. Launch and test the Server Manager: [http://localhost/manager](http://localhost/manager)

### 📂 Installation Steps

1. Download the [latest release](https://github.com/BredaUniversityResearch/MSPChallenge-Simulation-Example/releases) — **do not clone** the repo.
2. Copy contents into your own repo for custom simulation development.
3. Run the `program_manager.py` in command line (**py program_manager.py**). That will generate a `.env.local` file with a unique `SERVER_ID`.
4. Register the watchdog in the [Server Manager settings](http://localhost/manager/setting) with this ID and connection details.
5. Create a new game session and verify that the server connects to your watchdog.
6. View KPI results in the dashboard once simulations run.

👉 More technical details, usage guides, and testing tools are provided in the full README within the repository.

---

## 🧪 Summary

This project demonstrates:
- How to create and register external simulations for MSP Challenge
- How to structure a C# watchdog (or its Python port) for maritime simulations
- How to report KPI values per simulation cycle to the MSP server

For questions or contributions:
- 💬 [Open an issue](https://github.com/BredaUniversityResearch/MSPChallenge-Simulation-Example/issues)
- 🤝 [Read the contribution guidelines](https://community.mspchallenge.info/wiki/Community_Contribution)
- 📫 [Contact us](https://community.mspchallenge.info/wiki/Contact_us)

---

Let me know if you'd like this structured as a multi-file README set or exported to PDF!
