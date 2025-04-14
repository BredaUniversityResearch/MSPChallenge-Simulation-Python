from enum import Enum

class Trigger(str, Enum):
    MonthUpdated = "MonthUpdated"               # month updated trigger from MSP server
    EndGame = "EndGame"                         # end game trigger from MSP server, stop simulations
    SetupGame = "SetupGame"                     # setup game trigger from MSP server
    FinishedSetup = "FinishedSetup"              
    FinishedSimulation = "FinishedSimulation"    
    FinishedReport = "FinishedReport"            

