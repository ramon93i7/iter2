import typing as tp
import hypothesis as hyp
from ... import _hypothesis_strategies as st
from .._failing_iterator import FailingIterator

import pytest

from iter2.algo import (
    slice_items,
    drop_first_items_and_iterate_rest,
    iterate_through_first_items,
    iterate_with_fixed_step,

    iterate_alternating,
)


# ---

@hyp.given(
    N=st.supported_sizes(
        min_value=1,
    ),
)
def test_fix_size_slicing_functions_trully_lazy(
    N: int,
):
    slice_items(
        FailingIterator(),
        start_from_idx=N, step_size=N, end_before_idx=N,
    )
    drop_first_items_and_iterate_rest(
        FailingIterator(),
        count=N,
    )
    iterate_through_first_items(
        FailingIterator(),
        count=N,
    )
    iterate_with_fixed_step(
        FailingIterator(),
        step=N,
    )


# ---

@hyp.given(
    items=st.lists(st.integers(), min_size=10, max_size=20),
    start=st.integers(min_value=1, max_value=5),
    step=st.integers(min_value=1, max_value=3),
    end=st.integers(min_value=1, max_value=10),
)
def test_slice_items_is_equivalent_to_list_slicing_and_composition_of_other_fixed_size_iterations(
    items: tp.List[int],
    start: int,
    step: int,
    end: int,
):
    sliced = list(
        slice_items(
            iter(items),
            start_from_idx=start,
            step_size=step,
            end_before_idx=end,
        )
    )

    assert sliced == items[start:end:step]

    if start < end:
        assert (
            sliced
            ==
            list(
                iterate_with_fixed_step(
                    iterate_through_first_items(
                        drop_first_items_and_iterate_rest(
                            iter(items),
                            count=start,
                        ),
                        count=end - start,
                    ),
                    step=step,
                )
            )
        )


# ---

@hyp.given(
    first_items=st.lists(st.integers(), min_size=1),
    last_items=st.lists(st.integers()),
)
def test_iterate_and_drop_N_first_items_are_correct(
    first_items: tp.List[int],
    last_items: tp.List[int],
):
    sequence = [*first_items, *last_items]

    assert (
        first_items
        ==
        list(iterate_through_first_items(
            iter(sequence),
            count=len(first_items),
        ))
    )

    assert (
        last_items
        ==
        list(drop_first_items_and_iterate_rest(
            iter(sequence),
            count=len(first_items),
        ))
    )


# ---

@hyp.given(
    non_positive_int=st.integers(min_value=-5, max_value=0)
)
def test_fixed_size_iterations_fail_on_non_positive_argument(
    non_positive_int: int
):
    with pytest.raises(ValueError):
        iterate_through_first_items(
            iter(()),
            count=non_positive_int,
        )

    with pytest.raises(ValueError):
        drop_first_items_and_iterate_rest(
            iter(()),
            count=non_positive_int,
        )

    with pytest.raises(ValueError):
        iterate_with_fixed_step(
            iter(()),
            step=non_positive_int,
        )


@hyp.given(
    first_sequence=st.lists(st.integers(), min_size=1),
    second_sequence=st.lists(st.integers(), min_size=1),
    third_sequence=st.lists(st.integers(), min_size=1),
)
def test_iterate_with_fixed_step_is_inverse_for_alternating(
    first_sequence: tp.List[int],
    second_sequence: tp.List[int],
    third_sequence: tp.List[int],
):
    common_len = min(
        len(first_sequence),
        len(second_sequence),
        len(third_sequence),
    )

    first = first_sequence[:common_len]
    second = second_sequence[:common_len]
    third = third_sequence[:common_len]

    alternated = list(iterate_alternating(first, second, third))

    # ---

    it = iter(alternated)
    assert (
        first
        ==
        list(iterate_with_fixed_step(
            it,
            step=3,
        ))
    )

    # ---

    it = iter(alternated)
    next(it, None)  # drop 1st
    assert (
        second
        ==
        list(iterate_with_fixed_step(
            it,
            step=3,
        ))
    )

    # ---

    it = iter(alternated)
    next(it, None)  # drop 1st
    next(it, None)  # drop 2nd
    assert (
        third
        ==
        list(iterate_with_fixed_step(
            it,
            step=3,
        ))
    )

    # ---

    assert (
        list(iterate_with_fixed_step(
            iter(alternated),
            step=6,
        ))
        ==
        list(iterate_with_fixed_step(
            iter(first),
            step=2,
        ))
    )
