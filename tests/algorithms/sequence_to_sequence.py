import unittest
import random

import iter2.algorithms.sequence_to_sequence as algo


class TestSequenceToSequenceAlgorithms(unittest.TestCase):
    def assertEqualAsTuples(self, first, second):
        self.assertEqual(
            tuple(first),
            tuple(second)
        )

    def test_accumulate(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.accumulate((1, 2, 3)),
                (1, 3, 6)
            )

        with self.subTest('custom func'):
            self.assertEqualAsTuples(
                algo.accumulate((1, 2, 3), lambda x, y: x * y),
                (1, 2, 6)
            )

    def test_add_side_effect(self):
        with self.subTest('simple'):
            side_effect_shell = []
            it = algo.add_side_effect(
                ['Julia', 'Angelina', 'Jessica'],
                side_effect_shell.append,
                before=lambda: side_effect_shell.append('before'),
                after=lambda: side_effect_shell.append('after')
            )
            res = tuple(it)
            self.assertEqualAsTuples(
                res,
                ('Julia', 'Angelina', 'Jessica')
            )
            self.assertEqualAsTuples(
                side_effect_shell,
                ('before', 'Julia', 'Angelina', 'Jessica', 'after')
            )

        with self.subTest('w/ chunks'):
            side_effect_shell = []
            it = algo.add_side_effect(
                range(10),
                side_effect_shell.append,
                chunk_size=4
            )
            res = tuple(it)
            self.assertEqualAsTuples(
                res,
                range(10)
            )
            self.assertEqualAsTuples(
                side_effect_shell,
                ((0, 1, 2, 3), (4, 5, 6, 7), (8, 9))
            )

    def test_consume(self):
        with self.subTest('full'):
            self.assertEqualAsTuples(
                algo.consume(range(10)),
                ()
            )

        with self.subTest('partial'):
            self.assertEqualAsTuples(
                algo.consume(range(10), 8),
                (8, 9)
            )

    def test_cycle(self):
        with self.subTest('fixed number of iterations'):
            self.assertEqualAsTuples(
                algo.cycle('ab', number=3),
                'ababab'
            )

        with self.subTest('infinite number of iterations'):
            self.assertTrue(
                all(
                    val == ans
                    for val, ans in zip(
                        algo.cycle('ab'),
                        'ab' * random.randint(1, 10)  # shame
                    )
                )
            )

    def test_dedup(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.dedup('aaaaabbbbbbbbc'),
                'abc'
            )

    def test_difference(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.difference((1, 3, 6)),
                (1, 2, 3)
            )

        with self.subTest('custom func'):
            self.assertEqualAsTuples(
                algo.difference((1, 2, 6), lambda x, y: x / y),
                (1, 2, 3)
            )

    def test_drop(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.drop('abcdef', 3),
                'def'
            )

    def test_drop_while(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.drop_while('abcDef', str.islower),
                'Def'
            )

    def test_enumerate(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.enumerate('abc'),
                ((0, 'a'), (1, 'b'), (2, 'c'))
            )

        with self.subTest('custom start index'):
            self.assertEqualAsTuples(
                algo.enumerate('abc', count_from=10),
                ((10, 'a'), (11, 'b'), (12, 'c'))
            )

    def test_filter(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.filter('aBcDe', str.islower),
                'ace'
            )

    def test_filter_none(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.filter_none((1, None, 2, None)),
                (1, 2)
            )

    def test_flatmap(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.flatmap(['one two', 'three four', 'five'], str.split),
                ('one', 'two', 'three', 'four', 'five')
            )

    def test_flatten(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.flatten(['ab', 'cd', 'ef']),
                'abcdef'
            )

    def test_intersperse(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.intersperse('abc', ' '),
                'a b c'
            )

    def test_map(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.map('abc', str.upper),
                'ABC'
            )

    def test_slice(self):
        with self.subTest('prefix'):
            self.assertEqualAsTuples(
                algo.slice('abcdef', 3),
                'abc'
            )

        with self.subTest('suffix'):
            self.assertEqualAsTuples(
                algo.slice('abcdef', 3, None),
                'def'
            )

        with self.subTest('step'):
            self.assertEqualAsTuples(
                algo.slice('abcdef', None, None, 2),
                'ace'
            )

        with self.subTest('complex'):
            self.assertEqualAsTuples(
                algo.slice('abcdef', 1, 5, 2),
                'bd'
            )

    def test_starmap(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.starmap(('aB', 'aC', 'zA'), lambda f, s: f.upper() + s.lower()),
                ('Ab', 'Ac', 'Za')
            )

    def test_step(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.step('abcdef', 3),
                'ad'
            )

    def test_take(self):
        with self.subTest('simple'):
            it = iter('abcdef')
            self.assertEqualAsTuples(
                algo.take(it, 3),
                'abc'
            )
            self.assertEqualAsTuples(
                it,
                'def'
            )

        with self.subTest('lazy'):
            it = iter('abcdef')
            take2 = algo.take(it, 2)
            take3 = algo.take(it, 3)
            self.assertEqualAsTuples(
                map(next, [take2, take3, take3]),
                'abc'
            )
            self.assertEqualAsTuples(take2, 'd')
            self.assertEqualAsTuples(take3, 'e')

        with self.subTest('partial'):
            self.assertEqualAsTuples(
                algo.take('ab', 3),
                'ab'
            )

    def test_take_now(self):
        with self.subTest('simple'):
            it = iter('abcdef')
            self.assertEqual(
                algo.take_now(it, 3),
                tuple('abc')
            )
            self.assertEqualAsTuples(it, 'def')

        with self.subTest('not lazy'):
            it = iter('abcdef')
            f3 = algo.take_now(it, 3)
            s2 = algo.take_now(it, 2)
            self.assertEqualAsTuples(f3, 'abc')
            self.assertEqualAsTuples(s2, 'de')
            self.assertEqualAsTuples(it, 'f')

        with self.subTest('partial'):
            self.assertEqual(
                algo.take_now('ab', 3),
                ('a', 'b')
            )

    def test_take_last(self):
        with self.subTest('simple & not lazy'):
            it = iter('abcdef')
            self.assertEqual(
                algo.take_last(it, 3),
                tuple('def')
            )
            self.assertEqualAsTuples(it, ())

        with self.subTest('partial'):
            self.assertEqual(
                algo.take_last('ab', 3),
                ('a', 'b')
            )

    def test_take_while(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.take_while('abcDef', str.islower),
                'abc'
            )
