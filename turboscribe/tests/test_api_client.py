import unittest
from unittest.mock import MagicMock, patch

from turboscribe.api_client import TurboScribeClient, TurboScribeError


class TestTurboScribeClient(unittest.TestCase):
    def setUp(self):
        self.client = TurboScribeClient(api_key="test_key")

    @patch("requests.request")
    def test_upload_file(self, mock_request):
        mock_request.return_value = MagicMock(
            status_code=200, json=lambda: {"transcript_id": "12345"}
        )
        response = self.client.upload_file("path/to/file.mp3")
        self.assertEqual(response["transcript_id"], "12345")

    # Example test for TurboScribeError
    @patch("requests.request")
    def test_api_error_handling(self, mock_request):
        # Simulate an API error response
        mock_request.side_effect = Exception("API request failed")
        with self.assertRaises(TurboScribeError):
            self.client.upload_file("./file.mp3")

