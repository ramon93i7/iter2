
from iter2.op import is_instance_of


# ---

def test__is_instance_of_operator():
    x: int = 1
    s: str = 's'
    xs = [x, s]

    assert is_instance_of(x, int)
    assert is_instance_of(s, str)
    assert (
        [x] == list(filter(is_instance_of(int), xs))
        and
        [s] == list(filter(is_instance_of(str), xs))
    )
