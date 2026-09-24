import json
from uuid import uuid4
from datetime import datetime, timezone
from pathlib import Path
LEADS_FILE = Path(__file__).resolve().parent / "leads.json"

def get_required_input(prompt):
    value = input(prompt).strip()

    while not value:
        print("This field cannot be empty.")
        value = input(prompt).strip()
    return value

def load_leads():
    try:
        with open(LEADS_FILE, "r", encoding="utf-8") as file:
            leads = json.load(file)

            if not isinstance(leads, list):
                print("Invalid data: expected a list of leads.")
                raise SystemExit(1)
            for lead in leads:
                if not isinstance(lead, dict):
                    print("Invalid data: each lead must be an object.")
                    raise SystemExit(1)

                for field in ("name", "email", "message"):
                    if field not in lead or not isinstance(lead[field], str):
                        print(f"Invalid data: '{field}' must be text.")
                        raise SystemExit(1)
            return leads
    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("Cannot read leads.json: invalid JSON.")
        print("Fix the file before continuing. No data was changed.")
        raise SystemExit(1)

def save_leads(leads):
    temp_file = LEADS_FILE.with_suffix(".tmp")

    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(leads, file, ensure_ascii=False, indent=4)

    temp_file.replace(LEADS_FILE)

def show_leads(leads):
    if not leads:
        print("No leads yet.")
        return

    for number, lead in enumerate(leads, start=1):
        print(f"{number}. {lead['name']} | {lead['email']}")
        print(f"   Request: {lead['message']}")
        print(f"   ID: {lead.get('id', 'Not assigned')}")
        print(f"   Status: {lead.get('status', 'unknown')}")

def create_lead():
    name = get_required_input("Customer name: ")

    email = input("Customer email: ").strip()
    while "@" not in email or " " in email:
        print("Enter an email with @ and no spaces.")
        email = input("Customer email: ").strip()

    message = get_required_input("What does the customer need? ")

    lead = {
        "id": str(uuid4()),
        "status": "new",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "name": name,
        "email": email,
        "message": message,
    }

    return lead

def search_leads(leads, email):
    matches = []

    for lead in leads:
        if lead["email"].lower() == email.lower():
            matches.append(lead)

    return matches

def update_lead_status(leads, lead_id, new_status):
    for lead in leads:
        if lead.get("id") == lead_id:
            lead["status"] = new_status
            return True

    return False

def main():

    while True:
        print("\nLead Manager")
        print("1. Add lead")
        print("2. Show leads")
        print("3. Search by email")
        print("4. Change lead status")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            lead = create_lead()
            leads = load_leads()
            leads.append(lead)
            save_leads(leads)
            print("Lead saved successfully.")

        elif choice == "2":
            leads = load_leads()
            show_leads(leads)

        elif choice == "3":
            email = get_required_input("Email to search: ")
            leads = load_leads()
            matches = search_leads(leads, email)

            if matches:
                show_leads(matches)
            else:
                print("No matching leads found.")

        elif choice == "4":
            lead_id = get_required_input("Lead ID: ")
            new_status = get_required_input(
                "New status (new/contacted/closed): "
            ).lower()

            if new_status not in ("new", "contacted", "closed"):
                print("Invalid status.")
            else:
                leads = load_leads()

                if update_lead_status(leads, lead_id, new_status):
                    save_leads(leads)
                    print("Status updated successfully.")
                else:
                    print("Lead not found.")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1, 2, 3, 4, or 0.")

if __name__ == "__main__":
    main()

