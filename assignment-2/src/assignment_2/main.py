from enum import Enum, IntEnum

from assignment_2.state_machine import FSM


class Inputs(Enum):
    ZERO = "0"
    ONE = "1"


class States(IntEnum):
    S0 = 0
    S1 = 1
    S2 = 2


class BDT(FSM[States, Inputs]):
    _transitions = {
        (States.S0, Inputs.ZERO): States.S0,
        (States.S0, Inputs.ONE): States.S1,
        (States.S1, Inputs.ZERO): States.S2,
        (States.S1, Inputs.ONE): States.S0,
        (States.S2, Inputs.ZERO): States.S1,
        (States.S2, Inputs.ONE): States.S2,
    }

    def __init__(self):
        super().__init__(
            States,
            Inputs,
            self._transitions,
            States.S0,
            [States.S0, States.S1, States.S2],
        )


def main():
    fsm = BDT()
    binary_string = "1110"  # Example binary string

    for c in binary_string:
        fsm.input(c)

    print(f"Result: {fsm.state}")
