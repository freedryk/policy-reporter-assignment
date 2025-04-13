from assignment_2.state_machine import FSM, State


class ModThreeFSM(FSM):
    """
    Finite State Machine (FSM) that calculate the modulo 3 of a binary string.
    """

    inputs = ["0", "1"]

    S0 = State("S0", 0)
    S1 = State("S1", 1)
    S2 = State("S2", 2)
    states = [S0, S1, S2]

    transitions = {
        (S0, "0"): S0,
        (S0, "1"): S1,
        (S1, "0"): S2,
        (S1, "1"): S0,
        (S2, "0"): S1,
        (S2, "1"): S2,
    }

    def __init__(self):
        super().__init__(
            self.states,
            self.inputs,
            self.S0,
            self.states,
            self.transitions,
        )


def main():
    binary_strings = ["1101", "1110", "1111"]  # Example binary strings

    for bs in binary_strings:
        fsm = ModThreeFSM()
        for c in bs:
            fsm.input(c)

        if fsm.is_accepting:
            print(f"Input: {bs} Output: {fsm.state.value}")
