import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def test_canCalculate(self):
        calculator = Calculator()
        self.assertTrue(calculator.isValidExpression("3 + 3"))
        self.assertTrue(calculator.isValidExpression("a = 3"))
        self.assertFalse(calculator.isValidExpression("a = oaue3"))

        calculations = [
            ("5 + 5", "10"),
            ("sin(90)", "1"),
            ("a = 3", "3"),
            ("a*3", "9"),
            ("timesTwo(x) = x*2", "Declared!"),
            ("timesTwo(a)", "6")
        ]

        for calc, result in calculations:
            calculator.executeExpression(calc)
            self.assertEqual(calculator.getExpressions()[-1]['result'], result)

if __name__ == '__main__':
    unittest.main()
