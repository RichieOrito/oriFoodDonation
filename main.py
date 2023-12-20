from food_donation_system import FoodDonationSystem
from user_authentication import authenticate_user, logout_user
from donation_matching import match_donors_recipients
from notification_system import notify_users

def main():
    system = FoodDonationSystem()

    while not system.is_user_authenticated():
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        authenticate_user(system, username, password)
        # Display notifications on login
        system.view_notifications()

    while True:
        print("------------------------------------")
        print("\n#### Ori Food Donation System ####")
        print("------------------------------------")
        print("------------------------------------")
        print("\n1. Register as a Donor")
        print("************************************")
        print("2. Register as an Agent")
        print("************************************")
        print("3. Register as a Recipient")
        print("************************************")
        print("4. Donate Food")
        print("************************************")
        print("5. View Personal History")
        print("************************************")
        print("6. Display Donation Matches")
        print("************************************")
        print("7. Logout")
        print("************************************")
        print("8. Exit")

        choice = int(input("Enter your choice (1-8): "))

        if choice == 1:
            name = input("Enter your name: ")
            contact_info = input("Enter your email address: ")
            latitude = float(input("Enter your latitude: "))
            longitude = float(input("Enter your longitude: "))

            donor_id = system.register_donor(name, contact_info)
            system.donors[-1]['location'] = {'latitude': latitude, 'longitude': longitude}

            print(f"Thank you for registering as a donor, {name}!")

        elif choice == 2:
            name = input("Enter your name: ")
            contact_info = input("Enter your email address: ")

            agent_id = system.register_agent(name, contact_info)
            print(f"Thank you for registering as an agent, {name}!")

        elif choice == 3:
            name = input("Enter your name: ")
            contact_info = input("Enter your email address: ")
            latitude = float(input("Enter your latitude: "))
            longitude = float(input("Enter your longitude: "))
            comments = input("Enter comments for this recipient (optional): ")

            recipient_id = system.register_recipient(name, contact_info, {'latitude': latitude, 'longitude': longitude}, comments)
            print(f"Thank you for registering as a recipient, {name}!")

        elif choice == 4:
            if system.is_user_authenticated():
                donor_id = int(input("Enter your donor ID: "))
                food_type = input("Enter the type of food you want to donate: ")
                food_amount = input("Enter the amount of food you want to donate: ")
                food_unit = input("Enter the unit of the amount (e.g., g or kg): ")
                pickup_date = input("Enter the date of the donation (YYYY-MM-DD): ")

                # Provide the correct recipient_id
                recipient_id = int(input("Enter the recipient ID: "))

                system.donate_food(donor_id, food_type, food_amount, food_unit, pickup_date, recipient_id)
                print("Thank you for donating!")

            else:
                print("Authentication required to donate food.")

        elif choice == 5:
            user_type = input("Enter your user type (donor, agent, or recipient): ").lower()
            user_id = int(input("Enter your user ID: "))
            system.view_personal_history(user_type, user_id)
            # Display notifications after viewing personal history
            system.view_notifications()

        elif choice == 6:
            match_donors_recipients(system)
            system.display_matches()
            # Display notifications after displaying matches
            system.view_notifications()
            system.clear_notifications()

        elif choice == 7:
            logout_user(system)
            print("User logged out.")

        elif choice == 8:
            print("Exiting the Food Donation System.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
