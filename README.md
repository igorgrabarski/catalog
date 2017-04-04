## Catalog App

#### Application provides the necessary functionality to maintain the database of items, divided by categories. It includes the user's authentication with Google Oauth Platform.

#### Prerequisites:
* python 2.x installed on the machine. To check, write in console: ``` python --version ```
* Any database server . For example purposes, PostgreSQL is used. If you plan to use any other database, please change the appropriate lines in file **db_setup.py**.

#### Installation and run instructions:
* Open console and follow to the main folder(containing **db_setup.py**)
* Open file **db_setup.py** and choose if you want to use the default category names or create your own.
* Write in console ``` python db_setup.py ``` . When all is done, you will see the confirmation message.
* Create your own **CLIENT_ID** on ```https://console.developers.google.com/ ```
* Open file **application.py** and fill in CLIENT_ID in appropriate field on the top of the file.
* Also it's highly recommended to change the **secret_key** in **application.py** to your own long random string. It is used by Flask in session hashing.

* Run main application: ```python application.py ```
* Open the webbrowser and in address line write: ```http://localhost:8000/```

* To stop application, in console press control+C for Mac or ctrl+C for Linux/Windows

#### Application Features:
* Unauthenticated user may:
  * Browse through the categories and items 
  * Download the JSON file with database data by the link in the bottom of the page or by address ```http://localhost:8000/catalog.json/ ```
  
* Authenticated user may, in addition to above options:
  * Add new item to desired category
  * Edit item that he has created
  * Delete item that he has created
  
##### To Sign in, please press the **Sign in** button in top right corner of the page, and use your Google account.


#### Project structure:
* static
  * styles.css - CSS file for an application
* templates
  * index.html - Main web page for an application
* db_setup.py - Initial database setup file
* entities.py - Mapping file for database tables against SQLAlchemy classes
* application.py - Main application file, contains the logic of application. Runs the local webserver.
