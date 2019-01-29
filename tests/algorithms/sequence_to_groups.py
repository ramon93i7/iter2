import unittest

import iter2.algorithms.sequence_to_groups as algo


class TestSequenceToGroupsAlgorithms(unittest.TestCase):
    def assertEqualAsTuples(self, first, second):
        self.assertEqual(
            tuple(first),
            tuple(second)
        )

    def test_chunks(self):
        with self.subTest('only complete'):
            self.assertEqualAsTuples(
                algo.chunks([1, 2, 3, 4], 2),
                ((1, 2), (3, 4))
            )

        with self.subTest('last incomplete'):
            self.assertEqualAsTuples(
                algo.chunks([1, 2, 3], 2),
                ((1, 2),)
            )

        with self.subTest('last incomplete but `allow_partial`'):
            self.assertEqualAsTuples(
                algo.chunks([1, 2, 3], 2, allow_partial=True),
                ((1, 2), (3,))
            )

    def test_chunks_with_padding(self):
        with self.subTest('only complete'):
            self.assertEqualAsTuples(
                algo.chunks_with_padding([1, 2, 3, 4], 2),
                ((1, 2), (3, 4))
            )

        with self.subTest('last incomplete'):
            self.assertEqualAsTuples(
                algo.chunks_with_padding([1, 2, 3], 2),
                ((1, 2), (3, None))
            )

        with self.subTest('last incomplete w/ custom `fillvalue`'):
            self.assertEqualAsTuples(
                algo.chunks_with_padding([1, 2, 3], 2, fillvalue=100500),
                ((1, 2), (3, 100500))
            )

    def test_consecutive_groups(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                map(tuple,
                    algo.consecutive_groups([1, 2, 10, 11, 100, 101])
                ),
                ((1, 2), (10, 11), (100, 101))
            )

        with self.subTest('custom `ordering`'):
            self.assertEqualAsTuples(
                map(tuple,
                    algo.consecutive_groups('abcBCDcde', ordering=ord)
                ),
                (('a', 'b', 'c'), ('B', 'C', 'D'), ('c', 'd', 'e'))
            )

    def test_group_by(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                (
                    (key, tuple(group))
                    for key, group in algo.group_by([1, 2, 2, 3, 3, 3])
                ),
                ((1, (1,)), (2, (2, 2)), (3, (3, 3, 3)))
            )

        with self.subTest('w/ key'):
            self.assertEqualAsTuples(
                (
                    (key, tuple(group))
                    for key, group in algo.group_by([1, 2, 2, 3, 3, 3])
                ),
                ((1, (1,)), (2, (2, 2)), (3, (3, 3, 3)))
            )

    def test_pairwise(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.pairwise([1, 2, 3]),
                ((1, 2), (2, 3))
            )

    def test_permutations(self):
        with self.subTest('n=2'):
            self.assertEqualAsTuples(
                algo.permutations([0, 1], length=2),
                ((0, 1), (1, 0))
            )

        with self.subTest('n=2'):
            self.assertEqualAsTuples(
                algo.permutations([0, 1, 2], length=2),
                ((0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1))
            )

    def test_process_in_groups(self):
        materialize = lambda it: tuple((key, tuple(val)) for key, val in it)

        with self.subTest('"group_by"'):
            self.assertEqual(
                materialize(
                    algo.process_in_groups([1, 2, 2, 3, 3, 3], key=lambda x: x % 2)
                ),
                ((1, (1,)), (0, (2, 2)), (1, (3, 3, 3)))
            )

        with self.subTest('w/ transformation'):
            self.assertEqual(
                materialize(
                    algo.process_in_groups([1, 2, 2, 3, 3, 3], transformation=lambda x: x % 2)
                ),
                ((1, (1,)), (2, (0, 0)), (3, (1, 1, 1)))
            )

        with self.subTest('w/ aggregator'):
            self.assertEqualAsTuples(
                algo.process_in_groups([1, 2, 2, 3, 3, 3], aggregator=sum),
                ((1, 1), (2, 4), (3, 9))
            )

    def test_sliding_window(self):
        with self.subTest('"chunks"; `allow_partial` is False"'):
            self.assertEqualAsTuples(
                map(tuple,
                    algo.sliding_window([1, 2, 3, 4, 5], size=2, step=2),
                ),
                ((1, 2), (3, 4))
            )

        with self.subTest('"chunks"; `allow_partial` is True'):
            self.assertEqualAsTuples(
                map(tuple,
                    algo.sliding_window([1, 2, 3, 4, 5], size=2, step=2, allow_partial=True),
                ),
                ((1, 2), (3, 4), (5,))
            )

        with self.subTest('overlapping'):
            self.assertEqualAsTuples(
                map(tuple,
                    algo.sliding_window([1, 2, 3, 4, 5], size=2, step=1),
                ),
                ((1, 2), (2, 3), (3, 4), (4, 5))
            )

        with self.subTest('wide step'):
            self.assertEqualAsTuples(
                map(tuple,
                    algo.sliding_window([1, 2, 3, 4, 5], size=2, step=3),
                    ),
                ((1, 2), (4, 5))
            )

    def test_stagger(self):
        with self.subTest('simple'):
            self.assertEqualAsTuples(
                algo.stagger([0, 1, 2, 3]),
                ((None, 0, 1), (0, 1, 2), (1, 2, 3))
            )

        with self.subTest('custom `offsets`'):
           self.assertEqualAsTuples(
                algo.stagger([0, 1, 2, 3, 4, 5, 6, 7], offsets=(0, 2, 4)),
                ((0, 2, 4), (1, 3, 5), (2, 4, 6), (3, 5, 7))
           )

        with self.subTest('w/ `longest`'):
            self.assertEqualAsTuples(
                algo.stagger([0, 1, 2, 3], longest=True),
                ((None, 0, 1), (0, 1, 2), (1, 2, 3), (2, 3, None), (3, None, None))
            )
