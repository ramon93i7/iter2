import unittest

import iter2.algorithms.predicate_on_sequence as algo


class TestPredicateOnSequenceAlgorithms(unittest.TestCase):
    def test_all(self):
        with self.subTest('simple - positive'):
            self.assertEqual(
                algo.all([1, 2, 3], lambda x: x < 10),
                True
            )

        with self.subTest('simple - negative'):
            self.assertEqual(
                algo.all([1, 2, 3], lambda x: x % 2 == 0),
                False
            )

    def test_any(self):
        with self.subTest('simple - positive'):
            self.assertEqual(
                algo.any([1, 2, 3], lambda x: x % 2 == 0),
                True
            )

        with self.subTest('simple - negative'):
            self.assertEqual(
                algo.any([1, 2, 3], lambda x: x > 10),
                False
            )

    def test_none(self):
        with self.subTest('simple - positive'):
            self.assertEqual(
                algo.none([1, 2, 3], lambda x: x > 10),
                True
            )

        with self.subTest('simple - negative'):
            self.assertEqual(
                algo.none([1, 2, 3], lambda x: x % 2 == 0),
                False
            )


