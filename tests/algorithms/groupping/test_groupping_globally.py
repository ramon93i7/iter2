import typing as tp
import hypothesis as hyp
from ... import _hypothesis_strategies as st

import random

from iter2.algo import (
    group_consecutive_values_with_same_computable_key,
    group_consecutive_values_by_key,

    group_and_fold_values_globally_with_same_computable_key,
    group_and_fold_values_globally_by_key,

    group_and_collect_values_globally_with_same_computable_key,
    group_and_collect_values_globally_by_key,
)


# ---

@hyp.given(
    prekey_value_items=st.lists(
        st.tuples(
            st.positive_integers(),
            st.positive_integers(),
        ),
        unique=True,
    ),
    random=st.randoms(),
)
def test_group_globally_functions_via_group_consecutive_of_sorted(
    prekey_value_items: tp.List[tp.Tuple[int, int]],
    random: random.Random,
):
    key_value_items = [
        (_is_odd(prekey), value)
        for prekey, value in prekey_value_items
    ]

    polyndromed_items: tp.List[tp.Tuple[int, int]] = (
        [*key_value_items, (-1, -1), *reversed(key_value_items)]
        if len(key_value_items) > 0
        else []
    )

    with_dupes: tp.List[tp.Tuple[int, int]] = []
    for (key, value) in polyndromed_items:
        for dx in range(random.randint(1, 5)):
            with_dupes.append((key, value + dx))

    with_dupes_sorted = sorted(
        with_dupes,
        key=_first,
    )

    # --- sort -> group consecutive ---

    sort_consec_comp = {
        (key, tuple(value for _, value in pairs))
        for key, pairs in group_consecutive_values_with_same_computable_key(
            with_dupes_sorted,
            key_fn=_first,
        )
    }

    sort_consec_given = {
        (key, tuple(values))
        for key, values in group_consecutive_values_by_key(with_dupes_sorted)
    }

    # --- generic folding in groups ---

    fold_comp: tp.Set[tp.Tuple[int, tp.Sequence[int]]] = set(
        (key, tuple(values))
        for key, values in (
            group_and_fold_values_globally_with_same_computable_key(
                with_dupes,
                key_fn=_first,
                initial_fn=list,  # generates `list[Unknown]` :(
                fold_fn=(lambda xs, pair: (
                    xs + [pair[1]]
                ))
            )
            .items()
        )
    )

    fold_given: tp.Set[tp.Tuple[int, tp.Sequence[int]]] = set(
        (key, tuple(values))
        for key, values in (
            group_and_fold_values_globally_by_key(
                with_dupes,
                initial_fn=list,
                fold_fn=(lambda xs, value: (
                    xs + [value]
                ))
            )
            .items()
        )
    )

    # --- collecting groups ---

    collect_comp = {
        (key, tuple(value for _, value in pairs))
        for key, pairs in (
            group_and_collect_values_globally_with_same_computable_key(
                with_dupes,
                key_fn=_first,
            )
            .items()
        )
    }

    collect_given = set(
        (key, tuple(values))
        for key, values in (
            group_and_collect_values_globally_by_key(with_dupes)
            .items()
        )
    )

    # ---

    assert (
        sort_consec_comp
        ==
        sort_consec_given
        ==
        fold_comp
        ==
        fold_given
        ==
        collect_comp
        ==
        collect_given
    )


# ---

def _first[Head, *Tail](tpl: tp.Tuple[Head, *Tail]) -> Head:
    return tpl[0]


def _is_odd(value) -> bool:
    return value % 2 == 1
