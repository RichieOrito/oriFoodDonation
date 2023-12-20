import logging

def authenticate_user(system, username, password):
    if username == "admin" and password == "password":
        system.logged_in_user = username
        system.logger.info(f"User '{username}' logged in.")
        return True
    else:
        system.logger.warning(f"Failed login attempt for user '{username}'.")
        return False

def logout_user(system):
    system.logged_in_user = None
    system.logger.info("User logged out.")
