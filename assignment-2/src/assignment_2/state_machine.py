from collections.abc import Hashable
from typing import Any, Sequence

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class State:
    """
    Represents a state in a finite state machine (FSM). States are immutable.

    Attributes
    ----------
    name : str
        The name of the state.
    value : Any
        The value associated with the state. Can be used as a result for the FSM.
    """

    name: str
    value: Any


@dataclass
class FSM:
    """
    Generic base class for a finite state machine (FSM).

    This class provides the basic structure and functionality for an FSM,
    including state transitions, input processing, and accepting state checks.
    It can be subclassed for specific FSM implementations or used directly.
    Input types are checked at class initialization time via pydantic.

    Attributes
    ----------
    states : Sequence[State]
        FSM states.
    inputs: Sequence[Hashable]
        All valid inputs for the FSM.
    initial_state : State
        The initial State of the FSM.
    accepting_states : Sequence[State]
        Sequence of accepting States.
    transitions : dict[tuple[State, Hashable], State]
        Given the current FSM State and an input, maps (State, input) pairs to the next FSM State.

    Methods
    -------
    input(value: Hashable) -> None
        Process an input value and transition to the next state.
    state() -> State
        Get the current state of the FSM.
    state(new_state: State) -> None
        Set the current state of the FSM.
    is_accepting() -> bool
        Check if the current state is an accepting state.
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
        Transition to the next state based on the current state and input value.

        This method processes an input to the FSM, validates it against allowed inputs,
        finds the appropriate transition for the current state and input combination,
        and updates the FSM's state accordingly.

        Parameters
        ----------
        value : Hashable
            The input value to process. Must be one of the valid inputs defined for this FSM.

        Raises
        ------
        ValueError
            If the input value is not in the list of valid inputs, or
            if no transition is defined for the current state and input combination.
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
        """
        Sets the current state of the finite state machine.

        This method validates that the new state is one of the valid states
        defined for this FSM before updating the internal state.

        Parameters
        ----------
        new_state : State
            The new state to transition to.

        Raises
        ------
        ValueError
            If the provided state is not in the list of valid states for this FSM.
        """
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
