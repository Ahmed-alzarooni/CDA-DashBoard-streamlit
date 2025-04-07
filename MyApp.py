import streamlit as st
from Auth import sign_up, login
from Database import create_db
import pandas as pd
import math
import plotly.graph_objects as go
import numpy as np
from google import genai

# --- CSS ---
st.markdown(
    """
    <style>
    /* Change the background color of the main app container */
    [data-testid="stAppViewContainer"] {
        background-color: #F1EFEC;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* This selector targets the sidebar container */
    [data-testid="stSidebar"] {
         background-color: #D4C9BE;
    }
    </style>
    """,
    unsafe_allow_html=True
)

css_slider = """
<style>
/* 1) Active portion (the red line) */
[data-baseweb="slider"] [role="progressbar"] {
  background-color: #123458 !important;
}

/* 3) Thumb (draggable circle) */
[data-baseweb="slider"] [role="slider"] {
  background-color: #123458 !important;
}

/* 4) Force any text or SVG elements inside the slider to #123458 */
[data-testid="stSlider"] * {
  color: #123458 !important;
  fill: #123458 !important;
}
</style>
"""

st.markdown(css_slider, unsafe_allow_html=True)

st.markdown(
    """
    <style>
    /* For standard text input and password input fields */
    input[type="text"], input[type="password"] {
        background-color: white !important;
        color: black !important;
    }
    /* For larger text areas */
    textarea {
        background-color: white !important;
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .main {background-color: #f8f9fa; }
    .sidebar .sidebar-content {background-image: linear-gradient(#2c3e50, #3498db);}
    .header-banner {
        /* Optional: add a background image for the header banner if desired */
        /* background-image: url('https://your-banner-image-url.com/banner.jpg'); */
        background-size: cover;
        padding: 50px 20px;
        text-align: center;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header Banner with inline Earth image replacing the "O" in "CDA.IO"
st.markdown(
    """
    <div class="header-banner" style="color: black;">
        <h1 style="font-size: 3em; margin: 0; text-align: center; color: black;">
            CDA<img src="https://openclipart.org/image/800px/601" alt="Earth" style="height: 0.85em; vertical-align: middle; margin-top: -0.1em;"> 
        </h1>
        <p style="font-size: 1.5em; margin: 0; text-align: center; color: black;">Insights for Global Development</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* Target the container for the text input */
    div[data-baseweb="input"] {
        position: relative;               /* so we can position the arrow absolutely */
        background-color: #f5f7fa !important;
        border-radius: 9999px !important; /* pill shape */
        border: none !important;
        padding: 0 !important;
        box-shadow: none !important;      /* remove any default shadow */
    }

    /* Remove extra backgrounds from the container's inner divs */
    div[data-baseweb="input"] > div {
        background: none !important;
    }

    /* Style the actual input element */
    div[data-baseweb="input"] input {
        background: none !important;
        border: none !important;
        border-radius: 9999px !important;
        padding-left: 1rem !important;    /* space on the left for text */
        padding-right: 2.5rem !important; /* space on the right for the arrow */
        font-size: 14px !important;
        color: #333 !important;
        height: 1.5rem;                   /* adjust as needed */
    }

    /* Placeholder text color */
    div[data-baseweb="input"] input::placeholder {
        color: #999 !important;
    }

    /* Decorative arrow on the right side */
    div[data-baseweb="input"]::after {
        content: "➤";
        position: absolute;
        right: 1rem;                /* position the arrow */
        top: 50%;
        transform: translateY(-50%);
        color: #999;
        pointer-events: none;       /* arrow is not clickable */
        font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


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
    # Outer layout to center the inner content
    empty_left, center, empty_right = st.columns([1, 3, 1])
    with center:
        # Create three inner columns: left for "Sign Up", center empty, right for "Login"
        col_left, col_mid, col_right = st.columns([1, 1, 1])
        with col_left:
            if st.button("Sign Up", key="sign_up_button"):
                st.session_state.page = "Sign Up"
        with col_right:
            if st.button("Login", key="login_button"):
                st.session_state.page = "Login"

    if st.session_state.page == "Sign Up":
        st.header("Sign-Up")
        # Username Input
        username = st.text_input("Username", key="signup_user")
        # Display username requirement indicator below the username field
        username_valid = len(username) >= 4 if username else False
        st.markdown(f"- At least 4 characters: {'✅' if username_valid else '❌'}")

        
        # Password input field
        password_input = st.text_input("Password", type="password", key="signup_pass")
        
        # Helper function to check password requirements
        def check_password_requirements(password):
            has_min_length = len(password) >= 8
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_number = any(c.isdigit() for c in password)
            special_characters = "!@#$%^&*(),.?\":{}|<>"
            has_special = any(c in special_characters for c in password)
            return has_min_length, has_upper, has_lower, has_number, has_special

        # Get requirement status if a password is entered, otherwise default to False for each
        requirements = check_password_requirements(password_input) if password_input else (False, False, False, False, False)
        
        # Display password requirements as bullet points with dynamic indicators, below the password field
        
        st.markdown(
            f"- At least 8 characters: {'✅' if requirements[0] else '❌'}  \n"
            f"- At least one uppercase letter: {'✅' if requirements[1] else '❌'}  \n"
            f"- At least one lowercase letter: {'✅' if requirements[2] else '❌'}  \n"
            f"- At least one number: {'✅' if requirements[3] else '❌'}  \n"
            f"- At least one special character: {'✅' if requirements[4] else '❌'}"
        )
        
        # Confirm Password field appears after the dynamic display
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
        
        if password_input and confirm_password and password_input != confirm_password:
            st.warning("Passwords do not match!")
        
        if st.button("Sign Up", key="submit_sign_up"):
            # Check username length before proceeding
            if not username or not password_input:
                st.error("Please fill in all fields")
            elif len(username) < 4:
                st.error("Username must be at least 4 characters long.")
            else:
                message = sign_up(username, password_input)
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
                    st.rerun()  # Automatically refresh the app after login
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

    # Load and prepare dataset from the modified file
    file_path = 'Dataset/modified_cleaned_dataset.xlsx'
    data_df = pd.read_excel(file_path)

    # Drop rows without an indicator name
    cleaned_data_df = data_df.dropna(subset=['Indicator Name'])
    countries = cleaned_data_df['Country Name'].unique()
    indicators = cleaned_data_df['Indicator Name'].unique()

    # Allow users to select multiple countries
    selected_countries = st.sidebar.multiselect("Select Country(s)", options=countries, default=[countries[0]])
    indicator = st.sidebar.selectbox("Select Indicator", options=indicators)
    year_range = st.sidebar.slider("Select Year Range", 2014, 2023, (2014, 2023))
    start_year, end_year = year_range
    # --- Process Year Columns ---
    # We'll extract those columns that are digits.
    available_year_columns = [str(col) for col in data_df.columns if str(col).isdigit()]
    # Filter based on slider range
    selected_year_columns = [col for col in available_year_columns if start_year <= int(col) <= end_year]
    selected_year_columns.sort(key=lambda x: int(x))
    # Use these as x-axis labels
    years = selected_year_columns

    

    if not selected_year_columns:
        st.error("No year columns found in the dataset for the selected range!")
        st.stop()

    # Create the Plotly graph
    fig = go.Figure()

    # Define a default color palette and assign each country a color
    default_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", 
                      "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", 
                      "#bcbd22", "#17becf"]
    trace_colors = {}
    for idx, country in enumerate(selected_countries):
        color = default_colors[idx % len(default_colors)]
        trace_colors[country] = color
        country_data = cleaned_data_df[cleaned_data_df['Country Name'] == country]
        indicator_data = country_data[country_data['Indicator Name'] == indicator]
        indicator_values = indicator_data[selected_year_columns].values.flatten()
        indicator_values = pd.to_numeric(indicator_values, errors='coerce')
        valid_data_mask = ~np.isnan(indicator_values)
        valid_years = np.array(years)[valid_data_mask]
        valid_indicator_values = indicator_values[valid_data_mask]
        fig.add_trace(go.Scatter(
            x=valid_years,
            y=valid_indicator_values,
            mode='lines+markers',
            name=country,
            marker=dict(size=8, color=color),
            line=dict(width=2, color=color)
        ))

    # Disable built-in legend
    fig.update_layout(showlegend=False)

    # --- Create a Custom External Legend (without checkboxes) ---
    st.markdown(
    """
    <style>
    .custom-legend {
        display: flex;
        flex-wrap: wrap;         /* allow items to wrap to a new line */
        max-height: 150px;        /* fixed maximum height */
        overflow-y: auto;         /* vertical scrollbar when content exceeds height */
        background: #ffffff;
        border: 2px solid #123458;
        border-radius: 8px;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.2);
        padding: 10px;
        margin-top: 10px;
        gap: 10px;
    }
    .legend-item {
        display: flex;
        align-items: center;
        margin: 5px;
    }
    .legend-color {
        width: 16px;
        height: 16px;
        display: inline-block;
        margin-right: 5px;
        border-radius: 50%;
    }
    .legend-label {
        font-weight: 600;
        font-size: 14px;
        color: #123458;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    # Build the entire legend HTML as a single string
    if selected_countries:
    # Build the entire legend HTML as a single string
        legend_html = "<div class='custom-legend'>"
        for country in selected_countries:
            color = trace_colors[country]  # trace_colors is your dict mapping country to color
            legend_html += (
                f"<div class='legend-item'>"
                f"<span class='legend-color' style='background-color:{color};'></span>"
                f"<span class='legend-label'>{country}</span>"
                f"</div>"
            )
        legend_html += "</div>"
        st.markdown(legend_html, unsafe_allow_html=True)

    # Dynamically adjust the top margin based on the number of selected countries.
    countries_per_row = 4
    num_rows = math.ceil(len(selected_countries) / countries_per_row)
    base_top_margin = 40
    extra_space_per_row = 20
    dynamic_top_margin = 1

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title=indicator,
        template='plotly_white',
        hovermode='x unified',
        autosize=True,
        margin=dict(t=dynamic_top_margin, b=40, l=40, r=40),
        xaxis=dict(tickmode='linear', tick0=start_year, dtick=1)
    )
    st.plotly_chart(fig)

    if st.checkbox("Show Raw Data"):
        # Show raw data for all selected countries for the chosen indicator
        raw_data = cleaned_data_df[
            (cleaned_data_df['Country Name'].isin(selected_countries)) &
            (cleaned_data_df['Indicator Name'] == indicator)
        ]
        st.write(raw_data[['Country Name', 'Indicator Name'] + selected_year_columns])

    # AI Insights Section
    client = genai.Client(api_key="AIzaSyB9-Fdp_aO7bkY3Ds5q6iLlhPMNI5HIong")
    # Ensure each user has their own chat history
    # Ensure chat history is a dictionary keyed by username
    if 'chat_history' not in st.session_state or not isinstance(st.session_state.chat_history, dict):
        st.session_state.chat_history = {}

    user = st.session_state.username  # Unique username for the current user
    if user not in st.session_state.chat_history:
        st.session_state.chat_history[user] = []
        
    st.markdown("<h3>AI Insights</h3>", unsafe_allow_html=True)

    # Inject custom CSS for the chat log container, chat bubbles, and chat input container
    st.markdown(
    """
    <style>
    /* Chat log container styling */
    .chat-log-container {
        background-color: #f9f9f9;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 15px;
        max-height: 400px;
        overflow-y: auto;
        margin-bottom: 10px;
    }
    .chat-log {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .chat-message {
        padding: 8px;
        border-radius: 8px;
        max-width: 80%;
    }
    .chat-message.user {
        background-color: #D4C9BE;  /* Updated user message color */
        align-self: flex-end;
        text-align: right;
    }
    .chat-message.assistant {
        background-color: #e2e3e5;
        align-self: flex-start;
        text-align: left;
    }
    /* Chat input container styling */
    .chat-input-container {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    /* Adjust the text area to fill most of the width */
    .chat-input-container .stTextArea {
        flex-grow: 1;
    }
    /* Style the arrow button as a circular send button */
    .send-arrow-button button {
        background-color: #123458;
        color: white;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        font-size: 1.5rem;
    }
    /* Override default button styling if necessary */
    .send-arrow-button button:hover {
        background-color: #0e344a;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    

    # Display the chat history as chat bubbles
    # Build the entire chat log HTML as a single string
    chat_log_html = "<div class='chat-log-container'><div class='chat-log'>"
    for chat in st.session_state.chat_history[user]:
        # Only process if chat is a dictionary
        if isinstance(chat, dict):
            if chat.get('role') == 'user':
                chat_log_html += f"<div class='chat-message user'>{chat.get('message')}</div>"
            else:
                chat_log_html += f"<div class='chat-message assistant'>{chat.get('message')}</div>"
    chat_log_html += "</div></div>"

    # Now render the chat log in a single call
    st.markdown(chat_log_html, unsafe_allow_html=True)
    # Get a new message from the user using a text area with placeholder text.
    new_message = st.text_area("", placeholder="Ask a question about the graph", key="chat_input")

    if st.button("Send"):
        if new_message:
            st.session_state.chat_history[user].append({"role": "user", "message": new_message})
        
        
            # Construct the system prompt based on the current graph data.
            system_prompt = f"""
                You are an advanced economic data assistant. Your job is to analyze and provide insights on the following economic indicator: {indicator} for {selected_countries} from {start_year} to {end_year}.

                Response Style:
                - Use clear, plain American English and avoid technical jargon.
                - Explain any technical terms in simple language so that anyone can understand.
                - Keep your answer around 150 words, including only essential details.
                - Clearly justify the trends, patterns, and observations from the provided graph data.
                - Base your justifications on well-known economic principles and, when appropriate, reference reliable sources.
                - If the question goes beyond the provided data, politely state that your response is limited to the information given.
                - Return your answer as plain text only (do not include HTML tags or formatting).

                Data Provided:
                Years: {list(valid_years)}
                Values: {list(valid_indicator_values)}

                User Question:
                {new_message}

                Please analyze the data and justify the observed trends using reliable economic principles.
                """

            # Generate the AI response.
            ai_response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=system_prompt
            )
            ai_text = ai_response.candidates[0].content.parts[0].text
        
            # Append the AI response to the chat history.
            st.session_state.chat_history[user].append({"role": "assistant", "message": ai_text})
            st.rerun()
