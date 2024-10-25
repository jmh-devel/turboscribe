import unittest
from turboscribe.api_client import TurboScribeClient, TurboScribeError
from unittest.mock import patch, MagicMock

class TestTurboScribeClient(unittest.TestCase):

    def setUp(self):
        self.client = TurboScribeClient(api_key="test_key")

    @patch("requests.request")
    def test_upload_file(self, mock_request):
        mock_request.return_value = MagicMock(status_code=200, json=lambda: {"transcript_id": "12345"})
        response = self.client.upload_file("path/to/file.mp3")
        self.assertEqual(response["transcript_id"], "12345")

    @patch("requests.request")
    def test_upload_url(self, mock_request):
        mock_request.return_value = MagicMock(status_code=200, json=lambda: {"transcript_id": "12345"})
        response = self.client.upload_url("http://example.com/audio.mp3")
        self.assertEqual(response["transcript_id"], "12345")

    # More tests as needed for other methods
