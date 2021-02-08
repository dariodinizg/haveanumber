import unittest
import requests
import json

# from src.server import app

class ServerTest(unittest.TestCase):

    def setUp(self):
        self.post_body = {
            "current_age": "30",
            "goal_age": "60",
            "goal_monthly_withdraw": "3500",
            "initial_patrimony": "100000",
            "monthly_contribution": "100",
            "current_interest": "4.91",
            "future_interest":"7,5",
            "max_age": "80"
        }
        self.url = "http://127.0.0.1:5000/"
        self.response = requests.post(self.url, data=self.post_body)

    def test_server_running(self):
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_post_body(self):
    #     response_proof = {
    #     "decimal_current_yield": ,
    #     "decimal_future_yield": ,
    #     "monthly_yield_current": ,
    #     "monthly_yield_goal": ,
    #     "contribution_years": ,
    #     "contribution_months": ,
    #     "consumption_months": ,
    #     "consumable_patrimony_value": ,
    #     "infinity_patrimony_value": ,
    # }
        self.assertEqual(self.response.text, "")


if __name__ == "__main__":
    unittest.main()