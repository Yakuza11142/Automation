import schedule
from telephony.sim_handler import SIMHandler
from telephony.contacts_manager import ContactsManager

class CallScheduler:
    def __init__(self):
        self.sim = SIMHandler()
        self.contacts = ContactsManager()

    def schedule_optimal_call(self, contact_query: str, target_time: str = "10:30"):
        def job():
            number = self.contacts.search_contact(contact_query)
            if number:
                print(f"[Scheduler] Running scheduled call for: '{contact_query}'")
                self.sim.dial_number(number)
            else:
                print(f"[Scheduler Error] Could not find number for target '{contact_query}'")

        schedule.every().day.at(target_time).do(job)
        print(f"[Scheduler] Programmed call for '{contact_query}' daily at {target_time}")

    def run_pending(self):
        schedule.run_pending()
