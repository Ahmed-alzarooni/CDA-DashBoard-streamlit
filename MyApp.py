import streamlit as st
from Auth.Auth import sign_up, login
from Database.Database import create_db

# Create the database and user table (only need to run once)
create_db()

# Streamlit app interface
st.title("Sign-Up or Login")

# Create two buttons: one for Sign Up and one for Login
col1, col2 = st.columns(2)

# Display buttons for Sign Up and Login with unique keys
with col1:
    if st.button("Sign Up", key="sign_up_button"):
        st.session_state.page = "Sign Up"
        
with col2:
    if st.button("Login", key="login_button"):
        st.session_state.page = "Login"

# Handle the Sign Up form
if 'page' not in st.session_state:
    st.session_state.page = None

if st.session_state.page == "Sign Up":
    st.header("Sign-Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if password != confirm_password:
        st.warning("Passwords do not match!")

    if st.button("Sign Up", key="submit_sign_up"):
        if not username or not password:
            st.error("Please fill in all fields")
        else:
            message = sign_up(username, password)
            st.success(message)

elif st.session_state.page == "Login":
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", key="submit_login"):
        if not username or not password:
            st.error("Please fill in both fields")
        else:
            message = login(username, password)
            if "Login successful" in message:
                st.success(message)
                # Show the rest of the app content here after successful login
            else:
                st.error(message)