import logging
from geopy.distance import geodesic
from prettytable import PrettyTable
from datetime import datetime

class FoodDonationSystem:
    def __init__(self):
        self.donors = []
        self.recipients = []
        self.matches = []
        self.agents = []
        self.logged_in_user = None
        self.notifications = []
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger('food_donation_system')
        logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        logger.addHandler(ch)
        return logger

    def login(self, username, password):
        # Basic authentication (username and password check)
        if username == "admin" and password == "password":
            self.logged_in_user = username
            self.logger.info(f"User '{username}' logged in.")
            return True
        else:
            self.logger.warning(f"Failed login attempt for user '{username}'.")
            return False
        # Display notifications on login
        self.view_notifications()

    def logout(self):
        self.logged_in_user = None
        self.logger.info("User logged out.")

    def is_user_authenticated(self):
        return self.logged_in_user is not None

    def register_donor(self, name, contact_info, comments=None):
        if self.is_user_authenticated():
            registration_time = datetime.now()
            donor = {'id': len(self.donors) + 1, 'name': name, 'contact_info': contact_info, 'comments': comments or [], 'registration_time': registration_time}
            self.donors.append(donor)
            self.logger.info(f"Donor registered: {donor}")
            return donor['id']
        else:
            self.logger.warning("Authentication required to register as a donor.")
            return None

    def register_agent(self, name, contact_info, comments=None):
        if self.is_user_authenticated():
            registration_time = datetime.now()
            agent = {'id': len(self.agents) + 1, 'name': name, 'contact_info': contact_info, 'comments': comments or [], 'registration_time': registration_time}
            self.agents.append(agent)
            self.logger.info(f"Agent registered: {agent}")
            return agent['id']
        else:
            self.logger.warning("Authentication required to register as an agent.")
            return None

    def register_recipient(self, name, contact_info, location, comments=None):
        if self.is_user_authenticated():
            registration_time = datetime.now()
            recipient = {'id': len(self.recipients) + 1, 'name': name, 'contact_info': contact_info, 'location': location, 'comments': comments, 'registration_time': registration_time}
            self.recipients.append(recipient)
            self.logger.info(f"Recipient registered: {recipient}")
            return recipient['id']
        else:
            self.logger.warning("Authentication required to register as a recipient.")
            return None

    def donate_food(self, donor_id, food_type, food_amount, food_unit, pickup_date, recipient_id):
        if self.is_user_authenticated():
            comments = get_input("Enter comments for this donation (optional): ")
            try:
                # Convert food_amount to float
                food_amount = float(food_amount)
            except ValueError:
                print("Invalid input for food amount. Please enter a valid numeric value.")
                return
            donation = {'donor_id': donor_id, 'recipient_id': recipient_id, 'food_type': food_type, 'food_amount': food_amount, 'food_unit': food_unit, 'pickup_date': pickup_date, 'comments': comments or []}
            self.matches.append(donation)
            self.logger.info(f"Donation recorded: {donation}")
        else:
            self.logger.warning("Authentication required to donate food.")

    def match_donors_recipients(self):
        for donor in self.donors:
            for recipient in self.recipients:
                if recipient not in [match for match in self.matches if 'recipient_id' in match]:
                    distance = geodesic((donor['location']['latitude'], donor['location']['longitude']),
                                        (recipient['location']['latitude'], recipient['location']['longitude'])).miles

                    if distance < 10:  # Matching if the recipient is within 10 miles of the donor
                        matching_food_types = set([match.get('food_type', '').lower() for match in self.matches
                                                   if 'recipient_id' in match and match['recipient_id'] == recipient['id']])
                        donor_food_type = donor.get('food_type', '').lower()

                        if donor_food_type not in matching_food_types:
                            self.matches.append({'donor_id': donor['id'], 'recipient_id': recipient['id'], 'food_type': donor_food_type})
                            self.logger.info(f"Matched Donor {donor['name']} with Recipient {recipient['name']} for {donor_food_type}")

                            notification_message = f"Donor {donor['name']} matched with Recipient {recipient['name']} for {donor_food_type}."
                            self.add_notification(notification_message)

    def view_personal_history(self, user_type, user_id):
        if user_type == 'donor':
            user_history = [match for match in self.matches if match.get('donor_id') == user_id]
        elif user_type == 'agent':
            user_history = [match for match in self.matches if 'agent_id' in match and match['agent_id'] == user_id]
        elif user_type == 'recipient':
            user_history = [match for match in self.matches if 'recipient_id' in match and match['recipient_id'] == user_id]
        else:
            self.logger.warning("Invalid user type.")
            return

        if not user_history:
            print("No history found.")
        else:
            print(f"\n### {user_type.capitalize()} History ###")
            for match in user_history:
                donor_id = match.get('donor_id')
                donor = next((d for d in self.donors if d['id'] == donor_id), None)
                recipient = next((r for r in self.recipients if r['id'] == match.get('recipient_id')), None)
                agent = next((a for a in self.agents if a['id'] == match.get('agent_id')), None)

                print("Donation Details:")
                if donor:
                    print(f"Donor: {donor['name']} - {donor['contact_info']} (Registered on: {donor['registration_time']})")
                else:
                    print("Donor information not available.")
                if recipient:
                    print(f"Recipient: {recipient['name']} - {recipient['contact_info']} (Registered on: {donor['registration_time']})")
                    print(f"Recipient Comments: {recipient.get('comments', 'No comments')}")
                if agent:
                    print(f"Agent: {agent['name']} - {agent['contact_info']} (Registered on: {donor['registration_time']})")
                print(f"Food Type: {match.get('food_type')}")
                print(f"Pickup Date: {match.get('pickup_date')}")
                print(f"Comments: {match.get('comments', [])}")
                print("------------------------------")

    def display_matches(self):
        table = PrettyTable()
        table.field_names = ["Donor", "Recipient", "Food Type", "Pickup Date"]

        for match in self.matches:
            donor = next((d for d in self.donors if d['id'] == match.get('donor_id')), None)
            recipient = next((r for r in self.recipients if r['id'] == match.get('recipient_id')), None)
            if donor and recipient:
                table.add_row([donor['name'], recipient['name'], match.get('food_type', ''), match.get('pickup_date', 'Not specified')])

        print(table)

    def add_notification(self, message):
        self.notifications.append(message)
        self.logger.info(f"Notification: {message}")

    def view_notifications(self):
        if not self.notifications:
            print("No new notifications.")
        else:
            print("\n### Notifications ###")
            for notification in self.notifications:
                print(notification)
            print("------------------------------")
    
    def clear_notifications(self):
        self.notifications = []
        self.logger.info("Notifications cleared.")

def get_input(prompt, input_type=str):
    while True:
        try:
            user_input = input(prompt)
            return input_type(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid value.")
