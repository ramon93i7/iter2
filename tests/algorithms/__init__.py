import unittest

from .extra import TestExtraAlgorithms
from .folding import TestFoldingAlgorithms
from .merging import TestMergingAlgorithms
from .predicate_on_sequence import TestPredicateOnSequenceAlgorithms
from .searching import TestSearchingAlgorithms
from .sequence_to_groups import TestSequenceToGroupsAlgorithms
from .sequence_to_sequence import TestSequenceToSequenceAlgorithms
from .splitting import TestSplittingAlgorithms


def get_algorithms_test_suite():
    suite = unittest.TestSuite()
    suite.addTests(
        map(
            unittest.defaultTestLoader.loadTestsFromTestCase, (
                TestExtraAlgorithms,
                TestFoldingAlgorithms,
                TestMergingAlgorithms,
                TestPredicateOnSequenceAlgorithms,
                TestSearchingAlgorithms,
                TestSequenceToGroupsAlgorithms,
                TestSequenceToSequenceAlgorithms,
                TestSplittingAlgorithms
            )
        )
    )
    return suite

__all__ = ['get_algorithms_test_suite']
