import dataclasses

from pydantic import ValidationError

import pytest

from assignment_2.state_machine import FSM, State


state_A = State("OFF", 0)
state_B = State("ON", 1)

states = [state_A, state_B]
inputs = ["TOGGLE"]
initial_state = state_A
accepting_states = [state_A]


@pytest.fixture
def transitions():
    return {
        (state_A, "TOGGLE"): state_B,
        (state_B, "TOGGLE"): state_A,
    }


class TestState:
    def test_state_initialization(self):
        state = State("OFF", 0)
        assert state.name == "OFF"
        assert state.value == 0

    def test_state_equality(self):
        state1 = State("OFF", 0)
        state2 = State("OFF", 0)
        assert state1 == state2

    def test_state_name_inequality(self):
        state1 = State("OFF", 0)
        state2 = State("ON", 0)
        assert state1 != state2

    def test_state_value_inequality(self):
        state1 = State("OFF", 0)
        state2 = State("OFF", 1)
        assert state1 != state2

    def test_state_immutable(self):
        state = State("OFF", 0)
        with pytest.raises(dataclasses.FrozenInstanceError):
            state.name = "ON"  # type: ignore

        with pytest.raises(dataclasses.FrozenInstanceError):
            state.value = 1  # type: ignore


class TestFSMInit:
    def test_FSM_happy_path(self, transitions):
        fsm = FSM(
            states,
            inputs,
            initial_state,
            accepting_states,
            transitions,
        )

        assert fsm.state is state_A
        assert fsm.is_accepting is True

    def test_FSM_invalid_initial_state(self, transitions):
        with pytest.raises(ValidationError):
            FSM(states, inputs, "A", initial_state, transitions)  # type: ignore

    def test_FSM_invalid_accepting_state(self, transitions):
        with pytest.raises(ValidationError):
            FSM(states, inputs, state_A, {"A"}, transitions)  # type: ignore

    def test_FSM_invalid_transition(self):
        transitions = {
            (state_A, "TOGGLE"): state_B,
            (state_B, "TOGGLE"): "INVALID_STATE",  # Invalid state
        }

        with pytest.raises(ValidationError):
            FSM(states, inputs, state_A, [state_A], transitions)  # type: ignore

    def test_FSM_invalid_transition_key(self):
        transitions = {
            (state_A, "TOGGLE"): state_B,
            (state_B, "INVALID_INPUT"): state_A,  # Invalid input
        }

        with pytest.raises(ValidationError):
            FSM(states, inputs, state_A, [state_A], transitions)  # type: ignore

    def test_FSM_invalid_transition_value(self):
        transitions = {
            (state_A, "TOGGLE"): state_B,
            (state_B, "TOGGLE"): "INVALID_STATE",  # Invalid state
        }

        with pytest.raises(ValidationError):
            FSM(states, inputs, state_A, [state_A], transitions)  # type: ignore


class TestToggleFSM:
    @pytest.fixture
    def fsm(self, transitions):
        return FSM(states, inputs, state_A, [state_A], transitions)

    def test_happy_path(self, fsm):
        assert fsm.state == state_A
        assert fsm.is_accepting is True

        fsm.input("TOGGLE")
        assert fsm.state == state_B
        assert fsm.is_accepting is False

        fsm.input("TOGGLE")
        assert fsm.state == state_A
        assert fsm.is_accepting is True

    def test_invalid_input(self, fsm):
        with pytest.raises(ValueError):
            fsm.input("INVALID_INPUT")

    def test_invalid_state(self, fsm):
        with pytest.raises(ValueError):
            fsm.state = "INVALID_STATE"


def test_missing_transition():
    fsm = FSM(states, inputs, state_A, [state_A], {})

    with pytest.raises(ValueError):
        fsm.input("TOGGLE")
