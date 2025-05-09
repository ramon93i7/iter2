import typing as tp
import hypothesis as hyp

from .. import _hypothesis_strategies as st

from iter2.box import Box2


# ---

@hyp.given(
    values=st.tuples(st.integers()),
)
def test_box_is_mappable(
    values: tp.Tuple[int, ...],
):
    assert (
        str(values)
        ==
        Box2(values).map(str).value
    )

    assert (
        str(values)
        ==
        Box2(values).map_unpacked(lambda *args: str(args)).value
    )


@hyp.given(
    values=st.tuples(st.integers()),
)
def test_box_is_filterable(
    values: tp.Tuple[int, ...],
):
    sum_is_odd = lambda values: sum(values) % 2 == 1

    assert (
        sum_is_odd(values)
        ==
        Box2(values).filter(sum_is_odd).is_some()
        ==
        Box2(values).filter_unpacked(lambda *args: sum_is_odd(args)).is_some()
    )


@hyp.given(
    value=st.one_of(
        st.integers(min_value=-5, max_value=5),
        st.floats(min_value=0.0, max_value=1.0),
    ),
)
def test_box_is_filterable_by_type(
    value: int | float,
):
    def is_int(obj) -> tp.TypeGuard[int]:
        return isinstance(obj, int)

    assert (
        is_int(value)
        ==
        Box2(value).filter_by_type(int).is_some()
        ==
        Box2(value).filter_by_type_predicate(is_int).is_some()
    )
