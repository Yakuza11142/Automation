import re

class ContactsManager:
    def __init__(self):
        pass

    def search_contact(self, name_query: str) -> str:
        if not name_query:
            return None

        clean_query = name_query.strip().lower()

        try:
            from googleapiclient.discovery import build
            from google.auth import default

            creds, _ = default()
            service = build('people', 'v1', credentials=creds)

            results = service.people().searchContacts(
                query=clean_query,
                readMask='names,phoneNumbers'
            ).execute()

            results_list = results.get('results', [])
            if results_list:
                person = results_list[0].get('person', {})
                phones = person.get('phoneNumbers', [])
                if phones:
                    return phones[0].get('value')
        except Exception as e:
            print(f"[ContactsManager] Dynamic contact API search notice: {e}")

        digits = re.sub(r"\D", "", clean_query)
        if len(digits) >= 10:
            return digits

        return None
