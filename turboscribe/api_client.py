import os
from typing import Any, Dict

import requests
from requests.exceptions import RequestException


class TurboScribeError(Exception):
    """Custom exception for TurboScribe errors."""

    pass


class TurboScribeClient:
    """
    Client to interact with TurboScribe's website manually through HTTP requests.

    Attributes:
        session (requests.Session): Session to maintain cookies and headers.
    """

    LOGIN_URL = "https://turboscribe.ai/login"
    UPLOAD_URL = "https://turboscribe.ai/upload"
    TRANSCRIPT_URL = "https://turboscribe.ai/transcripts/"

    def __init__(self):
        self.session = requests.Session()
        self.username = os.getenv("TURBOSCRIBE_USERNAME")
        self.password = os.getenv("TURBOSCRIBE_PASSWORD")
        if not self.username or not self.password:
            raise TurboScribeError(
                "Username and password environment variables are required."
            )
        self.is_authenticated = False

    def login(self):
        """Logs in to establish a session."""
        try:
            response = self.session.post(
                self.LOGIN_URL,
                data={"username": self.username, "password": self.password},
            )
            response.raise_for_status()
            if "authentication failed" in response.text.lower():
                raise TurboScribeError("Login failed. Check your credentials.")
            self.is_authenticated = True
        except RequestException as e:
            raise TurboScribeError(f"Login failed: {e}")

    def upload_file(self, file_path: str) -> Dict[str, Any]:
        """Uploads a file for transcription."""
        if not self.is_authenticated:
            self.login()

        try:
            with open(file_path, "rb") as file:
                response = self.session.post(self.UPLOAD_URL, files={"file": file})
                response.raise_for_status()
                return response.json()  # Assuming JSON response format
        except FileNotFoundError:
            raise TurboScribeError(f"File {file_path} not found.")
        except RequestException as e:
            raise TurboScribeError(f"File upload failed: {e}")

    def get_transcript_metadata(self, transcript_id: str) -> Dict[str, Any]:
        """Retrieves metadata for a specific transcript."""
        if not self.is_authenticated:
            self.login()

        try:
            response = self.session.get(
                f"{self.TRANSCRIPT_URL}/{transcript_id}/metadata"
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            raise TurboScribeError(f"Metadata retrieval failed: {e}")

    def delete_transcript(self, transcript_id: str) -> Dict[str, Any]:
        """Deletes a specific transcript."""
        if not self.is_authenticated:
            self.login()

        try:
            response = self.session.delete(f"{self.TRANSCRIPT_URL}/{transcript_id}")
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            raise TurboScribeError(f"Deletion failed: {e}")
