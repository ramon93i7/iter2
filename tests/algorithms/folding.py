import unittest

import iter2.algorithms.folding as algo


class TestFoldingAlgorithms(unittest.TestCase):
    def test_count(self):
        with self.subTest('simple'):
            self.assertEqual(
                algo.count([1, 2, 3]),
                3
            )

    def test_fold(self):
        with self.subTest('simple'):
            self.assertEqual(
                algo.fold([1, 2, 5, 4, 3], max),
                5
            )

        with self.subTest('w/ initial'):
            self.assertEqual(
                algo.fold([1, 2, 3, 4, 5], max, initial=100500),
                100500
            )

    def test_join(self):
        with self.subTest('simple'):
            self.assertEqual(
                algo.join(['1', '2', '3'], '-'),
                '1-2-3'
            )

    def test_max(self):
        with self.subTest('simple'):
            self.assertEqual(
                algo.max([1, 2, 3, 4, 5]),
                5
            )

        with self.subTest('w/ default and no items'):
            self.assertEqual(
                algo.max([], default=100500),
                100500
            )

        with self.subTest('w/ default and some items'):
            self.assertEqual(
                algo.max([1, 2], default=100500),
                2
            )

        with self.subTest('w/ key function'):
            self.assertEqual(
                algo.max(
                    [None, object()],
                    key=lambda item: 100500 if item is None else 0
                ),
                None
            )

    def test_min(self):
        with self.subTest('simple'):
            self.assertEqual(
                algo.min([1, 2, 3, 4, 5]),
                1
            )

        with self.subTest('w/ default and no items'):
            self.assertEqual(
                algo.min([], default=100500),
                100500
            )

        with self.subTest('w/ default and some items'):
            self.assertEqual(
                algo.min([1, 2], default=100500),
                1
            )

        with self.subTest('w/ key function'):
            self.assertEqual(
                algo.min(
                    [None, object()],
                    key=lambda item: 0 if item is None else 100500
                ),
                None
            )

    def test_min_max(self):
        with self.subTest('simple'):
            self.assertEqual(
                algo.minmax([1, 2, 3, 4, 5]),
                (1, 5)
            )

        with self.subTest('w/ default and no items'):
            self.assertEqual(
                algo.minmax([], default=100500),
                100500
            )

        with self.subTest('w/ default and some items'):
            self.assertEqual(
                algo.minmax([1, 2], default=100500),
                (1, 2)
            )

        with self.subTest('w/ key function'):
            self.assertEqual(
                algo.minmax(
                    (True, None),
                    key=lambda item: 0 if item is None else 100500
                ),
                (None, True)
            )

    def test_product(self):
        with self.subTest('simple'):
            self.assertEqual(
                algo.product([1, 2, 3, 4, 5]),
                120
            )

    def test_sum(self):
        with self.subTest('simple'):
            self.assertEqual(
                algo.sum([1, 2, 3, 4, 5]),
                15
            )
