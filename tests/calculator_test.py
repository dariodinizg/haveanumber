# Standard Library imports
import sys
import subprocess
import unittest
from decimal import Decimal

# Local application imports
from src.calculator import FinancialCalculator



class FinancialCalculatorTest(unittest.TestCase):
    
    @classmethod
    def setUp(self):
        self.payload = {
            "current_age": 30,
            "goal_age": 60,
            "goal_monthly_withdraw": 3500,
            "initial_patrimony": 100000,
            "monthly_contribution": 100,
            "current_interest": 4.91,
            "future_interest":"7,5",
            "max_age": 80
        }
        
        self.payload2 = {
            "current_age": 29,
            "goal_age": 60,
            "goal_monthly_withdraw": 2500,
            "initial_patrimony": 100000,
            "monthly_contribution": 1450,
            "current_interest": "8,73",
            "future_interest":6,
            "max_age": 70
        }

        self.data = FinancialCalculator(**self.payload)
        self.data2 = FinancialCalculator(**self.payload2)

    def test_decimal_current_yield(self):
        self.assertEqual(self.data.decimal_current_yield, Decimal("0.0491"))
        self.assertEqual(self.data2.decimal_current_yield, Decimal("0.0873"))

    def test_decimal_future_yield(self):
        self.assertEqual(self.data.decimal_future_yield, Decimal("0.075"))
        self.assertEqual(self.data2.decimal_future_yield, Decimal("0.06"))

    def test_convert_to_monthly_interest(self):
        self.assertEqual(self.data.monthly_yield_current, Decimal("0.0040024"))
        self.assertEqual(self.data2.monthly_yield_current, Decimal("0.0069992"))

    def test_contribution_years(self):
        self.assertEqual(self.data.contribution_years, 30)

    def test_contribution_months(self):
        self.assertEqual(self.data.contribution_months, 30 * 12)

    def test_monthly_yield_current(self):
        self.assertEqual(self.data.monthly_yield_current, Decimal("0.0040024"))
        self.assertEqual(self.data2.monthly_yield_current, Decimal("0.0069992"))
    
    def test_monthly_yield_goal(self):
        self.assertEqual(self.data.monthly_yield_goal, Decimal("0.0060449"))
        self.assertEqual(self.data2.monthly_yield_goal, Decimal("0.0048676"))

    def test_infinity_patrimony_value(self):
        # delta = 0.05
        self.assertAlmostEqual(self.data.infinity_patrimony_value, Decimal("579000.48"))
        self.assertAlmostEqual(self.data2.infinity_patrimony_value, Decimal("513600.13"))

    def test_consumable_patrimony_value(self):
        delta = 1
        self.assertAlmostEqual(self.data.consumable_patrimony_value, Decimal("442694.76"), delta=delta)
        self.assertAlmostEqual(self.data2.consumable_patrimony_value, Decimal("226810.80"), delta=delta)

    # @unittest.skip("")
    # def test_zero_division_error(self):
    #     pass

    # @unittest.skip("")
    # def test_negative_division_error(self):
    #     pass

    def test_payment_value(self):
        delta = 0.05
        amount = 236437.13
        period = 360 #months
        interest = 0.007974140429 #by month
        self.assertAlmostEqual(self.data.payment_value(amount, interest, period), Decimal('114.62'))

    def test_present_value(self):
        delta = 1
        
        case1 = {
            "payment": 2500,
            "interest": 0.0070, 
            "period": 120,
        }
        with self.subTest(case1=case1):
            self.assertAlmostEqual(self.data.present_value(**case1), Decimal("202508.67"), delta=delta)

        case2 = {
            "payment": 3500,
            "interest": 0.004, 
            "period": 240, 
        }
        with self.subTest(case2=case2):
            self.assertAlmostEqual(self.data.present_value(**case2), Decimal("539326.56"), delta=delta)
        
        case3 = {
            "payment": 3500,
            "interest": 0.0060449, 
            "period": 240, 
        }
        self.assertAlmostEqual(self.data.present_value(**case3), Decimal("442694.76"), delta=delta)


# instead of writting python -m unittest test_name
if __name__ == "__main__":
    unittest.main()

