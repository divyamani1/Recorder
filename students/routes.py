from datetime import datetime
from flask import render_template, flash, redirect, url_for, session, request
from students import app, config
from werkzeug.security import generate_password_hash, check_password_hash
from students.forms import LoginForm, SignupForm, AssignmentsForm, AssesmentsForm

engine = config.Config.engine
current_date = datetime.date(datetime.utcnow())

class ServerError(Exception):pass

def convert_str_to_date(string_date):
    return datetime.strptime(string_date, '%Y-%m-%d')

@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
        connection = engine.connect()
        connection.execute('USE students')
        user_id = connection.execute('SELECT id FROM records WHERE username="{}";'.format(session['username']))
        user_id = list(user_id)[0][0]
        upcoming_assesment_query = connection.execute('SELECT * FROM (SELECT * FROM assesments WHERE date>=(SELECT CURDATE() AS S) AND std_id={0}) AS T WHERE date=(SELECT MIN(date) FROM (SELECT * FROM assesments WHERE date>=(SELECT CURDATE() AS S) AND std_id={0}) AS T);'.format(user_id))
        upcoming_assesment = list(upcoming_assesment_query)
        if not upcoming_assesment: upcoming_assesment = None
        upcoming_assignment_query = connection.execute('SELECT * FROM (SELECT * FROM assignments WHERE deadline>=(SELECT CURDATE() AS S) AND std_id={0}) AS T WHERE deadline=(SELECT MIN(deadline) FROM (SELECT * FROM assignments WHERE deadline>=(SELECT CURDATE() AS S) AND std_id={0}) AS T);'.format(user_id))
        upcoming_assignment = list(upcoming_assignment_query)
        if not upcoming_assignment: upcoming_assignment = None
        connection.close()
        return render_template('index.html', user=session, upcoming_assesment=upcoming_assesment, upcoming_assignment=upcoming_assignment)
    return render_template('index.html', user=None, upcoming_assesment=None, upcoming_assignment=None)


@app.route('/init_db')
def init_db():
    connection = engine.connect()
    connection.execute('CREATE DATABASE IF NOT EXISTS students;')
    connection.execute('USE students;')
    connection.execute('CREATE TABLE records (id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, first_name NVARCHAR(30), last_name NVARCHAR(30), username NVARCHAR(30) UNIQUE, password_hash NVARCHAR(128));')
    # TODO: Add archive column for archived/completed assignments or assesments.
    connection.execute('CREATE TABLE assignments (asgn_id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, std_id INTEGER NOT NULL, subject NVARCHAR(30), details NVARCHAR(300), date DATE, teacher NVARCHAR(30), deadline DATE, completed BIT DEFAULT 0, FOREIGN KEY (std_id) REFERENCES records(id));')
    connection.execute('CREATE TABLE assesments (asses_id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, std_id INTEGER NOT NULL, subject NVARCHAR(30), details NVARCHAR(300), date DATE, teacher NVARCHAR(30), completed BIT DEFAULT 0, FOREIGN KEY (std_id) REFERENCES records(id));')
    # TODO: Add subjects to allow users to insert there marks and analyze it.
    # connection.execute('CREATE TABLE subjects (id INTEGER NOT NULL PRIMARY KEY, subject_name NVARCHAR(30), year INTEGER, part NVARCHAR(2))')
    connection.close()
    return "Database initialized successfully."

@app.route('/drop_db')
def drop_db():
    connection = engine.connect()
    connection.execute('DROP DATABASE students;')
    connection.close()
    return "Database dropped successfully."


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    connection = engine.connect()
    connection.execute('USE students;')
    if 'username' in session:
        return redirect(url_for('index'))
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = list(connection.execute('SELECT * FROM records WHERE username="{}";'.format(username)))
            if user != [] and check_password_hash(user[0][4], password):
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            connection.close()
            raise ServerError('Invalid Password.')
    except ServerError as e:
        flash(str(e))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    connection = engine.connect()
    connection.execute('USE students;')
    if 'username' in session:
        return redirect(url_for('index'))
    try:
        if request.method == 'POST':
            username = request.form['username'].lower()
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            password = request.form['password']
            password_hash = generate_password_hash(password)
            connection.execute('INSERT INTO records (first_name, last_name, username, password_hash) VALUES ("{0}", "{1}", "{2}", "{3}");'.format(first_name, last_name, username, password_hash))
            flash("Successfully Signed up.")
            connection.close()
            return redirect(url_for('index'))
    except ServerError as e:
        print(str(e))
    return render_template('signup.html', form=form)


