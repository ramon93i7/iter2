import hypothesis.strategies as st

import sys


# ---

original = st

one_of = st.one_of

booleans = st.booleans
none = st.none
randoms = st.randoms


# --- Optional ---

def optionals(strategy):
    return st.one_of(st.none(), strategy)


# --- Numbers ---

integers = st.integers
floats = st.floats


def naturals(
    min_value: int = 0,
    max_value: int | None = None,
):
    if (
        min_value < 0
        or
        max_value is not None and max_value < 0
    ):
        raise ValueError(f'Naturals must be >= 0: {min_value = }, {max_value = }')

    return (
        integers(
            min_value=min_value,
            max_value=max_value,
        )
    )


def positive_integers(
    min_value: int = 1,
    max_value: int | None = None,
):
    if (
        min_value < 1
        or
        max_value is not None and max_value < 1
    ):
        raise ValueError(f'Positive integers must be >= 1: {min_value = }, {max_value = }')

    return (
        integers(
            min_value=min_value,
            max_value=max_value,
        )
    )


# ---

def supported_sizes(
    min_value: int = 0,
    max_value: int = sys.maxsize,
):
    if (
        min_value < 0
        or
        max_value is not None and max_value > sys.maxsize
    ):
        raise ValueError(f'Supported sizes are integers in [0, sys.maxsize]: {min_value = }, {max_value = }')

    return (
        integers(
            min_value=min_value,
            max_value=max_value,
        )
    )


# --- Collections ---

iterables = st.iterables

tuples = st.tuples
lists = st.lists
sets = st.sets
