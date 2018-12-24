import unittest

import iter2.algorithms.splitting as algo


class TestSplittingAlgorithms(unittest.TestCase):
    def assertEqualAfterMaterialize(self, first, second):
        self.assertEqual(
            tuple(map(tuple, first)),
            tuple(second)
        )

    def test_distribute(self):
        with self.subTest('simple'):
            self.assertEqualAfterMaterialize(
                algo.distribute([1, 2, 3, 4, 5], 3),
                ((1, 4), (2, 5), (3,))
            )

    def test_partition(self):
        with self.subTest('simple'):
            self.assertEqualAfterMaterialize(
                algo.partition('AbCd', str.isupper),
                (('A', 'C'), ('b', 'd'))
            )

    def test_split_after(self):
        with self.subTest('simple'):
            self.assertEqualAfterMaterialize(
                algo.split_after('192.168.0.1', lambda c: c == '.'),
                map(tuple, ('192.', '168.', '0.', '1'))
            )

    def test_split_at(self):
        with self.subTest('simple'):
            self.assertEqualAfterMaterialize(
                algo.split_at('192.168.0.1', lambda c: c == '.'),
                map(tuple, ('192', '168', '0', '1'))
            )

    def test_split_before(self):
        with self.subTest('simple'):
            self.assertEqualAfterMaterialize(
                algo.split_before('192.168.0.1', lambda c: c == '.'),
                map(tuple, ('192', '.168', '.0', '.1'))
            )

    def test_unzip(self):
        with self.subTest('simple'):
            self.assertEqualAfterMaterialize(
                algo.unzip([(1, 2), (3, 4)]),
                ((1, 3), (2, 4))
            )

        with self.subTest('custom arity'):
            self.assertEqualAfterMaterialize(
                algo.unzip([(1, 2, 3), (4, 5, 6)], arity=3),
                ((1, 4), (2, 5), (3, 6))
            )
