import unittest
from unittest.mock import patch

from user_authentication import authenticate_user, logout_user
from notification_system import notify_users
from donation_matching import match_donors_recipients
from food_donation_system import FoodDonationSystem


class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.system = unittest.mock.Mock()
        self.system.logged_in_user = None
        self.system.logger = unittest.mock.Mock()

    def test_successful_authentication(self):
        with patch('builtins.input', side_effect=['admin', 'password']):
            self.assertTrue(authenticate_user(self.system, 'admin', 'password'))
            self.assertEqual(self.system.logged_in_user, 'admin')
            self.system.logger.info.assert_called_once_with(f"User 'admin' logged in.")

    def test_failed_authentication(self):
        with patch('builtins.input', side_effect=['invalid_user', 'invalid_password']):
            self.assertFalse(authenticate_user(self.system, 'invalid_user', 'invalid_password'))
            self.assertIsNone(self.system.logged_in_user)
            self.system.logger.warning.assert_called_once_with(f"Failed login attempt for user 'invalid_user'.")

    def test_logout(self):
        self.system.logged_in_user = 'admin'
        logout_user(self.system)
        self.assertIsNone(self.system.logged_in_user)
        self.system.logger.info.assert_called_once_with("User logged out.")

class TestNotifications(unittest.TestCase):
    def setUp(self):
        self.system = unittest.mock.Mock()
        self.system.logger = unittest.mock.Mock()
        self.system.add_notification = unittest.mock.MagicMock()

    def test_successful_notification(self):
        donor = {'name': 'Kylian Mbappe'}
        recipient = {'name': 'Paul Pogba'}
        notify_users(self.system, donor, recipient)

        self.system.add_notification.assert_has_calls([
            unittest.mock.call("Your donation matched with Paul Pogba."),
            unittest.mock.call("You have a matched donation from Kylian Mbappe."),
    ])

class TestDonationMatching(unittest.TestCase):
    def setUp(self):
        self.system = unittest.mock.Mock()
        self.system.donors = []
        self.system.recipients = []
        self.system.matches = []
        self.system.logger = unittest.mock.Mock()
        self.system.add_notification = unittest.mock.MagicMock()

    def test_matching_within_distance(self):
        donor = {'id': 1, 'name': 'Kylian Mbappe', 'location': {'latitude': 37.7749, 'longitude': -122.4194}, 'food_type': 'canned_goods'}
        recipient = {'id': 2, 'name': 'Paul Pogba', 'location': {'latitude': 37.7700, 'longitude': -122.4100}}
        self.system.donors.append(donor)
        self.system.recipients.append(recipient)

        match_donors_recipients(self.system)

        self.assertEqual(self.system.matches, [{'donor_id': 1, 'recipient_id': 2, 'food_type': 'canned_goods'}])
        self.system.add_notification.assert_called_once_with("Donor Kylian Mbappe matched with Recipient Paul Pogba for canned_goods.")

# Will Add more test cases to cover:
# - Matching based on food types
# - Handling recipients already in matches
# - Edge cases (e.g., no donors or recipients, invalid locations)

class TestFoodDonationSystem(unittest.TestCase):
    def setUp(self):
        self.system = FoodDonationSystem()  # Creating an instance of the system

    def test_registration(self):
        self.system.logged_in_user = "admin"

        # Test successful donor registration
        donor_id = self.system.register_donor("Kylian Mbappe", "mbappe@example.com")
        self.assertIsNotNone(donor_id, "Expected a donor ID to be returned")
        self.assertEqual(len(self.system.donors), 1, "Expected one donor to be added")
        self.assertEqual(self.system.donors[0]['name'], "Kylian Mbappe")
        self.assertEqual(donor_id, 1, "Expected the registered donor to have ID 1")

    # Test successful recipient registration
        recipient_id = self.system.register_recipient("Paul Pogba", "pogba@example.com", {"latitude": 37.7749, "longitude": -122.4194})
        self.assertEqual(self.system.recipients[0]['name'], "Paul Pogba")
        self.assertEqual(recipient_id, 1)

    # Test successful Agent registration
        agent_id = self.system.register_agent("Mikel Arteta", "arteta@example.com", {"latitude": 37.7749, "longitude": -122.4194})
        self.assertEqual(self.system.agents[0]['name'], "Mikel Arteta")
        self.assertEqual(agent_id, 1)

    # Test registration with authentication required
        self.system.logged_in_user = None
        self.assertIsNone(self.system.register_donor("jude bellingham", "jude@example.com"))


# Add more test cases to cover:
# - Authentication (login and logout)
# - Donation process
# - Match generation
# - Viewing history and notifications
# - Input validation and error handling

if __name__ == '__main__':
    unittest.main()
