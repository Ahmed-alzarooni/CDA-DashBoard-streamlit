import bcrypt
import re
from Database import check_user_exists, insert_user, get_user

def is_valid_password(password):
    """
    Validates that the password meets the following criteria:
    - At least 8 characters
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one number
    - Contains at least one special character
    """
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
    return re.match(pattern, password) is not None

# Function to sign up a new user
def sign_up(username, password):
    # Check if username already exists
    if check_user_exists(username):
        return "Username already exists! Please choose a different username."
    
    # Validate password security
    if not is_valid_password(password):
        return ("Password must be at least 8 characters long and include at least one uppercase letter, "
                "one lowercase letter, one number, and one special character.")

    # Check for empty password (this check is optional now as the regex covers length, but kept for clarity)
    if not password:
        return "Password cannot be empty."
    
    try:
        # Debug: Print the user details
        print(f"Signing up user: {username}")
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Debug: Print the hashed password (for development only; remove in production)
        print(f"Hashed Password: {hashed_password}")
        
        # Insert the new user into the database
        insert_user(username, hashed_password)
        return "Sign-up successful! You can now log in."
    except Exception as e:
        print(f"Error during password hashing: {e}")
        return "There was an error during the sign-up process."

# Function to log in the user
def login(username, password):
    user = get_user(username)
    
    if user:
        # Debug: Print the user retrieved from the database
        print(f"User retrieved: {user}")
        
        stored_password = user[1]  # Assuming password is the second column in the table
        
        # Debug: Print stored password value
        print(f"Stored Password (from DB): {stored_password}")
        
        # Check the password with bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return "Login successful!"
        else:
            return "Invalid password!"
    else:
        return "Username not found!"
