from enum import Enum

class EGameState(str, Enum):
    setup = "Setup"
    play = "Play"
    simulation = "Simulation"
    fastforward = "Fastforward"
    pause = "Pause"
    end = "End"
