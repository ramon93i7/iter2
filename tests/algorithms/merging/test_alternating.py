import typing as tp
import hypothesis as hyp
from ... import _hypothesis_strategies as st
from .._failing_iterator import FailingIterator

from iter2.algo import (
    iterate_alternating_with_item,
    iterate_alternating,
)


# ---

def test_iterate_alternating_are_trully_lazy():
    iterate_alternating_with_item(
        FailingIterator(),
        item=None,
    )
    iterate_alternating(
        FailingIterator(),
        FailingIterator(),
    )


# ---

@hyp.given(
    items=st.lists(
        st.integers(),
    ),
)
def test_iterate_alternating_with_item(
    items: tp.List[int],
):
    sentinel = object()
    for idx, value in enumerate(iterate_alternating_with_item(items, item=sentinel)):
        q, r = divmod(idx, 2)
        if r == 0:
            assert value == items[q]
        else:
            assert value is sentinel


# ---

@st.original.composite
def _answer_and_original_sequences_for_alternating_iteration(
    draw: st.original.DrawFn,
    *,
    min_size: int = 1,
    max_size: int | None = None,
) -> tp.Tuple[tp.List[int], tp.List[tp.List[int]]]:
    # --- answer ---
    items = draw(st.lists(
        st.integers(),
        min_size=min_size,
        max_size=max_size,
    ))
    items_len = len(items)

    # --- number of sequences to split to ---
    number_of_seqs = draw(st.integers(
        min_value=1,
        max_value=len(items),
    ))

    # --- distributing extra credits ---
    random = draw(st.randoms())
    seq_credits = [0 for _ in range(number_of_seqs)]
    for _ in range(items_len):
        seq_credits[random.randint(0, number_of_seqs - 1)] += 1

    # --- collecting final sequences ---
    seqs = [[] for _ in range(number_of_seqs)]
    cur_seq = 0
    next_seq = lambda idx: (idx + 1) % number_of_seqs
    for item in items:
        while seq_credits[cur_seq] == 0:
            cur_seq = next_seq(cur_seq)
        # ---
        seq_credits[cur_seq] -= 1
        seqs[cur_seq].append(item)
        # ---
        cur_seq = next_seq(cur_seq)

    return items, seqs


@hyp.given(
    answer_with_original_sequences=_answer_and_original_sequences_for_alternating_iteration()
)
def test_iterate_alternating(
    answer_with_original_sequences: tp.Tuple[tp.List[int], tp.List[tp.List[int]]],
):
    answer, seqs = answer_with_original_sequences
    assert (
        answer
        ==
        list(iterate_alternating(*seqs))
    )