@app.route('/assignments', methods=['GET'])
def get_assignments():
    connection = engine.connect()
    connection.execute('USE students;')
    if 'username' in session:
        # Upcoming Assignments
        assignments_query = connection.execute('SELECT * FROM assignments WHERE std_id = (SELECT id FROM records WHERE username="{}") AND completed=0 ORDER BY deadline ASC;'.format(session['username']))
        assignments = list(assignments_query)
        if not assignments: assignments = None
        # Completed Assignments
        com_assignments_query = connection.execute('SELECT * FROM assignments WHERE std_id = (SELECT id FROM records WHERE username="{}") AND completed=1 ORDER BY deadline DESC;'.format(session['username']))
        com_assignments = list(com_assignments_query)
        connection.close()
        return render_template('assignments.html', assignments=assignments, user=session, com_assignments=com_assignments)
    return redirect(url_for('index'))

@app.route('/add_assignments', methods=['GET', 'POST'])
def add_assignments():
    form = AssignmentsForm()
    connection = engine.connect()
    connection.execute('USE students')
    if 'username' in session:
        user = connection.execute('SELECT id FROM records WHERE username="{}";'.format(session['username']))
        std_id = list(user)[0][0]
        if request.method == 'POST':
            subject = request.form['subject']
            details = request.form['details']
            date = request.form['date']
            teacher = request.form['teacher']
            deadline = request.form['deadline']
            deadline_val = datetime.date(convert_str_to_date(deadline))
            completed = 0
            if deadline_val < current_date:
                completed = 1
            connection.execute('INSERT INTO assignments (subject, details, date, teacher, deadline, std_id, completed) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}", {6});'.format(subject, details, date, teacher, deadline, std_id, completed))
            flash("Successfully Added.")
            return redirect(url_for('get_assignments'))
    connection.close()
    return render_template('add_assignments.html', user=session, form=form)

@app.route('/assignments/<assignment_id>')
def get_assignment(assignment_id):
    connection = engine.connect()
    connection.execute('USE students')
    if 'username' in session:
        assignment = connection.execute('SELECT * FROM assignments WHERE asgn_id={};'.format(assignment_id))
        return render_template('assignment.html', assignments=assignment, user=session)
    connection.close()
    return redirect(url_for('index'))

@app.route('/assignments/<assignment_id>/update', methods=['GET', 'POST'])
def update_assignment(assignment_id):
    form = AssignmentsForm()
    connection = engine.connect()
    connection.execute('USE students;')
    if 'username' in session:
        if request.method == 'POST':
            subject = request.form['subject']
            details = request.form['details']
            date = request.form['date']
            teacher = request.form['teacher']
            deadline = request.form['deadline']
            deadline_val = datetime.date(convert_str_to_date(deadline))
            assignment = connection.execute('SELECT * FROM assignments WHERE asgn_id={};'.format(assignment_id))
            assignment = list(assignment)[0]
            if subject=="":
                subject = assignment[2]
            if details=="":
                details = assignment[3]
            if date=="":
                date = assignment[4]
            if teacher=="":
                teacher = assignment[5]
            if deadline=="":
                deadline = assignment[6]
            completed = 0
            if deadline_val < current_date:
                completed = 1
            connection.execute('UPDATE assignments SET subject="{0}", details="{1}", date="{2}", teacher="{3}", deadline="{4}", completed={5} WHERE asgn_id={6};'.format(subject, details, date, teacher, deadline, completed, assignment_id))
            flash('Successfully updated')
            return redirect(url_for('get_assignment', assignment_id=assignment_id))
    connection.close()
    return render_template('update_assignments.html', user=session, form=form)

