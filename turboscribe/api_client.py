import requests
from typing import Optional, Dict, Any, List

class TurboScribeError(Exception):
    """Custom exception for TurboScribe API errors."""
    pass

class TurboScribeClient:
    """
    Client to interact with the TurboScribe transcription API.

    Attributes:
        api_key (str): API key for authenticating with the TurboScribe API.
    """
    
    BASE_URL = "https://api.turboscribe.ai"
    
    def __init__(self, api_key: str):
        """
        Initializes the TurboScribeClient with an API key.
        
        Parameters:
            api_key (str): API key for authenticating with the TurboScribe API.
        """
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Internal method to handle API requests.
        
        Parameters:
            method (str): HTTP method (e.g., 'GET', 'POST', 'DELETE').
            endpoint (str): API endpoint (e.g., '/api/upload').
            kwargs: Additional arguments for the request (e.g., params, data, files).
        
        Returns:
            Dict[str, Any]: JSON response data.
        
        Raises:
            TurboScribeError: If the request fails or returns an error response.
        """
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise TurboScribeError(f"API request failed: {e}")

    def upload_file(self, file_path: str, language: Optional[str] = None, recognize_speakers: bool = False, mode: Optional[str] = None) -> Dict[str, Any]:
        """
        Uploads a file for transcription.

        Parameters:
            file_path (str): Path to the audio or video file.
            language (Optional[str]): Language of the transcription.
            recognize_speakers (bool): If True, enables speaker recognition.
            mode (Optional[str]): Transcription mode (Cheetah, Dolphin, Whale).

        Returns:
            Dict[str, Any]: Response containing the transcript ID.
        """
        files = {'file': open(file_path, 'rb')}
        data = {
            "language": language,
            "recognize_speakers": recognize_speakers,
            "mode": mode
        }
        return self._request("POST", "/api/upload", files=files, data=data)

    def upload_url(self, url: str) -> Dict[str, Any]:
        """
        Uploads a URL for transcription.

        Parameters:
            url (str): URL of the audio or video file.

        Returns:
            Dict[str, Any]: Response containing the transcript ID.
        """
        data = {"url": url}
        return self._request("POST", "/api/upload/url", json=data)

    def list_recent_transcripts(self, limit: Optional[int] = 100, next_page: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Lists recent transcripts.

        Parameters:
            limit (Optional[int]): Maximum number of transcripts to fetch.
            next_page (Optional[str]): Pagination token.

        Returns:
            List[Dict[str, Any]]: List of transcripts with metadata.
        """
        params = {"limit": limit, "next_page": next_page}
        return self._request("GET", "/api/transcripts", params=params)

    def get_transcript_metadata(self, transcript_id: str) -> Dict[str, Any]:
        """
        Retrieves metadata for a specific transcript.

        Parameters:
            transcript_id (str): Unique identifier of the transcript.

        Returns:
            Dict[str, Any]: Metadata of the transcript.
        """
        return self._request("GET", f"/api/transcript/{transcript_id}")

    def get_transcript_content(self, transcript_id: str, remove_stopwords: bool = False, remove_timestamps: bool = False) -> Dict[str, Any]:
        """
        Fetches transcript content.

        Parameters:
            transcript_id (str): Unique identifier of the transcript.
            remove_stopwords (bool): If True, removes stopwords from the content.
            remove_timestamps (bool): If True, removes timestamps from the content.

        Returns:
            Dict[str, Any]: Transcript content with or without modifications.
        """
        params = {"remove_stopwords": remove_stopwords, "remove_timestamps": remove_timestamps}
        return self._request("GET", f"/api/transcript/{transcript_id}/content", params=params)

    def delete_transcript(self, transcript_id: str) -> Dict[str, Any]:
        """
        Deletes a specific transcript.

        Parameters:
            transcript_id (str): Unique identifier of the transcript.

        Returns:
            Dict[str, Any]: Confirmation of deletion.
        """
        return self._request("DELETE", f"/api/transcript/{transcript_id}")
