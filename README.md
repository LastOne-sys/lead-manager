# Lead Manager

A Python command-line application for managing customer enquiries.

## Features

- Create leads with a unique ID and UTC timestamp.
- Reject empty names and requests.
- Perform a basic email check.
- Save leads locally in JSON format.
- List leads and search by email.
- Change lead status: new, contacted, or closed.
- Validate stored data before use.
- Write updates to a temporary file before replacing the data file.

## Requirements

Developed and tested with Python 3.14.

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python main.py
```
## Tests

```bash
python -m unittest -v
```

Six tests cover email search, status updates, and the AI summary endpoint.
AI calls are mocked during tests; no OpenAI requests are sent.

## Run the API

```bash
python -m uvicorn api:app --reload
```

Open http://127.0.0.1:8000/docs to try the API.

Endpoints:
- GET /health — check server health.
- GET /leads — list saved leads.
- POST /leads — create a lead.
- POST /leads/summarize — generate an AI summary without saving a lead.

Run either the CLI or the API, not both at the same time.
They share the same local JSON file.

## Local data

The application creates leads.json beside main.py.
Local lead data is excluded from Git through .gitignore.

## Project status

This is a local learning project and portfolio foundation.
AI summaries are available through the OpenAI API.
External CRM integration is not implemented yet.

The email check is basic and does not verify that an address exists.
Run only one instance at a time to avoid conflicting file updates.

## AI setup

Create a local .env file beside main.py:

```dotenv
OPENAI_API_KEY=your_api_key_here
```

Replace the placeholder with your own API key.
Never commit .env or real API keys.

The summary endpoint sends only the request message to OpenAI.
Live AI requests incur API charges.