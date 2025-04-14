from fastapi import APIRouter, HTTPException, Request, Body
from typing import Dict, Any
from Api.UpdateStateRequest import UpdateStateRequest
from fastapi import Body
import json  
from Api.UpdateStateRequest import UpdateStateRequest
from StateMachine.ProgramStateMachine import ProgramStateMachine
import os
from Api.SetMonthRequest import SetMonthRequest  


router = APIRouter()

@router.api_route("/Watchdog/Ping", methods=["GET", "POST"], name="Ping")
async def ping(request: Request):
    program = request.app.state.program_manager
    return {
        "success": "1",
        "message": "Pong",
        "game_session_token": program.m_game_session_token  # <- critical!
    }


@router.post("/Watchdog/SetMonth", name="SetMonth")
async def set_month_endpoint(request: Request, body: Dict[str, Any] = Body(...)):
    program = request.app.state.program_manager
    token = body.get("game_session_token")

    if program.m_game_session_token is None or program.m_game_session_token != token:
        raise HTTPException(status_code=405, detail="Invalid game session token")

    program.m_target_month = body.get("month", program.DEFAULT_MONTH)

    # ✅ Also print current game state
    print(f"[DEBUG] Game state: {program.m_target_game_state}, target month set to {program.m_target_month}")

    return {
        "success": "1",
        "message": "Month set successfully"
    }





@router.api_route("/Watchdog/UpdateState", methods=["POST"], name="UpdateState")
async def update_state_endpoint(
    request: Request,
    update_request: UpdateStateRequest = Body(...)
):
    program = request.app.state.program_manager

    if program.m_game_session_token is None:
        if update_request.game_state.lower() == "setup":
            program.m_game_session_token = update_request.game_session_token
            program.setup_accepted = True
            print(f"[DEBUG] Setup accepted. Token initialized: {program.m_game_session_token}")

            # ✅ Init the MSP client and FSM explicitly
            api_access_token = update_request.api_access_token
            api_access_renew_token = update_request.api_access_renew_token
            game_session_api = update_request.game_session_api

            if isinstance(api_access_token, str):
                api_access_token = json.loads(api_access_token)
            if isinstance(api_access_renew_token, str):
                api_access_renew_token = json.loads(api_access_renew_token)

            program.init(
                server_id=os.getenv("SERVER_ID", "default-server-id"),
                game_session_api=game_session_api,
                api_access_token=api_access_token,
                api_access_renew_token=api_access_renew_token,
            )

            # ✅ FSM setup (only if it wasn’t created inside `init`)
            if not program.m_program_state_machine:
                program.m_program_state_machine = ProgramStateMachine()
                program.m_program_state_machine.on_setup_state_entered_event = program.on_setup_state_entered
                program.m_program_state_machine.on_simulation_state_entered_event = program.on_simulation_state_entered
                program.m_program_state_machine.on_report_state_entered_event = program.on_report_state_entered

            if program.m_program_state_machine.can_fire("SetupGame"):
                program.m_program_state_machine.fire("SetupGame")

        else:
            raise HTTPException(status_code=405, detail="Setup must be called first.")

    elif program.m_game_session_token != update_request.game_session_token:
        raise HTTPException(status_code=405, detail="Invalid game session token")

    if not program.setup_accepted:
        raise HTTPException(status_code=405, detail="Setup not yet accepted.")

    program.m_target_game_state = update_request.game_state
    program.m_target_month = update_request.month
    print(f"[DEBUG] Game state set to {program.m_target_game_state}, month: {program.m_target_month}")

    return {"success": "1", "message": "State updated successfully"}
