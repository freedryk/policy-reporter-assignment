from enum import Enum
from typing import Any, Generic, TypeVar


S = TypeVar("S", bound=Enum)
I = TypeVar("I", bound=Enum)


class FSM(Generic[S, I]):
    """
    Generic base class for a finite state machine (FSM).
    """

    def __init__(
        self,
        states: type[S],
        inputs: type[I],
        transitions: dict[tuple[S, I], S],
        initial_state: S,
        accepting_states: list[S],
    ) -> None:
        self._states = states
        self._inputs = inputs

        assert all(isinstance(trans, tuple) for trans in transitions.keys()), (
            f"Invalid transition: {transitions}. Expected all keys to be tuples of type ({states}, {inputs})"
        )

        assert all(isinstance(state, states) for state in transitions.values()), (
            f"Invalid transition: {transitions}. Expected all values to be of type {states}"
        )
        self._transitions = transitions

        assert initial_state in states, f"Invalid initial state: {initial_state}"
        self._state = initial_state

        assert all(state in states for state in accepting_states), (
            f"Invalid accepting states: {accepting_states}"
        )
        self._accepting_states = (
            accepting_states if accepting_states is not None else list(states)
        )

    def input(self, value: Any) -> None:
        """
        Transition to the next state based on the current state and event.
        """
        # if the input is not in the inputs enum, raise an error
        input_ = self._inputs(value)
        self.state = self._transitions[(self.state, input_)]

    @property
    def state(self) -> S:
        return self._state

    @state.setter
    def state(self, new_state: S) -> None:
        assert isinstance(new_state, self._states), (
            f"Invalid state: {new_state}. Expected type: {self._states}"
        )
        self._state = new_state

    @property
    def is_accepting(self) -> bool:
        """
        Check if the current state is an accepting state.
        """
        return self._state in self._accepting_states
