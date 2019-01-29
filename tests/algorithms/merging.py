import unittest

import iter2.algorithms.merging as algo


class TestMergingAlgorithms(unittest.TestCase):
    def assertEqualAsTuples(self, first, second):
        self.assertEqual(
            tuple(first),
            tuple(second)
        )

    def test_chain(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.chain([1, 2], [3, 4]),
                (1, 2, 3, 4)
            )

    def test_chain_from_iterable(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.chain_from_iterable([[1, 2], [3, 4]]),
                (1, 2, 3, 4)
            )

    def test_collate(self):
        pass

    def test_interleave(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.interleave('123', 'abc'),
                ('1', 'a', '2', 'b', '3', 'c')
            )

        with self.subTest('asymmetric'):
            self.assertEqualAsTuples(
                algo.interleave('12', 'abc'),
                ('1', 'a', '2', 'b', 'c')
            )

    def test_interleave_shortest(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.interleave_shortest('123', 'abc'),
                ('1', 'a', '2', 'b', '3', 'c')
            )

        with self.subTest('asymmetric'):
            self.assertEqualAsTuples(
                algo.interleave_shortest('12', 'abc'),
                ('1', 'a', '2', 'b')
            )

    def test_prepend(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.prepend([3, 4], [1, 2]),
                (1, 2, 3, 4)
            )

    def test_zip(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.zip('123', 'abc'),
                (('1', 'a'), ('2', 'b'), ('3', 'c'))
            )

        with self.subTest('asymmetric'):
            self.assertEqualAsTuples(
                algo.zip('12', 'abc'),
                (('1', 'a'), ('2', 'b'))
            )

    def test_zip_longest(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.zip_longest('123', 'abc'),
                (('1', 'a'), ('2', 'b'), ('3', 'c'))
            )

        with self.subTest('asymmetric'):
            self.assertEqualAsTuples(
                algo.zip_longest('12', 'abc', fillvalue='#'),
                (('1', 'a'), ('2', 'b'), ('#', 'c'))
            )

    def test_zip_offset(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.zip_offset('12', 'abcd', offsets=(0, 1)),
                (('1', 'b'), ('2', 'c'))
            )

        with self.subTest('longest'):
            self.assertEqualAsTuples(
                algo.zip_offset('12', 'abcd', offsets=(0, 1), fillvalue='#', longest=True),
                (('1', 'b'), ('2', 'c'), ('#', 'd'))
            )
