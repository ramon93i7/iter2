import unittest

import iter2.algorithms.extra as algo


class TestExtraAlgorithms(unittest.TestCase):
    def assertEqualAsTuples(self, first, second):
        self.assertEqual(tuple(first), tuple(second))

    def test_cartesian_product(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.cartesian_product((1, 2), 'ab', [True]),
                ((1, 'a', True),
                 (1, 'b', True),
                 (2, 'a', True),
                 (2, 'b', True))
            )
        with self.subTest('w/ repeat'):
            self.assertEqualAsTuples(
                algo.cartesian_product(range(2), repeat=2),
                ((0, 0), (0, 1), (1, 0), (1, 1))
            )

    def test_sort_together(self):
        with self.subTest('simple'):
            first, second = algo.sort_together(
                [3, 2, 1],
                  'cba'
            )
            self.assertEqualAsTuples(  first,       (1, 2, 3) )
            self.assertEqualAsTuples( second, ('a', 'b', 'c') )

        with self.subTest('by one iterable but w/ key_func'):
            first, second = algo.sort_together(
                [1, 2, 3, 4, 5],
                    'abcde',
                key_func=(lambda x: x % 2)
            )
            self.assertEqualAsTuples(  first, ( 2,   4,   1,   3,   5)  )
            self.assertEqualAsTuples( second, ('b', 'd', 'a', 'c', 'e') )

        with self.subTest('w/ parameters'):
            WOMEN_PENSION_AGE = 60
            names, ages, salaries = algo.sort_together(
                [ 'Lera', 'Nastya', 'Polina'],
                [     25,       22,       24],
                [ 150000,   200000,    40000],
                key_list=(1, 2),
                key_func=lambda age, salary: (WOMEN_PENSION_AGE - age) * salary,
                reverse=True
            )
            self.assertEqualAsTuples( names,    ( 'Nastya', 'Lera', 'Polina' ) )
            self.assertEqualAsTuples( ages,     (       22,     25,       24 ) )
            self.assertEqualAsTuples( salaries, (   200000, 150000,    40000 ) )

    def test_unique_to_each(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                map(sorted, algo.unique_to_each(
                    'abc',   'bcd',    'def'
                )), (
                    ['a'],    [],    ['e','f']
                )
            )