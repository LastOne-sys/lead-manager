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

Nine tests cover email search, status updates, AI summaries, and saving summaries for existing leads.
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
- POST /leads/{lead_id}/summary — generate and save a summary for an existing lead; return the saved summary if available.

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


## n8n workflow

The workflow creates a sample lead through the Python API, then generates
and saves an AI summary for that lead.

Workflow file: [create_and_summarize_lead.json](workflows/create_and_summarize_lead.json)

### Requirements

- The Python project dependencies are installed.
- A valid `OPENAI_API_KEY` is configured in the project's `.env` file.
- n8n is running locally on the same computer as the Python API.

This workflow was tested with n8n 2.40.7 and Node.js 24.

### Run the workflow

1. Start the Python API from the project directory:

   ```bash
   python -m uvicorn api:app --reload
   ```

2. Open your local n8n instance.
3. Import `workflows/create_and_summarize_lead.json`.
4. Open the `Create Lead` node to review or edit the sample customer data.
5. Click `Execute workflow`.
6. Open the `Summarize Lead` output and check the `summary` field.

Keep both n8n and the Python API running during execution.

Each full workflow run creates a new lead and requests an AI summary.
OpenAI API usage may incur charges. The lead and its summary are saved
in the local `leads.json` file.

The OpenAI key stays in the Python project's environment and is not
included in the workflow export.

The workflow uses `http://127.0.0.1:8000`. This setup assumes n8n runs
directly on the same computer; n8n Cloud or Docker requires different
network configuration.