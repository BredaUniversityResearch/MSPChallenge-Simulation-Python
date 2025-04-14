from enum import Enum

class State(str, Enum):
    AwaitingSetup = "AwaitingSetup"         # await setup game state from MSP server
    Setup = "Setup"                         # register kpi's with MSP API
    AwaitingNextMonth = "AwaitingNextMonth" # await next month trigger from MSP server
    Simulation = "Simulation"               # calculate kpi's for current month
    Report = "Report"                       # submit kpi's to MSP API

