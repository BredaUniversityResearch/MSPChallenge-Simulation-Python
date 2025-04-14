Runs on Python 3.12.9 (install this version first).
Activate the environment with (on windows): 
     .\.venv\Scripts\activate      


The example application involves event-driven simulation, REST API handling, asynchronous tasks, and a state machine. Therefore, the following Python equivalent stack is chosen:

📌 C# Features                      →       Python Equivalents
    
    ASP.NET Core (Web API)	                FastAPI (for REST APIs)
    State Machine (ProgramStateMachine)	    transitions library
    Async Tasks (Task, ContinueWith)	    asyncio, concurrent.futures
    HTTP Requests (HttpPost)	            httpx, requests
    Events (OnSimulationDefinitionsEvent)	Python callbacks, asyncio.Event
    Json Serialization (Newtonsoft.Json)	pydantic, json
    Dependency Injection (builder.Services)	dependency_injector
    Timers (Timer(Tick, ...))	            asyncio loop


