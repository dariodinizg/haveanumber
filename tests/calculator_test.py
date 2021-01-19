# Standard Library imports
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
            "goal_monthly_withdraw": 2500,
            "initial_patrimony": 100000,
            "monthly_contribution": 100,
            "current_interest": 9,
            "future_interest":6,
            "max_age": 95
        }
        self.payload2 = {
            "current_age": 29,
            "goal_age": 55,
            "goal_monthly_withdraw": 3000,
            "initial_patrimony": 100000,
            "monthly_contribution": 1450,
            "current_interest": 7,
            "future_interest":5,
            "max_age": 95
        }
        # self.payload3 = {
        #     "current_age": 30,
        #     "goal_age": 60,
        #     "goal_monthly_withdraw": 2500,
        #     "initial_patrimony": 100000,
        #     "monthly_contribution": 100,
        #     "rentabilidade_media": 0.09,
        #     "max_age": 95
        # }        

        self.data = FinancialCalculator(**self.payload)
        self.data2 = FinancialCalculator(**self.payload2)

    def test_contribution_years(self):
        self.assertEqual(self.data.contribution_years, 30)
        self.assertEqual(self.data2.contribution_years, 26)

    def test_contribution_months(self):
        self.assertEqual(self.data.contribution_months, 30 * 12)
        self.assertEqual(self.data2.contribution_months, 26 * 12)

    def test_monthly_yield_current(self):
        self.assertEqual(self.data.monthly_yield_current, Decimal("0.007207"))
    
    def test_monthly_yield_goal(self):
        self.assertEqual(self.data.monthly_yield_goal, Decimal("0.004868"))

    def test_profitable_patrimony_value(self):
        delta = 0.05
        two_places = 2

        self.assertAlmostEqual(self.data.profitable_patrimony_value, Decimal("513557.93"), delta=delta)
        self.assertAlmostEqual(self.data2.profitable_patrimony_value, Decimal("736377.02"), delta=delta)

    @unittest.skip("")
    def test_zero_division_error(self):
        pass

    @unittest.skip("")
    def test_negative_division_error(self):
        pass


# instead of writting python -m unittest test_name
if __name__ == "__main__":
    unittest.main()