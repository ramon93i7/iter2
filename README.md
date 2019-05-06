# iter2

This library provides implementation of 
[rich-iterator](http://code.activestate.com/recipes/498272-rich-iterator-wrapper/) 
concept, inspired by 
[Rust's std::iter::Iterator](https://doc.rust-lang.org/std/iter/trait.Iterator.html), 
[Java's Stream](https://docs.oracle.com/javase/8/docs/api/?java/util/stream/Stream.html)
and [more-itertools library](https://more-itertools.readthedocs.io/en/latest/).


##  Usage
The main object of library is `iter2`. It behaves like built-in 
`iter` except that it creates an instance of rich-iterator. 
```python
iter2(['dzen', 'of', 'python']).map(str.capitalize).join(' ')  # 'Dzen Of Python'
```

> **Every** method of rich-iterator that returns new iterator makes original rich-iterator **invalid**, so it
> **cannot be used** in any iteration process. This behaviour can be bypassed with `ref` method. 

Original iterator can be retrieved with `raw` method:
```python
orig = iter2.range(5).raw()
tuple(orig)  # (0, 1, 2, 3, 4)
```

`iter2` has some methods to build sequences of values:
```python
iter2.of('a', 'b', 'cde').join()  # 'abcde'
iter2.range(5).map(str).join()  # '01234'
iter2.count_from(100).take(5).map(str).join('->')  # '100->101->102->103->104'
iter2.numeric_range(1.0, 3.5, 0.3).to_tuple()  # (1.0, 1.3, 1.6, 1.9, 2.2, 2.5, 2.8, 3.1, 3.4)
# and some other ...
```

and some algorithm-methods on multiple iterables:
```python
iter2.cartesian_product(range(2), repeat=2).to_tuple()  # ((0, 0), (0, 1), (1, 0), (1, 1))
iter2.zip_longest(range(3), range(1, 5), fillvalue=-1).to_tuple()  # ((0, 1), (1, 2), (2, 3), (-1, 4))
iter2.chain(['Somewhere', 'over'], ['the', 'Rainbow']).join(' ')  # 'Somewhere over the Rainbow
# and some other ...
```


### Comparison
Here are some examples of usage compared with builtins-and-itertools-based 
implementations:

```python
from itertools import islice
from functools import reduce
import operator

from iter2 import iter2

square = lambda x: x ** 2
odd = lambda x: x % 2 == 1

def fibonacci():
    a = b = 1
    while True:
        yield a
        a, b = b, a + b
        

# Example 1:
cool_song = 'Somewhere over the Rainbow'
# "from `cool_song` take capital characters and join them with '+'"
iter2(cool_song).filter(str.isupper).join('+')
# vs
# "with '+' join capital characters from `cool_song`"
'+'.join(filter(str.isupper, cool_song)) 


# Example 2:
# "for values in 0..99 take squares of them that are odd and sum them" (sounds like algo)
iter2.range(100).map(square).filter(odd).sum()
# vs
# "sum values that are odd that are squares of values in 0..99" (sounds like shit)
sum(filter(odd, map(square, range(100))))
# "sum squares of values in 0..99 that are odd"
sum(x ** 2 for x in range(100) if x % 2 == 1) # luckily, oddity doesn't change on squaring


# Example 3: "Playing with infinite sequences"
(iter2(fibonacci())
    .drop(10)
    .filter(odd)
    .map(square)
    .take(5)
    .product())  # shortcut for `.fold(operator.mul)`
# vs
reduce(operator.mul,islice(map(square, filter(odd, islice(fibonacci(), 10, None))), 5))  # (counting braces balance and commas positions)
# (to make clearer):
reduce(
    operator.mul,
    islice(
        map(
            square, 
            filter(
                odd, 
                islice(fibonacci(), 10, None)
            )
        ), 
        5
    )
) # or not?
```

##Changelog

####v1.1

- Tuple-wise methods

#### v1.0

- Initial
