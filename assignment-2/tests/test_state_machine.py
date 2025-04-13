from enum import Enum

from assignment_2.state_machine import FSM


class TestFSM:
    def test_2_states_1_event(self):
        class States(Enum):
            A = "A"
            B = "B"

            def on_enter(self):
                print(f"Entering state: {self.name}")

        class Inputs(Enum):
            TOGGLE = "TOGGLE"

        transitions = {
            (States.A, Inputs.TOGGLE): States.B,
            (States.B, Inputs.TOGGLE): States.A,
        }

        fsm: FSM[States, Inputs] = FSM(States, Inputs, transitions, States.A, [States.A])
        assert fsm.state == States.A
        assert fsm.is_accepting is True

        fsm.input(Inputs.TOGGLE)
        assert fsm.state == States.B
        assert fsm.is_accepting is False

        fsm.input(Inputs.TOGGLE)
        assert fsm.state == States.A
        assert fsm.is_accepting is True

    
