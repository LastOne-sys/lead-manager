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

Python 3.10 or newer. No external packages required.

## Run

```bash
python main.py
```

## Tests

```bash
python -m unittest -v
```

Four tests cover email search and status updates.

## Local data

The application creates leads.json beside main.py.
Local lead data is excluded from Git through .gitignore.

## Project status

This is a local learning project and portfolio foundation.
AI integration and external CRM integration are not implemented yet.

The email check is basic and does not verify that an address exists.
Run only one instance at a time to avoid conflicting file updates.