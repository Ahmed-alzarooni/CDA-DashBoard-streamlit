# CDA-DashBoard-streamlit

## AWS Deploy
https://www.cda-insight.com/
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
       └── Database.py       ← SQLite DB functions
   ```
   
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
   Or you can use this directory structure while keeping the same exact code in `MyApp.py`:
   ```
   App/
   ├── MyApp.py              ← Main app launcher
   ├── Auth.py               ← Handles login & sign-up logic           
   ├── Database.py           ← SQLite DB functions       
   ```
Note: Please be sure to run the App in light mode. You can switch between light mode and dark mode from the 3 dots in the top right corner after you run the app. If your system is on dark mode, then the app will automatically run on dark mode.
