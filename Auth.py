import bcrypt
from Database.Database import check_user_exists, insert_user, get_user

# Function to sign up a new user
def sign_up(username, password):
    # Check if username already exists
    if check_user_exists(username):
        return "Username already exists! Please choose a different username."
    
    # Hash the password using bcrypt
    if not password:
        return "Password cannot be empty."
    
    try:
        # Debugging: Check if password is empty
        print(f"Signing up user: {username}, with password: {password}")

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Debugging: Print the hashed password to check its value
        print(f"Hashed Password (from bcrypt): {hashed_password}")
        
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
        # Debugging: Print out the user retrieved from the database
        print(f"User retrieved: {user}")
        
        stored_password = user[1]  # Assuming password is the second column in the table
        
        # Debugging: Check stored password value
        print(f"Stored Password (from DB): {stored_password}")
        
        # Check the password with bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return "Login successful!"
        else:
            return "Invalid password!"
    else:
        return "Username not found!"