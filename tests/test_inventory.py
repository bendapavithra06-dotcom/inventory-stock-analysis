import unittest

class InventoryRuleTests(unittest.TestCase):
    def test_stock_calculation(self):
        opening_stock = 20
        stock_in = 10
        stock_out = 7
        self.assertEqual(opening_stock + stock_in - stock_out, 23)

    def test_stock_must_not_become_negative(self):
        current_stock = 5
        requested_out = 6
        self.assertGreater(requested_out, current_stock)

if __name__ == "__main__":
    unittest.main()
