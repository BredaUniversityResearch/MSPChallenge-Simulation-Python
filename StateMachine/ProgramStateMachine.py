from transitions import Machine
from StateMachine.State import State
import asyncio

class ProgramStateMachine:
    def __init__(self):
        self._current_state = "AwaitingSetup"
        self._transitions = {
            ("AwaitingSetup", "SetupGame"): "Setup",
            ("Setup", "FinishedSetup"): "AwaitingNextMonth",
            ("AwaitingNextMonth", "MonthUpdated"): "Simulating",
            ("Simulating", "FinishedSimulation"): "Reporting",
            ("Reporting", "FinishedReport"): "AwaitingNextMonth",
            ("AwaitingNextMonth", "EndGame"): "AwaitingSetup"
        }

        # Callbacks
        self.on_state_exit = None
        self.on_state_enter = None
        self.on_setup_state_entered_event = None
        self.on_simulation_state_entered_event = None
        self.on_report_state_entered_event = None

    def get_current_state(self) -> str:
        return self._current_state

    def can_fire(self, trigger: str) -> bool:
        return (self._current_state, trigger) in self._transitions

    def fire(self, trigger: str):
        key = (self._current_state, trigger)
        if key not in self._transitions:
            print(f"[WARN] Cannot fire {trigger} from {self._current_state}")
            return

        new_state = self._transitions[key]
        print(f"Exiting {self._current_state} state")
        print(f"Transitioned from {self._current_state} to {new_state} via {trigger}")
        self._current_state = new_state
        print(f"Entering {new_state} state")
        print(f"Current state: {new_state}")

        # Call state-specific events
        if new_state == "Setup" and self.on_setup_state_entered_event:
            asyncio.create_task(self.on_setup_state_entered_event())
        elif new_state == "Simulating" and self.on_simulation_state_entered_event:
            asyncio.create_task(self.on_simulation_state_entered_event())
        elif new_state == "Reporting" and self.on_report_state_entered_event:
            asyncio.create_task(self.on_report_state_entered_event())

"""# Example usage:
sm = ProgramStateMachine()
sm.setup_game()  # Transitions to 'Setup'
print(sm.state)
"""