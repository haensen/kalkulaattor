import unittest
from expression import Expression

class TestExpression(unittest.TestCase):
    def test_canReturnGivenExpression(self):
        self.assertEqual(Expression("1 + 1").asString(), "1 + 1")
        self.assertEqual(Expression("1 + 5").asString(), "1 + 5")
    
    def test_validatesExpressions(self):
        self.assertTrue(Expression("1 + 1").isValid())
        self.assertTrue(Expression("1 + 5").isValid())
        self.assertTrue(Expression("1 * 1").isValid())
        self.assertTrue(Expression("1 / 50").isValid())
        self.assertTrue(Expression("(5) * 3 - 7").isValid())
        self.assertTrue(Expression("1000 / (353 + 32)").isValid())
        self.assertFalse(Expression("1000 / 353 + 32)").isValid())
        self.assertFalse(Expression("aoeuaoeu***").isValid())
        self.assertFalse(Expression("100 / 0").isValid())
    
    def test_returnsCorrectResult(self):
        self.assertAlmostEqual(Expression("1 + 1").result(), 2)
        self.assertAlmostEqual(Expression("1 + 5").result(), 6)
        self.assertAlmostEqual(Expression("100 / 5").result(), 20)
        self.assertAlmostEqual(Expression("3 * 3 / 10").result(), 0.9)

if __name__ == '__main__':
    unittest.main()
