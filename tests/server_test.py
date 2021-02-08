import unittest
import requests

# from src.server import app

class ServerTest(unittest.TestCase):

    url = "http://127.0.0.1:5000/"
    def test_server_running(self):
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_main(self):
        endpoint = self.url + "calculator"
        post_body = {
            "current_age": "30",
            "goal_age": "60",
            "goal_monthly_withdraw": "3500",
            "initial_patrimony": "100000",
            "monthly_contribution": "100",
            "current_interest": "4.91",
            "future_interest":"7,5",
            "max_age": "80"
        }
        response = requests.post(endpoint, data=post_body)
        self.assertEqual(response.text,post_body)


if __name__ == "__main__":
    unittest.main()