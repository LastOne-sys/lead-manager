import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from openai import APIConnectionError

from api import app


class TestSummaryAPI(unittest.TestCase):
    def test_returns_summary(self):
        with patch("api.summarize_lead") as mock_summary:
            mock_summary.return_value = "Automate email processing."

            with TestClient(app) as client:
                response = client.post(
                    "/leads/summarize",
                    json={
                        "name": "Alex",
                        "email": "alex@example.com",
                        "message": "Please automate our emails.",
                    },
                )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json(),
                {"summary": "Automate email processing."},
            )
            mock_summary.assert_called_once_with(
                "Please automate our emails."
            )

    def test_returns_502_when_ai_is_unavailable(self):
        with patch("api.summarize_lead") as mock_summary:
            mock_summary.side_effect = APIConnectionError(request=None)

            with TestClient(app) as client:
                response = client.post(
                    "/leads/summarize",
                    json={
                        "name": "Alex",
                        "email": "alex@example.com",
                        "message": "Please automate our emails.",
                    },
                )

            self.assertEqual(response.status_code, 502)
            self.assertEqual(
                response.json(),
                {
                    "detail": (
                        "AI service unavailable. Please try again later."
                    )
                },
            )


if __name__ == "__main__":
    unittest.main()