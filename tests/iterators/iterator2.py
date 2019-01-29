import random
import unittest

from iter2.option import None2, Some2
from iter2 import iter2


class TestIterator2(unittest.TestCase):
    # ====================
    # `iterator`-behaviour
    # ====================
    def test_next(self):
        it = iter2([1, 2])
        with self.subTest('next-protocol returns next item'):
            self.assertEqual(next(it), 1)
        with self.subTest('next-method returns Option2'):
            self.assertEqual(it.next().unwrap(), 2)
        with self.subTest('StopIteration on empty iterator'):
            with self.assertRaises(StopIteration):
                next(it)
        with self.subTest('None2 from empty iterator w/ `.next`'):
            self.assertEqual(it.next(), iter2.none)

    # =================================
    # Processing "sequence -> sequence"
    # =================================
    def test_accumulate(self):
        with self.subTest('default: cumulative sum'):
            self.assertEqual(
                iter2([1, 2, 3]).accumulate().to_tuple(),
                (1, 3, 6)
            )
        with self.subTest('custom: with user defined function'):
            self.assertEqual(
                iter2([2, 1, 3]).accumulate(min).to_tuple(),
                (2, 1, 1)
            )
        with self.subTest('w/ initial element'):
            self.assertEqual(
                iter2([2, 1, 3]).accumulate(min, initial=100500).to_tuple(),
                (100500, 2, 1, 1)
            )

    def test_difference(self):
        with self.subTest('simple'):
            self.assertEqual(
                iter2((1, 3, 6)).difference().to_tuple(),
                (1, 2, 3)
            )

        with self.subTest('custom func'):
            self.assertEqual(
                iter2((1, 2, 6)).difference(lambda x, y: x / y).to_tuple(),
                (1, 2, 3)
            )

    def test_enumerate(self):
        with self.subTest('default enumerate: from 0'):
            self.assertEqual(
                iter2([1, 2, 3]).enumerate().to_tuple(),
                ((0, 1), (1, 2), (2, 3))
            )
        with self.subTest('general enumerate: from 4'):
            self.assertEqual(
                iter2([1, 2, 3]).enumerate(count_from=4).to_tuple(),
                ((4, 1), (5, 2), (6, 3))
            )

    def test_filter(self):
        self.assertEqual(
            iter2([1, 2, 3]).filter(lambda x: x % 3 == 1).to_tuple(),
            (1,)
        )

    def test_filter_builtin_none(self):
        self.assertEqual(
            iter2([0, 1, None, 3, '', {}, set()]).filter_builtin_none().to_tuple(),
            (0, 1, 3, '', {}, set())
        )

    def test_filter_none(self):
        self.assertEqual(
            iter2([Some2(1), None2, Some2(3)]).filter_none().to_tuple(),
            (1, 3)
        )

    def test_flatmap(self):
        self.assertEqual(
            iter2([1, 2, 3]).flatmap(lambda x: [1] * x).to_tuple(),
            (1,) * (1+2+3)
        )

    def test_flatten(self):
        self.assertEqual(
            iter2([(1, 2), (3,), (4, 5)]).flatten().to_tuple(),
            (1, 2, 3, 4, 5)
        )

    def test_for_each(self):
        res = []
        iter2([1, 2, 3]).for_each(res.append)
        self.assertEqual(res, [1, 2, 3])

    def test_map(self):
        self.assertEqual(
            iter2([1, 2, 3]).map(lambda x: x ** 2).to_tuple(),
            (1, 4, 9)
        )

    def test_starmap(self):
        self.assertEqual(
            iter2([(2, 5), (3, 2), (10, 3)]).starmap(pow).to_tuple(),
            (32, 9, 1000)
        )

    # ===================
    # Checking conditions
    # ===================
    def test_all(self):
        self.assertTrue(
            iter2([1, 2, 3]).all(lambda x: x > 0)
        )

    def test_any(self):
        self.assertTrue(
            iter2([1, 2, 3]).any(lambda x: x > 1)
        )

    def test_none(self):
        self.assertTrue(
            iter2([1, 2, 3]).none(lambda x: x < 0)
        )

    # =============
    # Making groups
    # =============
    def test_chunks(self):
        with self.subTest('default'):
            self.assertEqual(
                iter2([1, 2, 3, 4, 5])
                    .chunks(2)
                    .to_tuple(),
                ((1, 2), (3, 4))
            )
        with self.subTest('allow partial'):
            self.assertEqual(
                iter2([1, 2, 3, 4, 5])
                    .chunks(2, allow_partial=True)
                    .to_tuple(),
                ((1, 2), (3, 4), (5,))
            )

    def test_chunks_with_padding(self):
        with self.subTest('default'):
            self.assertEqual(
                iter2([1, 2, 3]).chunks_with_padding(2).to_tuple(),
                ((1, 2), (3, None))
            )
        with self.subTest('w/ fillvalue'):
            self.assertEqual(
                iter2([1, 2, 3]).chunks_with_padding(2, fillvalue=100500).to_tuple(),
                ((1, 2), (3, 100500))
            )
        with self.subTest('w/o remainder'):
            self.assertEqual(
                iter2([1, 2, 3, 4]).chunks_with_padding(2).to_tuple(),
                ((1, 2), (3, 4))
            )

    def test_consecutive_groups(self):
        with self.subTest('simple'):
            self.assertEqual(
                iter2([1, 2, 10, 11, 100, 101]).consecutive_groups().map(tuple).to_tuple(),
                ((1, 2), (10, 11), (100, 101))
            )

        with self.subTest('custom `ordering`'):
            self.assertEqual(
                iter2('abcBCDcde').consecutive_groups(ordering=ord).map(tuple).to_tuple(),
                (('a', 'b', 'c'), ('B', 'C', 'D'), ('c', 'd', 'e'))
            )

    def test_dedup(self):
        self.assertEqual(
            iter2([1, 2, 2, 3, 3, 3, 2, 2, 1]).dedup().to_tuple(),
            (1, 2, 3, 2, 1)
        )

    def test_group_by(self):
        with self.subTest('default: key is identity function'):
            self.assertEqual(
                iter2([1, 2, 2, 3, 3, 3])
                    .group_by()
                    .starmap(lambda val, subiter: (val, subiter.count()))
                    .to_tuple(),
                ((1, 1), (2, 2), (3, 3))
            )
        with self.subTest('w/ key function'):
            self.assertEqual(
                iter2([1, 2, 2, 3, 3, 3])
                    .group_by(key=lambda x: x % 2)
                    .starmap(lambda val, sub_iter: (val, sub_iter.count()))
                    .to_tuple(),
                ((1, 1), (0, 2), (1, 3))
            )

    def test_process_in_groups(self):
        materialize = lambda pair: (pair[0], tuple(pair[1]))

        with self.subTest('"group_by"'):
            self.assertEqual(
                (iter2([1, 2, 2, 3, 3, 3])
                    .process_in_groups(key=lambda x: x % 2)
                    .map(materialize)
                    .to_tuple()),
                ((1, (1,)), (0, (2, 2)), (1, (3, 3, 3)))
            )

        with self.subTest('w/ transformation'):
            self.assertEqual(
                (iter2([1, 2, 2, 3, 3, 3])
                    .process_in_groups(transformation=lambda x: x % 2)
                    .map(materialize)
                    .to_tuple()),
                ((1, (1,)), (2, (0, 0)), (3, (1, 1, 1)))
            )

        with self.subTest('w/ aggregator'):
            self.assertEqual(
                (iter2([1, 2, 2, 3, 3, 3])
                    .process_in_groups(aggregator=sum)
                    .to_tuple()),
                ((1, 1), (2, 4), (3, 9))
            )

    # ===========
    # (Un)Merging
    # ===========
    def test_distribute(self):
        first, second, third = iter2([1, 2, 3, 4, 5]).distribute(3)
        self.assertEqual( first.to_tuple(), (1, 4))
        self.assertEqual(second.to_tuple(), (2, 5))
        self.assertEqual( third.to_tuple(), (3,))

    def test_cartesian_product(self):
        self.assertEqual(
            iter2([1, 2]).cartesian_product(repeat=2).to_tuple(),
            ((1, 1), (1, 2), (2, 1), (2, 2))
        )

    def test_interleave(self):
        seq1 = 'abc'
        seq2 = 'ij'
        seq3 = 'xyz'
        self.assertEqual(
            iter2(seq1).interleave(seq2, seq3).join(''),
            'aixbjycz'
        )

    def test_interleave_shortest(self):
        seq1 = 'abc'
        seq2 = 'ij'
        seq3 = 'xyz'
        self.assertEqual(
            iter2(seq1).interleave_shortest(seq2, seq3).join(''),
            'aixbjy'
        )

    def test_intersperse(self):
        with self.subTest('empty iterator'):
            self.assertEqual(
                iter2(()).intersperse(0).to_tuple(),
                ()
            )
        with self.subTest('common case'):
            self.assertEqual(
                iter2([1, 2, 3]).intersperse(0).to_tuple(),
                (1, 0, 2, 0, 3)
            )

    def test_pairwise(self):
        self.assertEqual(
            iter2([1, 2, 3]).pairwise().to_tuple(),
            ((1, 2), (2, 3))
        )

    def test_partition(self):
        t, f = iter2([1, 2, 3, 4, 5]).partition(lambda x: x % 2 == 0)
        self.assertEqual(t.to_tuple(), (2, 4))
        self.assertEqual(f.to_tuple(), (1, 3, 5))

    def test_split_after(self):
        with self.subTest('simple'):
            self.assertEqual(
                (iter2('192.168.0.1')
                    .split_after(lambda c: c == '.')
                    .map(tuple)
                    .to_tuple()),
                tuple(map(tuple, ('192.', '168.', '0.', '1')))
            )

    def test_split_at(self):
        with self.subTest('simple'):
            self.assertEqual(
                (iter2('192.168.0.1')
                    .split_at(lambda c: c == '.')
                    .map(tuple)
                    .to_tuple()),
                tuple(map(tuple, ('192', '168', '0', '1')))
            )

    def test_split_before(self):
        with self.subTest('simple'):
            self.assertEqual(
                (iter2('192.168.0.1')
                    .split_before(lambda c: c == '.')
                    .map(tuple)
                    .to_tuple()),
                tuple(map(tuple, ('192', '.168', '.0', '.1')))
            )


    def test_permutations(self):
        with self.subTest('default'):
            self.assertEqual(
                iter2([1, 2, 3]).permutations().to_tuple(),
                ((1, 2, 3), (1, 3, 2),
                 (2, 1, 3), (2, 3, 1),
                 (3, 1, 2), (3, 2, 1))
            )
        with self.subTest('pairs'):
            self.assertEqual(
                iter2([1, 2, 3]).permutations(length=2).to_tuple(),
                ((1, 2), (1, 3),
                 (2, 1), (2, 3),
                 (3, 1), (3, 2))
            )

    def test_stagger(self):
        with self.subTest('default'):
            self.assertEqual(
                iter2([1, 2, 3]).stagger().to_tuple(),
                ((None, 1, 2), (1, 2, 3))
            )
        with self.subTest('offsets'):
            self.assertEqual(
                iter2.range(8).stagger(offsets=(0, 2, 4)).to_tuple(),
                ((0, 2, 4), (1, 3, 5), (2, 4, 6), (3, 5, 7))
            )
        with self.subTest('longest'):
            self.assertEqual(
                iter2([1, 2, 3]).stagger(longest=True).to_tuple(),
                ((None, 1, 2), (1, 2, 3), (2, 3, None), (3, None, None))
            )

    def test_unzip(self):
        letters = 'abc'
        digits = [1, 2, 3]

        with self.subTest('default: arity=2'):
            ls, ds = iter2(zip(letters, digits)).unzip()
            self.assertEqual(ls.to_tuple(), tuple(letters))
            self.assertEqual(ds.to_tuple(), tuple(digits))

        with self.subTest('arity=3'):
            ls, ds, lsr = iter2(zip(letters, digits,reversed(letters))) \
                .unzip(arity=3)
            self.assertEqual(ls.to_tuple(), tuple(letters))
            self.assertEqual(ds.to_tuple(), tuple(digits))
            self.assertEqual(lsr.to_tuple(), tuple(reversed(letters)))

    def test_zip(self):
        self.assertEqual(
            iter2('abc').zip([1, 2, 3]).to_tuple(),
            (('a', 1), ('b', 2), ('c', 3))
        )

    def test_zip_longest(self):
        self.assertEqual(
            iter2('ab').zip_longest([1, 2, 3]).to_tuple(),
            (('a', 1), ('b', 2), (None, 3))
        )

    def test_zip_offset(self):
        with self.subTest('default'):
            self.assertEqual(
                iter2('0123').zip_offset('abcdef', offsets=(0, 1)).to_tuple(),
                (('0', 'b'), ('1', 'c'), ('2', 'd'), ('3', 'e'))
            )
        with self.subTest('negative offsets'):
            self.assertEqual(
                iter2('0123')
                    .zip_offset('abcdef', offsets=(-1, 0), fillvalue='@')
                    .to_tuple(),
                (('@', 'a'), ('0', 'b'), ('1', 'c'), ('2', 'd'), ('3', 'e'))
            )
        with self.subTest('longest'):
            self.assertEqual(
                iter2('0123')
                    .zip_offset('abcdef', offsets=(-1, 0), fillvalue='@', longest=True)
                    .to_tuple(),
                (('@', 'a'), ('0', 'b'), ('1', 'c'), ('2', 'd'), ('3', 'e'), ('@', 'f'))
            )

    # =================
    # Flow manipulation
    # =================
    def test_chain(self):
        with self.subTest('chain rich iterators'):
            self.assertEqual(
                iter2([1, 2, 3]).chain(iter2([4, 5]), iter2([6, 7])).to_tuple(),
                (1, 2, 3, 4, 5, 6, 7)
            )
        with self.subTest('chain with iterable'):
            self.assertEqual(
                iter2([1, 2, 3]).chain([4, 5], [6, 7]).to_tuple(),
                (1, 2, 3, 4, 5, 6, 7)
            )

    def test_chain_from_iterable(self):
        with self.subTest('simple'):
            self.assertEqual(
                iter2([1, 2, 3]).chain_from_iterable([(4, 5), (6, 7)]).to_tuple(),
                (1, 2, 3, 4, 5, 6, 7)
            )

    def test_consume(self):
        self.assertEqual(
            iter2([1, 2, 3]).consume().to_tuple(),
            ()
        )

    def test_drop(self):
        self.assertEqual(
            iter2([1, 2, 3, 4, 5]).drop(2).to_tuple(),
            (3, 4, 5)
        )

    def test_drop_while(self):
        it = iter2([1, 2, 3, 4, 5])
        self.assertEqual(
            it.drop_while(lambda x: x < 3).to_tuple(),
            (3, 4, 5)
        )

    def test_find(self):
        with self.subTest('item exist'):
            self.assertEqual(
                iter2([1, 2, 3]).find(lambda x: x % 2 == 0).unwrap(),
                2
            )
        with self.subTest('not found'):
            self.assertTrue(
                iter2([1, 2, 3]).find(lambda x: x == 5).is_none()
            )

    def test_first(self):
        self.assertEqual(iter2([1, 2, 3]).first().unwrap(), 1)

    def test_last(self):
        self.assertEqual(iter2([1, 2, 3]).last().unwrap(), 3)

    def test_locate(self):
        with self.subTest('w/o items'):
            self.assertEqual(
                iter2('aBcDe').locate(str.isupper, count_from=1).to_tuple(),
                (2, 4)
            )

        with self.subTest('w/ items'):
            self.assertEqual(
                iter2('aBcDe').locate(str.isupper, count_from=1, with_items=True).to_tuple(),
                ((2, 'B'), (4, 'D'))
            )

        with self.subTest('not found'):
            self.assertEqual(
                iter2('abcde').locate(str.isupper, count_from=1).to_tuple(),
                ()
            )

    def test_nth(self):
        with self.subTest('found'):
            self.assertEqual(
                iter2([1, 2, 3]).nth(1).unwrap(),
                2
            )
        with self.subTest('not found'):
            self.assertTrue(
                iter2([1, 2, 3]).nth(10).is_none()
            )

    def test_position(self):
        with self.subTest('found'):
            self.assertEqual(
                iter2('aBcDe').position(str.isupper, count_from=1).unwrap(),
                2
            )

        with self.subTest('not found'):
            self.assertTrue(
                iter2('abcde').position(str.isupper, count_from=1).is_none()
            )

    def test_prepend(self):
        with self.subTest('simple'):
            self.assertEqual(
                iter2([3, 4]).prepend([1, 2]).to_tuple(),
                (1, 2, 3, 4)
            )

    def test_cycle(self):
        with self.subTest('repeat forever in cycle'):
            count = random.randint(1, 5)
            self.assertEqual(
                iter2([1]).cycle().take(count).to_tuple(),
                (1,) * count
            )
        with self.subTest('repeat several times'):
            self.assertEqual(
                iter2([1, 2]).cycle(number=4).to_tuple(),
                (1, 2) * 4
            )

    def test_skip(self):
        'alias for `Iterator2.drop`'
        pass

    def test_skip_while(self):
        'alias for `Iterator2.drop_while`'
        pass

    def test_slice(self):
        with self.subTest('Short variant: only `stop` argument.'):
            self.assertEqual(
                iter2([1, 2, 3]).slice(2).to_tuple(),
                (1, 2)
            )
        with self.subTest('Interval variant: `start`, `stop` without `step`.'):
            self.assertEqual(
                iter2([1, 2, 3, 4, 5]).slice(1, 3+1).to_tuple(),
                (2, 3, 4)
            )
        with self.subTest('Full variant: `start`, `stop` and `step`.'):
            self.assertEqual(
                iter2([1, 2, 3, 4, 5]).slice(1, 3+1, 2).to_tuple(),
                (2, 4)
            )

    def test_sliding_window(self):
        with self.subTest('default'):
            self.assertEqual(
                iter2([1, 2, 3]) \
                    .sliding_window() \
                    .to_tuple(),
                ((1,), (2,), (3,))
            )
        with self.subTest('split into pairs'):
            self.assertEqual(
                iter2([1, 2, 3, 4, 5])
                    .sliding_window(step=2, size=2)
                    .to_tuple(),
                ((1, 2), (3, 4))
            )
        with self.subTest('3-size window'):
            self.assertEqual(
                iter2([1, 2, 3, 4, 5])
                    .sliding_window(size=3)
                    .to_tuple(),
                ((1, 2, 3), (2, 3, 4), (3, 4, 5))
            )
        with self.subTest('step > size is OK'):
            self.assertEqual(
                iter2([1, 2, 3, 4, 5])
                    .sliding_window(step=3, size=2)
                    .to_tuple(),
                ((1, 2), (4, 5))
            )
        with self.subTest('partial window at the end'):
            self.assertEqual(
                iter2([1, 2, 3, 4, 5])
                    .sliding_window(step=2, size=2, allow_partial=True)
                    .to_tuple(),
                ((1, 2), (3, 4), (5,))
            )

    def test_step(self):
        self.assertEqual(
            iter2([1, 2, 3, 4, 5]).step(2).to_tuple(),
            (1, 3, 5)
        )

    def test_sort(self):
        with self.subTest('default'):
            self.assertEqual(
                iter2([3, 1, 2]).sort().to_tuple(),
                (1, 2, 3)
            )
        with self.subTest('reverse'):
            self.assertEqual(
                iter2([3, 1, 2]).sort(reverse=True).to_tuple(),
                (3, 2, 1)
            )
        with self.subTest('w/ key'):
            self.assertEqual(
                iter2(dict(a=1, b=2, c=0).items())
                    .sort(key=lambda pair: pair[1])
                    .to_tuple(),
                (('c', 0), ('a', 1), ('b', 2))
            )

    def test_take(self):
        with self.subTest('default'):
            self.assertEqual(
                iter2([1, 2, 3]).take().to_tuple(),
                (1,)
            )
        with self.subTest('take pair'):
            self.assertEqual(
                iter2([2, 3]).take(2).to_tuple(),
                (2, 3)
            )
        with self.subTest('result may be insufficient'):
            self.assertEqual(
                iter2([1, 2, 3]).take(10).to_tuple(),
                (1, 2, 3)
            )

    def test_take_now(self):
        with self.subTest('default'):
            self.assertEqual(
                iter2([1, 2, 3]).take_now(),
                (1,)
            )
        with self.subTest('take pair'):
            self.assertEqual(
                iter2([2, 3]).take_now(2),
                (2, 3)
            )
        with self.subTest('result may be insufficient'):
            self.assertEqual(
                iter2([1, 2, 3]).take_now(10),
                (1, 2, 3)
            )

    def test_take_into_option(self):
        with self.subTest('default'):
            self.assertEqual(
                iter2([1, 2, 3]).take_into_option().unwrap(),
                (1,)
            )
        with self.subTest('take pair'):
            self.assertEqual(
                iter2([1, 2, 3]).take_into_option(2).unwrap(),
                (1, 2)
            )
        with self.subTest('None2 if insufficient'):
            self.assertTrue(
                iter2([1, 2]).take_into_option(3).is_none()
            )
        with self.subTest('if insufficient then return back taken items to iterator'):
            it = iter2([1, 2])
            self.assertTrue(it.take_into_option(3).is_none())
            self.assertEqual(
                it.take_into_option(2).unwrap(),
                (1, 2)
            )

    def test_take_last(self):
        with self.subTest('default'):
            self.assertEqual(
                iter2([1, 2, 3]).take_last().to_tuple(),
                (3,)
            )
        with self.subTest('take pair'):
            self.assertEqual(
                iter2([1, 2, 3]).take_last(2).to_tuple(),
                (2, 3)
            )

    def test_take_last_into_option(self):
         with self.subTest('default'):
            self.assertEqual(
                iter2([1, 2, 3]).take_last_into_option().unwrap(),
                (3,)
            )
         with self.subTest('take pair'):
            self.assertEqual(
                iter2([1, 2, 3]).take_last_into_option(2).unwrap(),
                (2, 3)
            )
         with self.subTest('if insufficient then return back taken items to iterator'):
            it = iter2([1, 2])
            self.assertTrue(it.take_last_into_option(3).is_none())
            self.assertEqual(
                it.take_last_into_option(2).unwrap(),
                (1, 2)
            )

    def test_take_last_now(self):
        with self.subTest('default'):
            self.assertEqual(
                iter2([1, 2, 3]).take_last_now(),
                (3,)
            )
        with self.subTest('take pair'):
            self.assertEqual(
                iter2([1, 2, 3]).take_last_now(2),
                (2, 3)
            )


    def test_take_while(self):
        with self.subTest('default: do not keep border element'):
            it = iter2([1, 2, 3, 4, 5])
            self.assertEqual(
                it.ref().take_while(lambda x: x < 3).to_tuple(),
                (1, 2)
            )
            # `3` was consumed and not placed back
            self.assertEqual(
                it.ref().to_tuple(),
                (4, 5)
            )

    def test_unique(self):
        self.assertEqual(
            iter2([1, 3, 2, 3, 2, 3]).unique().collect(frozenset),
            frozenset([1, 2, 3])
        )

    # =============
    # Materializing
    # =============
    def test_collect(self):
        with self.subTest('Collecting to default collection (tuple)'):
            self.assertEqual(
                iter2([1, 2, 3]).collect(),
                (1, 2, 3)
            )

        SUBTESTS = (
            (tuple,     [1, 2, 3],              (1, 2, 3)),
            (list,      [1, 2, 3],              [1, 2, 3]),
            (frozenset, [1, 1, 3],              frozenset([1, 3])),
            (set,       [1, 1, 3],              {1, 3}),
            (dict,      [('a', 1), ('b', 2)],   dict(a=1, b=2))
        )

        for factory, input, output in SUBTESTS:
            with self.subTest('Collecting to {factory}'.format(factory=factory)):
                self.assertEqual(
                    iter2(input).collect(factory),
                    output
                )

    # ===========
    # Duplication
    # ===========
    def test_copy(self):
        orig = iter2([1, 2, 3])
        copy = orig.copy()
        self.assertEqual(
            orig.to_tuple(),
            (1, 2, 3)
        )
        self.assertEqual(
            copy.collect(list),
            [1, 2, 3]
        )

    def test_tee(self):
        copy1, copy2 = iter2([1, 2, 3]).tee()
        self.assertEqual(
            copy1.to_tuple(),
            (1, 2, 3)
        )
        self.assertEqual(
            copy2.collect(list),
            [1, 2, 3]
        )


    # =======
    # Folding
    # =======
    def test_count(self):
        with self.subTest('empty iterator'):
            self.assertEqual(iter2([]).count(), 0)
        with self.subTest('non-empty iterator'):
            self.assertEqual(iter2([1, 2, 3]).count(), 3)

    def test_fold(self):
        with self.subTest('w/o initial'):
            self.assertEqual(
                iter2([1, 2, 3]).fold(lambda st, x: st + x),
                sum([1, 2, 3])
            )
        with self.subTest('w/ initial'):
            self.assertEqual(
                iter2([1, 2, 3]).fold(lambda st, x: st + x, initial=-3),
                sum([-3,  1, 2, 3])
            )

    def test_join(self):
        with self.subTest('str'):
            self.assertEqual(
                iter2('abc').join('-'),
                'a-b-c'
            )
        with self.subTest('bytes'):
            self.assertEqual(
                iter2([b'a', b'b', b'c']).join(b'-'),
                b'a-b-c'
            )
        with self.subTest('incompatible'):
            with self.assertRaises(TypeError):
                _ = iter2('abc').join(b'-')

    def test_max(self):
        with self.subTest('empty'):
            self.assertEqual(
                iter2([]).max(),
                None
            )
        with self.subTest('empty with default'):
            self.assertEqual(
                iter2([]).max(default=100500),
                100500
            )
        with self.subTest('regular, w/o key'):
            self.assertEqual(
                iter2([1, 2, 3]).max(),
                3
            )
        with self.subTest('regular, w/ key'):
            self.assertEqual(
                # [(1, -1), (0, -2), (1, -3), (0, -4)]
                iter2([1, 2, 3, 4]).max(key=lambda x: (x % 2, -x)),
                1
            )

    def test_min(self):
        with self.subTest('empty'):
            self.assertEqual(
                iter2([]).min(),
                None
            )
        with self.subTest('empty with default'):
            self.assertEqual(
                iter2([]).min(default=100500),
                100500
            )
        with self.subTest('regular, w/o key'):
            self.assertEqual(
                iter2([1, 2, 3]).min(),
                1
            )
        with self.subTest('regular, w/ key'):
            self.assertEqual(
                iter2([1, 2, 3, 4]).min(key=lambda x: (x % 2, -x)),
                # [(1, -1), (0, -2), (1, -3), (0, -4)]
                4
            )

    def test_minmax(self):
        with self.subTest('empty'):
            self.assertEqual(
                iter2([]).minmax(),
                None
            )
        with self.subTest('empty with default'):
            self.assertEqual(
                iter2([]).minmax(default=100500),
                100500
            )
        with self.subTest('regular, w/o key'):
            self.assertEqual(
                iter2([1, 2, 3]).minmax(),
                (1, 3)
            )
        with self.subTest('regular, w/ key'):
            self.assertEqual(
                iter2([1, 2, 3, 4]).minmax(key=lambda x: (x % 2, -x)),
                # [(1, -1), (0, -2), (1, -3), (0, -4)]
                (4, 1)
            )

    def test_product(self):
        self.assertEqual(
            iter2([1, 2, 3]).product(),
            (1 * 2 * 3)
        )

    def test_reduce(self):
        'alias for `iterator2.fold`'
        pass

    def test_sum(self):
        self.assertEqual(
            iter2([1, 2, 3]).sum(),
            sum([1, 2, 3])
        )

    # ======================
    # Lookahead and lookback
    # ======================
    def test_spy(self):
        with self.subTest('default :: sufficient'):
            it = iter2([1, 2, 3])
            self.assertEqual(
                it.spy(2).unwrap(),
                (1, 2)
            )
            self.assertEqual(it.to_tuple(), (1, 2, 3))
        with self.subTest('default :: insufficient'):
            it = iter2([1, 2, 3])
            self.assertTrue(it.spy(4).is_none())
            self.assertEqual(it.to_tuple(), (1, 2, 3))
        with self.subTest('partial :: sufficient'):
            it = iter2([1, 2, 3])
            self.assertEqual(it.spy(2, allow_partial=True).unwrap(), (1, 2))
            self.assertEqual(it.to_tuple(), (1, 2, 3))
        with self.subTest('partial :: insufficient'):
            it = iter2([1, 2, 3])
            self.assertEqual(it.spy(4, allow_partial=True).unwrap(), (1, 2, 3))
            self.assertEqual(it.to_tuple(), (1, 2, 3))
