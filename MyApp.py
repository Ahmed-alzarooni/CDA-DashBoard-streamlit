import streamlit as st
from Auth import sign_up, login
from Database import create_db
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from google import genai
# Create the database and set up session state defaults
create_db()

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'page' not in st.session_state:
    st.session_state.page = None

# ---------- LOGIN / SIGN-UP INTERFACE ----------
if not st.session_state.authenticated:
    st.title("Sign-Up or Login")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sign Up", key="sign_up_button"):
            st.session_state.page = "Sign Up"
    with col2:
        if st.button("Login", key="login_button"):
            st.session_state.page = "Login"

    if st.session_state.page == "Sign Up":
        st.header("Sign-Up")
        username = st.text_input("Username", key="signup_user")
        password = st.text_input("Password", type="password", key="signup_pass")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")

        if password and confirm_password and password != confirm_password:
            st.warning("Passwords do not match!")

        if st.button("Sign Up", key="submit_sign_up"):
            if not username or not password:
                st.error("Please fill in all fields")
            else:
                message = sign_up(username, password)
                st.success(message)

    elif st.session_state.page == "Login":
        st.header("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login", key="submit_login"):
            if not username or not password:
                st.error("Please fill in both fields")
            else:
                message = login(username, password)
                if "Login successful" in message:
                    st.success(message)
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.rerun() # Force a rerun to update the UI automatically
                else:
                    st.error(message)

# ---------- DASHBOARD CONTENT ----------
if st.session_state.authenticated:
    st.sidebar.title(f"Welcome, {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.page = None
        st.rerun()

    st.sidebar.title("Customize Graph")

    # Load and prepare dataset
    file_path = 'Dataset/cleaned_dataset.xlsx'
    data_df = pd.read_excel(file_path)
    cleaned_data_df = data_df.dropna(subset=['Series Name'])
    countries = cleaned_data_df['Country Name'].unique()
    indicators = cleaned_data_df['Series Name'].unique()

    country = st.sidebar.selectbox("Select Country", countries)
    indicator = st.sidebar.selectbox("Select Indicator", indicators)
    start_year = st.sidebar.slider("Start Year", 2014, 2023, 2014)
    end_year = st.sidebar.slider("End Year", 2014, 2023, 2023)
    years = [str(year) for year in range(start_year, end_year + 1)]
    year_columns = [col for col in data_df.columns if col.split()[0].isdigit()]

    # Filter data based on selection
    country_data = cleaned_data_df[cleaned_data_df['Country Name'] == country]
    indicator_data = country_data[country_data['Series Name'] == indicator]
    indicator_values = indicator_data[year_columns].values.flatten()
    indicator_values = pd.to_numeric(indicator_values, errors='coerce')
    valid_data_mask = ~np.isnan(indicator_values)
    valid_years = np.array(years)[:len(indicator_values)][valid_data_mask]
    valid_indicator_values = indicator_values[valid_data_mask]

    # Create and display the Plotly graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=valid_years,
        y=valid_indicator_values,
        mode='lines+markers',
        name=f'{indicator} for {country}',
        marker=dict(size=8),
        line=dict(width=2)
    ))
    fig.update_layout(
        title=f'{indicator} for {country}',
        xaxis_title='Year',
        yaxis_title=indicator,
        template='plotly_dark',
        hovermode='x unified',
        showlegend=False,
        autosize=True,
        margin=dict(t=40, b=40, l=40, r=40),
        xaxis=dict(tickmode='linear', tick0=start_year, dtick=1),
    )
    st.plotly_chart(fig)

    if st.checkbox("Show Raw Data"):
        st.write(indicator_data[['Country Name', 'Series Name'] + year_columns])

    # AI Insights Section
    st.sidebar.title("AI Insights")

    # Initialize the AI client
    client = genai.Client(api_key="AIzaSyB9-Fdp_aO7bkY3Ds5q6iLlhPMNI5HIong")

    user_question = st.text_area("Ask a question about the graph:")
    if user_question:
        # Construct the context for the model based on graph data
        prompt = (
            f"Given the data for {indicator} from {start_year} to {end_year} for {country}, "
            f"please provide insights about the trends, patterns, or any important observations. "
            f"Here is the data:\nYears: {valid_years.tolist()}\nValues: {valid_indicator_values.tolist()}\n\n"
            f"Question: {user_question} "
            f"Return your answer as plain text only. Do not use HTML tags or formatting."
        )

        # Generate content from the AI model
        ai_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        # Extract the generated text using attribute access
        ai_text = ai_response.candidates[0].content.parts[0].text

        # Display the AI response on the app
        st.write("### AI Insights:")
        st.write(ai_text)
        print(ai_text)
