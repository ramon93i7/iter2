import typing as tp
import hypothesis as hyp
from .. import _hypothesis_strategies as st

import string

from iter2.op import call


# ---

@hyp.given(
    args=st.lists(
        st.one_of(
            st.booleans(),
            st.integers(),
        ),
    ),
    kwargs=st.original.dictionaries(
        st.original.text(
            string.ascii_letters
        ),
        st.one_of(
            st.booleans(),
            st.integers(),
        ),
        min_size=1,
        max_size=10,
    ),
)
def test__call_operator_is_partial_from_native_call(
    args: tp.Sequence[tp.Any],
    kwargs: tp.Mapping[str, tp.Any],
):
    def return_args(*args, **kwargs):
        return (args, kwargs)

    assert (
        return_args(*args, **kwargs)
        ==
        call(*args, **kwargs)(return_args)  # type: ignore - it's OK, checking `runtime` property
    )


# ---

def call_operator_type_checks():
    def func(a: int, b: str, *, c: bool, d: complex) -> float: ...

    tp.assert_type(
        list(map(call(1, 'b', c=True, d=0j), [func])),
        list[float],
    )
