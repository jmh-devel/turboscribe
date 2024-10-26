import unittest
from unittest.mock import MagicMock, patch

from turboscribe.api_client import TurboScribeClient, TurboScribeError


class TestTurboScribeClient(unittest.TestCase):
    def setUp(self):
        self.client = TurboScribeClient(username="test_user", password="test_pass")

    @patch("requests.Session.post")
    def test_login(self, mock_post):
        mock_post.return_value = MagicMock(status_code=200)
        self.client.login()
        self.assertTrue(self.client.is_authenticated)

    @patch("requests.Session.post")
    def test_upload_file(self, mock_post):
        mock_post.return_value = MagicMock(status_code=200, json=lambda: {"transcript_id": "12345"})
        response = self.client.upload_file("turboscribe/tests/resources/sample.mp3")
        self.assertEqual(response["transcript_id"], "12345")

    # Example test for TurboScribeError
    @patch("requests.request")
    def test_api_error_handling(self, mock_request):
        # Simulate an API error response
        mock_request.side_effect = Exception("API request failed")
        with self.assertRaises(TurboScribeError):
            self.client.upload_file("./file.mp3")
