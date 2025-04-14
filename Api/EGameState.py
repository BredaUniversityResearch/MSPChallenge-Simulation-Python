from enum import Enum

class EGameState(str, Enum):
    Setup = "Setup"
    Play = "Play"
    Simulation = "Simulation"
    Fastforward = "Fastforward"
    Pause = "Pause"
    End = "End"
