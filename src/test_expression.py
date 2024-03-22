import unittest
import math
from expression import Expression, ExpressionType

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
        self.assertFalse(Expression("abs()").isValid())
        self.assertFalse(Expression("abs").isValid())
        self.assertFalse(Expression("grandma()").isValid())
    
    def test_returnsCorrectResult(self):
        self.assertAlmostEqual(Expression("1 + 1").result(), 2)
        self.assertAlmostEqual(Expression("1 + 5").result(), 6)
        self.assertAlmostEqual(Expression("100 / 5").result(), 20)
        self.assertAlmostEqual(Expression("3 * 3 / 10").result(), 0.9)
    
    def test_canUseBasicFunctions(self):
        self.assertAlmostEqual(Expression("abs(-3)").result(), 3)
        self.assertAlmostEqual(Expression("abs(3)").result(), 3)
        self.assertAlmostEqual(Expression("sin(0)").result(), 0)
        self.assertAlmostEqual(Expression("sin(90)").result(), 1)
    
    def test_detectsCalculationType(self):
        self.assertEqual(Expression("1+5").type(), ExpressionType.CALCULATION)
        self.assertEqual(Expression("abs(3) - 7").type(), ExpressionType.CALCULATION)
        self.assertEqual(Expression("dog = 3").type(), ExpressionType.VARIABLE_ASSIGNMENT)
        self.assertEqual(Expression("cat = 3 * 3515").type(), ExpressionType.VARIABLE_ASSIGNMENT)
    
    def test_canAssignVariables(self):
        self.assertEqual(Expression("dog = 3").result(), ("dog", 3))
        self.assertEqual(Expression("cat = -5").result(), ("cat", -5))
    
    def test_canUseVariables(self):
        self.assertAlmostEqual(Expression("dog * 3", {"dog": 3}).result(), 9)
        self.assertAlmostEqual(Expression("dog * sin(cat)", {"dog": 5, "cat": 30}).result(), 2.5)

if __name__ == '__main__':
    unittest.main()
