import streamlit as st
from Auth.Auth import sign_up, login
from Database.Database import create_db
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
            CDA.I<img src="https://openclipart.org/image/800px/601" alt="Earth" style="height: 0.85em; vertical-align: middle; margin-top: -0.1em;"> 
        </h1>
        <p style="font-size: 1.5em; margin: 0; text-align: center; color: black;">Insights for Global Development</p>
    </div>
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

    # Load and prepare dataset
    file_path = 'Dataset/cleaned_dataset.xlsx'
    data_df = pd.read_excel(file_path)
    cleaned_data_df = data_df.dropna(subset=['Series Name'])
    countries = cleaned_data_df['Country Name'].unique()
    indicators = cleaned_data_df['Series Name'].unique()

    # Allow users to select multiple countries
    selected_countries = st.sidebar.multiselect("Select Country(s)", options=countries, default=[countries[0]])
    indicator = st.sidebar.selectbox("Select Indicator", options=indicators)
    start_year = st.sidebar.slider("Start Year", 2014, 2023, 2014)
    end_year = st.sidebar.slider("End Year", 2014, 2023, 2023)
    years = [str(year) for year in range(start_year, end_year + 1)]
    # Assume the dataset has year columns like "2014", "2015", etc.
    year_columns = [col for col in data_df.columns if col.split()[0].isdigit()]

    # Create the Plotly graph
    fig = go.Figure()

    for country in selected_countries:
        # Filter data for the current country and indicator
        country_data = cleaned_data_df[cleaned_data_df['Country Name'] == country]
        indicator_data = country_data[country_data['Series Name'] == indicator]
        indicator_values = indicator_data[year_columns].values.flatten()
        indicator_values = pd.to_numeric(indicator_values, errors='coerce')
        valid_data_mask = ~np.isnan(indicator_values)
        valid_years = np.array(years)[:len(indicator_values)][valid_data_mask]
        valid_indicator_values = indicator_values[valid_data_mask]

        # Add a trace for each selected country (legend label is only the country name)
        fig.add_trace(go.Scatter(
            x=valid_years,
            y=valid_indicator_values,
            mode='lines+markers',
            name=country,  # only the country name appears in the legend
            marker=dict(size=8),
            line=dict(width=2)
        ))

    # Dynamically adjust the top margin based on the number of selected countries.
    # Assume that up to 4 legend items fit per row.
    countries_per_row = 4
    num_rows = math.ceil(len(selected_countries) / countries_per_row)
    base_top_margin = 40
    extra_space_per_row = 20
    dynamic_top_margin = base_top_margin + (num_rows * extra_space_per_row)

    # Update the layout of the graph
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title=indicator,
        template='plotly_white',
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,          # place legend slightly above the plot
            xanchor="center",
            x=0.5
        ),
        autosize=True,
        margin=dict(t=dynamic_top_margin, b=40, l=40, r=40),
        xaxis=dict(tickmode='linear', tick0=start_year, dtick=1)
    )

    st.plotly_chart(fig)

    if st.checkbox("Show Raw Data"):
        first_country = selected_countries[0] if selected_countries else None
        if first_country:
            country_data = cleaned_data_df[cleaned_data_df['Country Name'] == first_country]
            indicator_data = country_data[country_data['Series Name'] == indicator]
            st.write(indicator_data[['Country Name', 'Series Name'] + year_columns])

    # AI Insights Section

    # Initialize the AI client
    client = genai.Client(api_key="AIzaSyB9-Fdp_aO7bkY3Ds5q6iLlhPMNI5HIong")

    user_question = st.text_area("Ask a question about the graph:")
    if user_question:
        # Construct the context for the model based on graph data
        system_prompt = f"""
You are an advanced economic data assistant. Your job is to analyze and provide insights on the following economic indicator: {indicator} for {country} from {start_year} to {end_year}.

Response Style:
- Use clear, plain American English and avoid technical jargon.
- Explain any technical terms in simple language so that anyone can understand.
- Keep your answer around 150 words, including only essential details.
- Clearly justify the trends, patterns, and observations from the provided graph data.
- Base your justifications on well-known economic principles and, when appropriate, reference reliable sources or widely recognized data (e.g., government statistics, academic research, or reputable financial institutions). Do not attribute trends to random or unsupported causes.
- If the question goes beyond the provided data, politely state that your response is limited to the information given.
- Return your answer as plain text only (do not include HTML tags or formatting).

Data Provided:
Years: {valid_years.tolist()}
Values: {valid_indicator_values.tolist()}

User Question:
{user_question}

Please analyze the data and justify the observed trends and patterns using reliable economic sources and principles.
IF THE USER ASKS QUESTIONS THAT HAS NO RELEVANCE TO THE GRAPH OR THE WORLD BANK GROUP OR OTHER ECONIMICAL METRICS THEN ABSTAIN FROM ANSWERING THE QUESTION AND SUGGEST A DIFFERENT QUESTION.
if the users asks about a different economical indicator ask the user to use the sidebar and select the indicator for better analysis.
You are allowed to relate other economical factors or indicator to the graph.
Answer questions about general economic metric and their relations when asked but do not provide that is not from the graph, only general concept explaination.
"""

        # Generate content from the AI model
        ai_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=system_prompt
        )

        # Extract the generated text using attribute access
        ai_text = ai_response.candidates[0].content.parts[0].text

        # Display the AI response on the app
        st.write("### AI Insights:")
        st.write(ai_text)
