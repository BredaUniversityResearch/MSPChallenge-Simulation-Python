# Runs on Python 3.12.9 (install this version first).
# activate the environment with (on windows): 
# .\.venv\Scripts\activate        

import os
import sys
import uuid
import asyncio
import json
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from Simulation.Exceptions import FatalException, TriggerResetException
from StateMachine.ProgramStateMachine import ProgramStateMachine
from Communication.MspClient import MspClient
from Extensions.TaskExtensions import register_exception_handler, continue_with_on_success, continue_with_on_success_result
from api import router





# Load environment variables from .env and .env.local
load_dotenv()  # loads .env
load_dotenv(".env.local")

# Get or create SERVER_ID
SERVER_ID = os.getenv("SERVER_ID")
if not SERVER_ID:
    SERVER_ID = str(uuid.uuid4())
    os.environ["SERVER_ID"] = SERVER_ID
    with open(".env.local", "a") as f:
        f.write(f"SERVER_ID={SERVER_ID}\n")
print(f"Server ID: {SERVER_ID}")

# Create FastAPI app (global)
app = FastAPI(title="MSP Challenge Simulation API in Python :)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# The ProgramManager class in Python
class ProgramManager:
    DEFAULT_TICK_RATE_MS = 1000
    DEFAULT_MONTH = -1
    POLL_TOKEN_FREQUENCY_SEC = 60
    REFRESH_API_ACCESS_TOKEN_FREQUENCY_SEC = 900
    setup_accepted = False


    def __init__(self, args: List[str]):
        self.m_tick_rate_ms: int = ProgramManager.DEFAULT_TICK_RATE_MS
        self.m_args: List[str] = args
        self.m_current_month: int = ProgramManager.DEFAULT_MONTH
        self.m_target_month: int = ProgramManager.DEFAULT_MONTH
        self.m_current_game_state: Optional[str] = None  # e.g. "Setup", etc.
        self.m_target_game_state: Optional[str] = "Setup"
        self.m_last_tick_time: datetime = datetime.now()
        self.m_setup_accepted: bool = False
        self.m_game_session_token: Optional[str] = None
        self.m_game_session_info: Optional[Any] = None  # Replace with your GameSessionInfo
        self.m_simulation_definitions: Optional[List[Any]] = None  # Replace with list of SimulationDefinition

        self.m_program_state_machine: Optional[ProgramStateMachine] = None
        self.m_msp_client: Optional[MspClient] = None

        self.m_poll_token_time_left_sec: float = ProgramManager.POLL_TOKEN_FREQUENCY_SEC
        self.m_refresh_api_access_token_time_left_sec: float = ProgramManager.REFRESH_API_ACCESS_TOKEN_FREQUENCY_SEC

        # Event callbacks as lists of callables
        self.on_simulation_definitions_event: List[Callable[[Any], List[Any]]] = []
        self.on_question_accept_setup_event: List[Callable[[Any], bool]] = []
        self.on_setup_event: List[Callable[[], asyncio.Future]] = []
        self.on_simulation_state_entered_event: List[Callable[[int], asyncio.Future]] = []
        self.on_report_state_entered_event: List[Callable[[], asyncio.Future]] = []
        self.on_tick_event: List[Callable[[float], Any]] = []

        # Register exception handlers (stub)
        self.register_exception_handler(FatalException, lambda e: (_ for _ in ()).throw(e))
        self.register_exception_handler(TriggerResetException, lambda e: self.reset())

        # Add tick event handlers
        self.on_tick_event.append(self.validate_watchdog_token)
        self.on_tick_event.append(self.refresh_api_access_token)

        # Helper callback to update tokens after a successful HTTP POST
    def _update_tokens(self, task: asyncio.Future) -> None:
        result = task.result()
        self.m_msp_client.apiAccessToken = result.get("api_access_token")
        self.m_msp_client.apiRefreshToken = result.get("api_refresh_token")
        print("Api access token refreshed.")

    async def refresh_api_access_token(self, delta_time_sec: float):
        if self.m_msp_client is None:
            return
        self.m_refresh_api_access_token_time_left_sec -= delta_time_sec
        if self.m_refresh_api_access_token_time_left_sec > 0:
            return
        while self.m_refresh_api_access_token_time_left_sec < 0:
            self.m_refresh_api_access_token_time_left_sec += ProgramManager.REFRESH_API_ACCESS_TOKEN_FREQUENCY_SEC
        try:
            task = asyncio.create_task(
                self.m_msp_client.http_post(
                    "/api/User/RequestToken",
                    {"api_refresh_token": self.m_msp_client.apiRefreshToken}
                )
            )
            # Use the TaskExtensions helper to chain continuation on success
            await continue_with_on_success(
                task,
                self._update_tokens,
                lambda e: print(f"Could not refresh api access token: {str(e)}")
            )
        except Exception as e:
            print(f"Could not refresh api access token: {str(e)}")
            self.reset()

    # Helper callback to check watchdog token after successful HTTP POST
    def _check_watchdog_token(self, task: asyncio.Future) -> None:
        token_obj = task.result()  # Expected to be a dict with "watchdog_token"
        if self.m_game_session_token != token_obj.get("watchdog_token"):
            print("Watchdog token changed.")
            self.reset()

    async def validate_watchdog_token(self, delta_time_sec: float):
        if self.m_game_session_token is None or self.m_msp_client is None:
            return
        self.m_poll_token_time_left_sec -= delta_time_sec
        if self.m_poll_token_time_left_sec > 0:
            return
        while self.m_poll_token_time_left_sec < 0:
            self.m_poll_token_time_left_sec += ProgramManager.POLL_TOKEN_FREQUENCY_SEC
        try:
            task = asyncio.create_task(
                self.m_msp_client.http_post("/api/Simulation/GetWatchdogTokenForServer", {})
            )
            await continue_with_on_success(
                task,
                self._check_watchdog_token,
                lambda e: print(f"Could not retrieve watchdog token: {str(e)}")
            )
        except Exception as e:
            print(f"Could not retrieve watchdog token: {str(e)}")
            self.reset()


    

    def reset(self):
        print("Resetting.")
        self.m_program_state_machine = None
        self.m_setup_accepted = False
        self.m_game_session_token = None
        self.m_msp_client = None
        self.m_simulation_definitions = None
        self.m_current_game_state = None

    async def get_simulation_definitions(self):
        if not self.on_simulation_definitions_event or self.m_game_session_info is None:
            return
        # For demo purposes, call the first subscribed handler
        self.m_simulation_definitions = self.on_simulation_definitions_event[0](self.m_game_session_info)
        data = {sim_def["Name"]: sim_def["Version"] for sim_def in self.m_simulation_definitions}
        await self.get_msp_client().http_post("/api/Simulation/Upsert", data, headers={"X-Remove-Previous": "true"})

    async def on_setup_state_entered(self):
        client = self.get_msp_client()
        # Set default error handler on client if needed
        await self.get_simulation_definitions()
        if self.on_setup_event:
            await asyncio.gather(*(handler() for handler in self.on_setup_event))
        if self.m_program_state_machine:
            self.m_program_state_machine.fire("FinishedSetup")

    async def on_simulation_state_entered(self):
        if self.on_simulation_state_entered_event:
            await asyncio.gather(*(handler(self.m_current_month) for handler in self.on_simulation_state_entered_event))
        if self.m_program_state_machine:
            self.m_program_state_machine.fire("FinishedSimulation")

    async def on_report_state_entered(self):
        if self.on_report_state_entered_event:
            results = await asyncio.gather(*(handler() for handler in self.on_report_state_entered_event))
            # Flatten KPI lists (assuming each handler returns a list)
            kpis = [item for sublist in results for item in sublist]
            await self.submit_kpis(kpis)
        if self.m_program_state_machine:
            self.m_program_state_machine.fire("FinishedReport")

    async def submit_kpis(self, kpis: List[Dict[str, Any]]):
        if not kpis:
            return
        data = {"kpiValues": json.dumps(kpis)}
        await self.get_msp_client().http_post(
            "/api/kpi/BatchPost", data, headers={"x-notify-monthly-simulation-finished": "true"}
        )

    def set_tick_rate_ms(self, tick_rate_ms: int):
        self.m_tick_rate_ms = tick_rate_ms

    def get_msp_client(self) -> MspClient:
        if self.m_msp_client is None:
            raise Exception("MSP client is not initialized. The client is available after the OnSetupEvent event.")
        return self.m_msp_client
    
    def extract_token(self, token_obj):
        return token_obj.get("token") if isinstance(token_obj, dict) else token_obj.token

    def init(self, server_id: str, game_session_api: str, api_access_token: Any, api_access_renew_token: Any):
        # Assume api_access_token and api_access_renew_token are already parsed objects/dicts with a "token" key
        if self.m_msp_client is None:
            self.m_msp_client = MspClient(server_id, game_session_api, self.extract_token(api_access_token), self.extract_token(api_access_renew_token))
        self.m_msp_client.apiAccessToken = api_access_token.token
        self.m_msp_client.apiRefreshToken = api_access_renew_token.token

        if self.m_program_state_machine is not None:
            return
        self.m_program_state_machine = ProgramStateMachine()
        # Subscribe to state machine events (using our async methods)
        self.m_program_state_machine.on_setup_state_entered_event = self.on_setup_state_entered
        self.m_program_state_machine.on_simulation_state_entered_event = self.on_simulation_state_entered
        self.m_program_state_machine.on_report_state_entered_event = self.on_report_state_entered

    def is_setup_accepted(self, game_session_info: Any) -> bool:
        self.m_game_session_info = game_session_info
        if not self.on_question_accept_setup_event:
            return True
        return all(handler(game_session_info) for handler in self.on_question_accept_setup_event)
    
    def register_exception_handler(self, ex_type: type, handler: Callable[[Exception], None]) -> None:
        # Just delegate to the imported function.
        from Extensions.TaskExtensions import register_exception_handler as global_register
        global_register(ex_type, handler)


    async def tick(self):
        current_tick_time = datetime.now()
        delta_time = (current_tick_time - self.m_last_tick_time).total_seconds()
        self.m_last_tick_time = current_tick_time

        # Call all tick event handlers
        for handler in self.on_tick_event:
            result = handler(delta_time)
            if asyncio.iscoroutine(result):
                await result

        # Debug log
        if self.m_program_state_machine:
            print(f"[DEBUG] FSM tick — Current state: {self.m_program_state_machine.get_current_state()}")

        # ---------------------------
        # Setup transition
        # ---------------------------
        if self.m_target_game_state == "Setup" and self.m_current_game_state != "Setup":
            self.m_current_month = ProgramManager.DEFAULT_MONTH
            self.m_current_game_state = "Setup"
            if self.m_program_state_machine and self.m_program_state_machine.can_fire("SetupGame"):
                self.m_program_state_machine.fire("SetupGame")
            else:
                print(f"[WARN] Cannot fire SetupGame from current state: {self.m_program_state_machine.get_current_state() if self.m_program_state_machine else 'None'}")
            return  # Stop processing until next tick

        if self.m_target_game_state == "Setup":
            return  # Setup is blocking; wait for transition to complete

        # ---------------------------
        # FSM must be in AwaitingNextMonth to proceed
        # ---------------------------
        if not self.m_program_state_machine or self.m_program_state_machine.get_current_state() != "AwaitingNextMonth":
            return

        # ---------------------------
        # End Game transition
        # ---------------------------
        if self.m_target_game_state == "End" and self.m_current_game_state != "End":
            self.m_current_game_state = "End"
            if self.m_program_state_machine.can_fire("EndGame"):
                self.m_program_state_machine.fire("EndGame")
            else:
                print(f"[WARN] Cannot fire EndGame from current state: {self.m_program_state_machine.get_current_state()}")
            return

        if self.m_target_game_state == "End":
            return  # End blocks further action

        # ---------------------------
        # Advance month
        # ---------------------------
        if self.m_target_month <= self.m_current_month:
            return  # Already up to date

        self.m_current_month += 1
        print(f"Month updated to {self.m_current_month}")
        if self.m_program_state_machine and self.m_program_state_machine.can_fire("MonthUpdated"):
            self.m_program_state_machine.fire("MonthUpdated")
        else:
            print(f"[WARN] Cannot fire MonthUpdated from current state: {self.m_program_state_machine.get_current_state() if self.m_program_state_machine else 'None'}")

    async def run(self):
        while True:
            await self.tick()
            await asyncio.sleep(self.m_tick_rate_ms / 1000)

    def handle_dot_file(self, dotfile: Optional[str]):
        if not dotfile or not self.m_program_state_machine:
            return
        self.m_program_state_machine.write_to_dot_file(dotfile)

    def run_internal(self, port: Optional[int] = None, https_redirection: Optional[bool] = None):
        # Build FastAPI app configuration (environment already loaded)
        server_id = os.getenv("SERVER_ID")
        if not server_id:
            print("SERVER_ID environment variable is not set. Generating a new one.")
            server_id = str(uuid.uuid4())
            os.environ["SERVER_ID"] = server_id
            with open(".env.local", "a") as f:
                f.write(f"SERVER_ID={server_id}\n")
        #print(f"Server ID in run_internal: {server_id}")

        # Add services to FastAPI
        from fastapi import Body, Response
        from fastapi.responses import JSONResponse

        

        # Schedule the tick loop
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.create_task(self.run())

        # Start FastAPI via Uvicorn
        import uvicorn
        uvicorn.run("program_manager:app", host="0.0.0.0", port=port or 5026, reload=True)

    def validate_request_data(self, api_access_token: Optional[Dict[str, Any]], api_access_renew_token: Optional[Dict[str, Any]], request_body: Dict[str, Any], new_game_state: str):
        if not api_access_token or not api_access_renew_token:
            raise Exception("Invalid JSON format for API tokens")
        # For simplicity, assume new_game_state is valid.
        if new_game_state == "Setup":
            if not request_body.get("game_session_info"):
                raise Exception("Missing setup game session info")
            self.m_setup_accepted = self.is_setup_accepted(request_body.get("game_session_info"))
            self.m_game_session_token = request_body.get("game_session_token")

    def validate_request_allowed(self, game_session_token: str, required_simulations: Optional[Dict[str, str]] = None):
        if not self.m_setup_accepted:
            raise Exception("Please start the setup first.")
        if self.m_game_session_token != game_session_token:
            raise Exception("Invalid game session token")
        if required_simulations is None or self.m_simulation_definitions is None:
            return
        for sim_def in self.m_simulation_definitions:
            if sim_def["Name"] not in required_simulations:
                raise Exception(f"Required simulation {sim_def['Name']} is not available")
            # Version comparison omitted for brevity.

# Instantiate and store ProgramManager globally in the FastAPI app state
program_manager = ProgramManager(sys.argv[1:])
app.state.program_manager = program_manager
app.include_router(router)

if __name__ == "__main__":
    # For simplicity, pass command-line arguments excluding script name.
    program_manager.run_internal(port=5026, https_redirection=False)
