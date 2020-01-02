# Intelligent Timetabling System
1.  Connect to HKU CS VPN

2.  Create a virtual environment
-   `python -m venv {name_of_virtual_environment}`

3.  Run the virtual environment 
-   For Windows: `{name_of_virtual_environment}\Scripts\activate`
    
4.  Install dependencies in virtual environment
-   `pip -r install requirements.txt`

5.  Copy `settings.py` which contains the credentials of connecting to i2.cs.hku.hk/phpmyadmin into folder `timetable-system`

6.  Set Flask environment and app
-   For Windows: 
    -   `set FLASK_ENV = development`
    -   `set FLASK_APP = timetable-system`

7.  Run the flask application
-   `flask run`

8.  Open the url
