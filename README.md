# Recorder: Record your Assignments and Assesments.
Easily arrange and view your assignment and assesment details with this Recorder so that you never miss them.

### Requirements
* Flask Web Framework
* MySQL Database (or change to any SQL database you like. Some databases may not support some features.)

### Installation
* Clone the repo or download the zip file and extract it.

  `git clone git@github.com:divyamani1/Recorder.git`
  
  `cd Recorder`
  
* Create a virtual environment using venv or Virtualenv and activate the virtual environment.

  `python -m venv venv`
  
  `source venv/bin/activate`
  
* Add Recorder to `FLASK_APP` variable.

  `export FLASK_APP=std_record.py`
  
* Update the database username and password (and if you didn't use mysql, the database url) in `routes.py`.
  
  Change `user@password` to your username and password.

* Run the Application. Make sure that your database server is running.

  `flask run`
