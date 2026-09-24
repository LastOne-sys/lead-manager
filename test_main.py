import unittest

from main import search_leads, update_lead_status


class TestSearchLeads(unittest.TestCase):
    def test_search_ignores_case(self):
        leads = [
            {"email": "alex@example.com"},
            {"email": "sam@example.com"},
        ]

        result = search_leads(leads, "ALEX@EXAMPLE.COM")

        self.assertEqual(result, [{"email": "alex@example.com"}])

    def test_search_returns_empty_when_not_found(self):
        leads = [
            {"email": "alex@example.com"},
        ]

        result = search_leads(leads, "missing@example.com")

        self.assertEqual(result, [])
class TestUpdateLeadStatus(unittest.TestCase):
    def test_updates_only_matching_lead(self):
        leads = [
            {"id": "lead-1", "status": "new"},
            {"id": "lead-2", "status": "new"},
        ]

        result = update_lead_status(leads, "lead-2", "contacted")

        self.assertTrue(result)
        self.assertEqual(leads[0]["status"], "new")
        self.assertEqual(leads[1]["status"], "contacted")

    def test_unknown_id_does_not_change_leads(self):
        leads = [
            {"id": "lead-1", "status": "new"},
        ]

        result = update_lead_status(leads, "missing-id", "contacted")

        self.assertFalse(result)
        self.assertEqual(leads, [{"id": "lead-1", "status": "new"}])
if __name__ == "__main__":
    unittest.main()