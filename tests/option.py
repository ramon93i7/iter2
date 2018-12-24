import unittest

from iter2.option import None2, Some2


class TestOption2(unittest.TestCase):
    def test_bool(self):
        with self.subTest('Some'):
            self.assertTrue(Some2(1))
        with self.subTest('None'):
            self.assertFalse(None2)

    def test_expect(self):
        with self.subTest('Some'):
            self.assertEqual(Some2(1).expect(RuntimeError), 1)
        with self.subTest('None'):
            with self.assertRaises(RuntimeError):
                None2.expect(RuntimeError, 'lol')

    def test_is_some(self):
        with self.subTest('Some'):
            self.assertTrue(Some2(1).is_some())
        with self.subTest('None'):
            self.assertFalse(None2.is_some())

    def test_is_none(self):
        with self.subTest('Some'):
            self.assertFalse(Some2(1).is_none())
        with self.subTest('None'):
            self.assertTrue(None2.is_none())

    def test_unwrap(self):
        with self.subTest('Some'):
            self.assertEqual(Some2(1).unwrap(), 1)
        with self.subTest('None'):
            with self.assertRaises(RuntimeError):
                None2.unwrap()

    def test_unwrap_or(self):
        with self.subTest('Some'):
            self.assertEqual(Some2(1).unwrap_or(2), 1)
        with self.subTest('None'):
            self.assertEqual(None2.unwrap_or(2), 2)

    def test_unwrap_or_else(self):
        with self.subTest('Some'):
            self.assertEqual(Some2(1).unwrap_or_else(lambda: 2), 1)
        with self.subTest('None'):
            self.assertEqual(None2.unwrap_or_else(lambda: 2), 2)

    def test_map(self):
        with self.subTest('Some'):
            self.assertEqual(Some2(-1).map(abs).unwrap(), 1)
        with self.subTest('None'):
            self.assertTrue(None2.map(abs).is_none())

    def test_map_or(self):
        with self.subTest('Some'):
            self.assertEqual(Some2(-1).map_or(2, abs), 1)
        with self.subTest('None'):
            self.assertEqual(None2.map_or(2, abs), 2)

    def test_map_or_else(self):
        with self.subTest('Some'):
            self.assertEqual(Some2(-1).map_or_else(lambda: 2, abs), 1)
        with self.subTest('None'):
            self.assertEqual(None2.map_or_else(lambda: 2, abs), 2)

    def test_and(self):
        with self.subTest('Some'):
            self.assertEqual(
                (Some2(object()) & Some2(1)).unwrap(),
                1
            )
        with self.subTest('None'):
            self.assertTrue(
                None2.and_(object()).is_none()
            )

    def test_and_then(self):
        with self.subTest('Some'):
            self.assertEqual(
                Some2(object()).and_then(lambda: Some2(1)).unwrap(),
                1
            )
        with self.subTest('None'):
            self.assertTrue(
                None2.and_then(lambda: Some2(object())).is_none()
            )

    def test_filter(self):
        with self.subTest('Some :: true'):
            self.assertEqual(Some2(1).filter(bool).unwrap(), 1)
        with self.subTest('Some :: false'):
            self.assertTrue(Some2(0).filter(bool).is_none())
        with self.subTest('None'):
            self.assertTrue(None2.filter(bool).is_none())

    def test_or(self):
        with self.subTest('Some'):
            self.assertEqual(
                Some2(1).or_(Some2(object())).unwrap(),
                1
            )
        with self.subTest('None'):
            self.assertEqual(None2 | 1, 1)

    def test_or_else(self):
        with self.subTest('Some'):
            self.assertEqual(
                Some2(1).or_else(lambda: Some2(object())).unwrap(),
                1
            )
        with self.subTest('None'):
            self.assertEqual(None2.or_else(lambda: 1), 1)

    def test_xor(self):
        with self.subTest('Some ^ Some'):
            self.assertTrue(
                Some2(1).xor(Some2(2)).is_none()
            )
        with self.subTest('Some ^ None'):
            self.assertEqual(
                Some2(1).xor(None2).unwrap(),
                1
            )
        with self.subTest('None ^ Some'):
            self.assertTrue(
                None2.xor(Some2(2)).unwrap(),
                2
            )
        with self.subTest('None ^ None'):
            self.assertTrue(
                None2.xor(None2).is_none()
            )
