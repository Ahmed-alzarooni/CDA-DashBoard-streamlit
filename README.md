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
   When using this directory structure, please change the head section of the `MyApp.py` where we import libraries from
   ```
   from Auth import sign_up, login
   from Database import create_db
   ```
   to
   ```
   from Auth.Auth import sign_up, login
   from Database.Database import create_db
   ```

```
App/
├── MyApp.py              ← Main app launcher
├── Auth/
│   └── Auth.py           ← Handles login & sign-up logic
├── Database/
│   └── Database.py       ← SQLite DB functions
```

Note: Please be sure to run the App in light mode. You can switch between light mode and dark mode from the 3 dots in the top right corner after you run the app. If your system is on dark mode, then the app will automatically run on dark mode.