@app.route('/assignments/<assignment_id>/delete')
def delete_assignment(assignment_id):
    connection = engine.connect()
    connection.execute('USE students;')
    if 'username' in session:
        connection.execute('DELETE FROM assignments WHERE asgn_id={};'.format(assignment_id))
        flash("Assignment Successfully deleted.")
        return redirect('/assignments')
    connection.close()
    return redirect(url_for('index'))

@app.route('/assesments', methods=['GET'])
def get_assesments():
    connection = engine.connect()
    connection.execute('USE students;')
    if 'username' in session:
        # Upcoming Assesments
        assesments_query = connection.execute('SELECT * FROM assesments WHERE std_id = (SELECT id FROM records WHERE username="{}") AND completed=0 ORDER BY date ASC;'.format(session['username']))
        assesments = list(assesments_query)
        # Completed Assesments
        com_assesments_query = connection.execute('SELECT * FROM assesments WHERE std_id = (SELECT id FROM records WHERE username="{}") AND completed=1 ORDER BY date DESC;'.format(session['username']))
        com_assesments = list(com_assesments_query)
        connection.close()
        return render_template('assesments.html', assesments=assesments, com_assesments=com_assesments, user=session)
    return redirect(url_for('index'))

@app.route('/add_assesments', methods=['GET', 'POST'])
def add_assesments():
    form = AssesmentsForm()
    connection = engine.connect()
    connection.execute('USE students')
    if 'username' in session:
        user = connection.execute('SELECT id FROM records WHERE username="{}";'.format(session['username']))
        std_id = list(user)[0][0]
        if request.method == 'POST':
            subject = request.form['subject']
            details = request.form['details']
            date = request.form['date']
            teacher = request.form['teacher']
            date_val = datetime.date(convert_str_to_date(date))
            completed = 0
            if date_val < current_date:
                completed = 1
            connection.execute('INSERT INTO assesments (subject, details, date, teacher, std_id, completed) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", {5});'.format(subject, details, date, teacher, std_id, completed))
            flash("Successfully Added.")
            return redirect(url_for('get_assesments'))
    connection.close()
    return render_template('add_assesments.html', user=session, form=form)

@app.route('/assesments/<assesment_id>')
def get_assesment(assesment_id):
    connection = engine.connect()
    connection.execute('USE students')
    if 'username' in session:
        assesment = connection.execute('SELECT * FROM assesments WHERE asses_id={};'.format(assesment_id))
        return render_template('assesment.html', assesments=assesment, user=session)
    connection.close()
    return redirect(url_for('index'))

@app.route('/assesments/<assesment_id>/update', methods=['GET', 'POST'])
def update_assesment(assesment_id):
    form = AssesmentsForm()
    connection = engine.connect()
    connection.execute('USE students')
    if 'username' in session:
        if request.method == 'POST':
            subject = request.form['subject']
            details = request.form['details']
            date = request.form['date']
            teacher = request.form['teacher']
            date_val = datetime.date(convert_str_to_date(date))
            assesment = connection.execute('SELECT * FROM assesments WHERE asses_id={};'.format(assesment_id))
            assesment = list(assesment)[0]
            if subject=="":
                subject = assesment[2]
            if details=="":
                details = assesment[3]
            if date=="":
                date = assesment[4]
            if teacher=="":
                teacher = assesment[5]
            completed = 0
            if date_val < current_date:
                completed = 1
            connection.execute('UPDATE assesments SET subject="{0}", details="{1}", date="{2}", teacher="{3}", completed={4} WHERE asses_id={5};'.format(subject, details, date, teacher, completed, assesment_id))
            flash('Successfully updated')
            return redirect(url_for('get_assesment', assesment_id=assesment_id))
    connection.close()
    return render_template('update_assesments.html', user=session, form=form)

@app.route('/assesments/<assesment_id>/delete')
def delete_assesment(assesment_id):
    connection = engine.connect()
    connection.execute('USE students')
    if 'username' in session:
        connection.execute('DELETE FROM assesments WHERE asses_id={};'.format(assesment_id))
        flash("Assesment Successfully deleted.")
        return redirect('/assesments')
    connection.close()
    return redirect(url_for('index'))

    
