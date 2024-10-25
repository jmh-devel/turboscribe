# TurboScribe API Client

A Python client for interacting with the TurboScribe transcription API.

## Features
- Upload files and URLs for transcription
- Retrieve metadata and transcription content
- Delete transcriptions

## Installation

1. Clone the repository:

   ```
   git clone git@github.com:tacitness/turboscribe.git
   cd turboscribe
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```
from turboscribe.api_client import TurboScribeClient

# Initialize the client
client = TurboScribeClient(api_key='YOUR_API_KEY')

# Upload a file for transcription
response = client.upload_file('path/to/file.mp3', recognize_speakers=True)
print("Transcript ID:", response.get('transcript_id'))
```

### Configuration
Set environment variables in a `.env` file:

```
API_KEY=your_api_key_here
```

## Testing
To run tests, navigate to the project root and run:

```
pytest
```

## License
[MIT License](LICENSE)