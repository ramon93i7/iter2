import unittest

import iter2.algorithms.searching as algo


class TestSearchingAlgorithms(unittest.TestCase):
    def test_find(self):
        with self.subTest('found'):
            self.assertEqual(
                algo.find('aBc', lambda c: c.isupper()),
                'B'
            )

        with self.subTest('not found'):
            with self.assertRaises(StopIteration):
                algo.find('abc', lambda c: c.isupper())


    def test_locate(self):
        with self.subTest('w/o items'):
            self.assertEqual(
                tuple(algo.locate('aBcDe', str.isupper, count_from=1)),
                (2, 4)
            )

        with self.subTest('w/ items'):
            self.assertEqual(
                tuple(algo.locate('aBcDe', str.isupper, count_from=1, with_items=True)),
                ((2, 'B'), (4, 'D'))
            )

        with self.subTest('not found'):
            self.assertEqual(
                tuple(algo.locate('abcde', str.isupper, count_from=1)),
                ()
            )

    def test_position(self):
        with self.subTest('found'):
            self.assertEqual(
                algo.position('aBcDe', str.isupper, count_from=1),
                2
            )

        with self.subTest('not found'):
            self.assertEqual(
                algo.position('abcde', str.isupper, count_from=1),
                -1
            )
