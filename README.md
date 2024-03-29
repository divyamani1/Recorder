# Recorder: Record your Assignments and Assesments  

Easily arrange and view your assignment and assesment details with Recorder so that you never miss them.

## Requirements  

* Flask Web Framework

* MySQL Database (or change to any SQL database you like. Some databases may not support some features.)

## Installation

* Clone the repo or download the zip file and extract it.

  `git clone git@github.com:divyamani1/Recorder.git`
  
  `cd Recorder`
  
* Create a virtual environment using venv or Virtualenv and activate the virtual environment.

  `python -m venv venv`
  
  `source venv/bin/activate`
  
  `pip install -r requirements.txt`
  
* Add Recorder to `FLASK_APP` variable.

  `export FLASK_APP=std_record.py`
  
* Update the database username and password (and if you didn't use mysql, the database url) in `config.py`.
  
  Change `user:password` to your username and password.

* Run the Application. Make sure that your database server is running.

  `flask run`

* Initialize the database from `127.0.0.1:5000/init_db`.

* Now, you're good to go.
