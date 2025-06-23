import calculator
import unittest

class TestCalculator(unittest.TestCase):

    def test_add(self):
        print("Running test_add")
        self.assertEqual(calculator.add(1, 2), 3)
        self.assertEqual(calculator.add(-1, 1), 0)
        self.assertEqual(calculator.add(-1, -1), -2)

    def test_subtract(self):
        print("Running test_subtract")
        self.assertEqual(calculator.subtract(5, 2), 3)
        self.assertEqual(calculator.subtract(2, 5), -3)
        self.assertEqual(calculator.subtract(-1, -1), 0)

    def test_multiply(self):
        print("Running test_multiply")
        self.assertEqual(calculator.multiply(2, 3), 6)
        self.assertEqual(calculator.multiply(-2, 3), -6)
        self.assertEqual(calculator.multiply(-2, -3), 6)

    def test_divide(self):
        print("Running test_divide")
        self.assertEqual(calculator.divide(6, 2), 3)
        self.assertEqual(calculator.divide(-6, 2), -3)
        self.assertEqual(calculator.divide(6, -2), -3)
        self.assertEqual(calculator.divide(5, 2), 2.5)

    def test_divide_by_zero(self):
        print("Running test_divide_by_zero")
        self.assertEqual(calculator.divide(5, 0), "Cannot divide by zero")

if __name__ == '__main__':
    unittest.main()