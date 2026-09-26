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
                {"detail": "AI service unavailable. Please try again later."},
            )

    def test_saved_summary_does_not_call_ai(self):
        lead = {
            "id": "lead-1",
            "name": "Alex",
            "email": "alex@example.com",
            "message": "Please automate our emails.",
            "summary": "Automate email processing.",
        }

        with (
            patch("api.load_leads", return_value=[lead]),
            patch("api.summarize_lead") as mock_summary,
            patch("api.save_leads") as mock_save,
        ):
            with TestClient(app) as client:
                response = client.post("/leads/lead-1/summary")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), lead)
            mock_summary.assert_not_called()
            mock_save.assert_not_called()

    def test_missing_lead_returns_404_without_calling_ai(self):
        with (
            patch("api.load_leads", return_value=[]),
            patch("api.summarize_lead") as mock_summary,
            patch("api.save_leads") as mock_save,
        ):
            with TestClient(app) as client:
                response = client.post("/leads/missing-id/summary")

            self.assertEqual(response.status_code, 404)
            self.assertEqual(
                response.json(),
                {"detail": "Lead not found."},
            )
            mock_summary.assert_not_called()
            mock_save.assert_not_called()

    def test_generates_and_saves_summary(self):
        lead = {
            "id": "lead-1",
            "name": "Alex",
            "email": "alex@example.com",
            "message": "Please automate our emails.",
        }
        expected_lead = {
            **lead,
            "summary": "Automate email processing.",
        }

        with (
            patch("api.load_leads", return_value=[lead]),
            patch("api.summarize_lead") as mock_summary,
            patch("api.save_leads") as mock_save,
        ):
            mock_summary.return_value = "Automate email processing."

            with TestClient(app) as client:
                response = client.post("/leads/lead-1/summary")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), expected_lead)
            mock_summary.assert_called_once_with(
                "Please automate our emails."
            )
            mock_save.assert_called_once_with([expected_lead])


if __name__ == "__main__":
    unittest.main()