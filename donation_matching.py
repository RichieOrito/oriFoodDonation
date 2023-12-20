from geopy.distance import geodesic

def match_donors_recipients(system):
    for donor in system.donors:
        for recipient in system.recipients:
            if recipient not in [match for match in system.matches if 'recipient_id' in match]:
                distance = geodesic((donor['location']['latitude'], donor['location']['longitude']),
                                    (recipient['location']['latitude'], recipient['location']['longitude'])).miles

                if distance < 10:  # Matching if the recipient is within 10 miles of the donor
                    matching_food_types = set([match.get('food_type', '').lower() for match in system.matches
                                               if 'recipient_id' in match and match['recipient_id'] == recipient['id']])
                    donor_food_type = donor.get('food_type', '').lower()

                    if donor_food_type not in matching_food_types:
                        system.matches.append({'donor_id': donor['id'], 'recipient_id': recipient['id'], 'food_type': donor_food_type})
                        system.logger.info(f"Matched Donor {donor['name']} with Recipient {recipient['name']} for {donor_food_type}")

                        notification_message = f"Donor {donor['name']} matched with Recipient {recipient['name']} for {donor_food_type}."
                        system.add_notification(notification_message)
