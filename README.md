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
   $ streamlit run MyApp.py
   ```
3. Project Directory Structure

```
App/
├── MyApp.py              ← Main app launcher
├── Auth/
│   └── Auth.py           ← Handles login & sign-up logic
├── Database/
│   └── Database.py       ← SQLite DB functions
```

Note: Please be sure to run the App in light mode. You can switch between light mode and dark mode from the 3 dots in the top right corner.
