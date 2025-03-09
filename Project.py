import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Load the cleaned dataset
file_path = '/Users/3bdulla/Desktop/University/DS 440W/App/Dataset/cleaned_dataset.xlsx'  # Update this with the correct path to the cleaned dataset
data_df = pd.read_excel(file_path)

# Clean up the column names (removing spaces and brackets)
data_df.columns = data_df.columns.str.replace(r"\[|\]", "", regex=True)
data_df.columns = data_df.columns.str.strip()

# Clean the data (remove rows with NaN in 'Series Name')
cleaned_data_df = data_df.dropna(subset=['Series Name'])

# Get the list of countries and indicators
countries = cleaned_data_df['Country Name'].unique()
indicators = cleaned_data_df['Series Name'].unique()

# Streamlit Sidebar
st.sidebar.title("Customize Graph")
country = st.sidebar.selectbox("Select Country", countries)
indicator = st.sidebar.selectbox("Select Indicator", indicators)

# Set the year range
start_year = st.sidebar.slider("Start Year", 2014, 2023, 2014)
end_year = st.sidebar.slider("End Year", 2014, 2023, 2023)

# Prepare the list of years
years = [str(year) for year in range(start_year, end_year + 1)]

# Sanitize the year columns to make sure they match
year_columns = [col for col in data_df.columns if col.split()[0].isdigit()]

# Filter the dataset for the selected country and indicator
country_data = cleaned_data_df[cleaned_data_df['Country Name'] == country]
indicator_data = country_data[country_data['Series Name'] == indicator]

# Extract the years and corresponding values
indicator_values = indicator_data[year_columns].values.flatten()

# Convert the values to numeric, forcing errors to NaN (handles any non-numeric entries)
indicator_values = pd.to_numeric(indicator_values, errors='coerce')

# Filter out NaN values for indicator_values and corresponding years
valid_data_mask = ~np.isnan(indicator_values)

# Filter both the years and indicator_values arrays to make sure they match
valid_years = np.array(years)[:len(indicator_values)][valid_data_mask]
valid_indicator_values = indicator_values[valid_data_mask]

# Create an interactive Plotly graph
fig = go.Figure()

# Add the indicator data to the plot
fig.add_trace(go.Scatter(
    x=valid_years,
    y=valid_indicator_values,
    mode='lines+markers',
    name=f'{indicator} for {country}',
    marker=dict(color='orange', size=8),
    line=dict(color='orange', width=2)
))

# Update layout with better styling
fig.update_layout(
    title=f'{indicator} for {country}',
    xaxis_title='Year',
    yaxis_title=indicator,
    template='plotly_dark',  # Use a dark theme for the plot
    hovermode='x unified',  # Show all data points on hover
    showlegend=False,  # Hide the legend for simplicity
    autosize=True,
    margin=dict(t=40, b=40, l=40, r=40),  # Adjust margins for better readability
    xaxis=dict(tickmode='linear', tick0=start_year, dtick=1),  # Show years as ticks
)

# Display the plot in Streamlit
st.plotly_chart(fig)

# Optional: Display the raw data
if st.checkbox("Show Raw Data"):
    st.write(indicator_data[['Country Name', 'Series Name'] + year_columns])

# Add an AI-powered textbox for insights
st.sidebar.title("AI Insights")

# Create an input box for users to ask questions related to the graph
user_question = st.text_area("Ask a question about the graph:")

# Generate insights from the AI if the user asks something
if user_question:
    # Construct the context for the model based on graph data
    prompt = f"Given the data for {indicator} from {start_year} to {end_year} for {country}, " \
             f"please provide insights about the trends, patterns, or any important observations. " \
             f"Here is the data:\nYears: {valid_years.tolist()}\nValues: {valid_indicator_values.tolist()}\n\n" \
             f"Question: {user_question}"

    # Placeholder response (AI model integration can be done here later)
    ai_response = "AI model integration is coming soon! Once integrated, you will be able to ask the AI for insights on the graph data."

    # Display the response (temporary until actual AI integration)
    st.write("### AI Insights:")
    st.write(ai_response)
