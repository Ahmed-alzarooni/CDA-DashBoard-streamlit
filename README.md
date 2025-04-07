# CDA-DashBoard-streamlit

## Streamlit Deploy
https://cda-app.streamlit.app/
### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```

App/
├── MyApp.py              ← Main app launcher
├── Auth/
│   └── Auth.py           ← Handles login & sign-up logic
├── Database/
│   └── Database.py       ← SQLite DB functions
