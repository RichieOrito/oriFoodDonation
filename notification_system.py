import logging

def notify_users(system, donor, recipient):
    # Notify donors and recipients about the match
    donor_notification = f"Your donation matched with {recipient['name']}."
    recipient_notification = f"You have a matched donation from {donor['name']}."

    system.add_notification(donor_notification)
    system.add_notification(recipient_notification)
