from collections.abc import Hashable
from typing import Any, Sequence

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class State:
    """
    Base class for all states.
    """

    name: str
    value: Any


@dataclass
class FSM:
    """
    Generic base class for a finite state machine (FSM).
    """

    states: Sequence[State]
    inputs: Sequence[Hashable]
    initial_state: State
    accepting_states: Sequence[State]
    transitions: dict[tuple[State, Hashable], State]

    def __post_init__(self) -> None:
        for trans in self.transitions:
            assert trans[1] in self.inputs, (
                f"transitions input {trans[1]} not in inputs {self.inputs}"
            )

        self._state = self.initial_state

    def input(self, value: Hashable) -> None:
        """
        Transition to the next state based on the current state and event.
        """
        if value not in self.inputs:
            raise ValueError(f"Invalid input: {value}. Expected one of: {self.inputs}")

        transition = self.transitions.get((self.state, value))
        if transition is None:
            raise ValueError(
                f"No transition defined for state {self.state} with input {value}"
            )
        self.state = self.transitions[(self.state, value)]

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, new_state: State) -> None:
        if new_state not in self.states:
            raise ValueError(
                f"Invalid state: {new_state}. Expected type: {self.states}"
            )
        self._state = new_state

    @property
    def is_accepting(self) -> bool:
        """
        Check if the current state is an accepting state.
        """
        return self._state in self.accepting_states
