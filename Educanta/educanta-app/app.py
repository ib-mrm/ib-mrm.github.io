import datetime
import pytz
import base64
from flask import Flask
from flask import render_template, request, Response, render_template_string, make_response
from functools import wraps

import sqlalchemy
import pandas as pd

from context import aws
from context import config
from context import databases
from context import general

import logging
logging.basicConfig(filename='app.log', level=logging.WARNING)

app = Flask(__name__)
app.config.from_object('settings_dev')
app.config.from_envvar('APP_SETTINGS', silent=True)

if app.config['ENV'] == 'prod':
    db = 'dbprod'
elif app.config['ENV'] == 'dev':
    db = 'dbdev'

conn = databases.get_connection(db)
cur = conn.cursor() # TODO: remove in favour of sqlalchemy

# tables
students_table = 'students'
projects_table = 'projects'
companies_table = 'companies'

# define login decorator
# source: https://techmonger.github.io/42/flask-basic-auth/
def check(authorization_header):
    encoded_userpass = authorization_header.split()[-1]
    expected_encoded_userpass = base64.b64encode(
        (config.site_username + ":" + config.site_password).encode()).decode()
    if encoded_userpass == expected_encoded_userpass:
        return True

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        if authorization_header and check(authorization_header):
            return f(*args, **kwargs)
        else:
            print("else")
            resp = Response()
            resp.headers['WWW-Authenticate'] = 'Basic'
            return resp, 401
        #return f(*args, **kwargs)

    return decorated

# start app routes
@app.route('/')
def start():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)

# Student signup
@app.route('/signup-student')
def submit_signup_student():
    return render_template("signup-student.html")

@app.route("/submit-signup-student", methods=["POST"])
def upload_signup_student():
    """
    Load student info into the database
    """
    try:
        name = request.form['name']
        email = request.form['email']
        school = request.form['school']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        tz = pytz.timezone("Europe/Stockholm")
        signup_at = datetime.datetime.now(tz)

        command = f"insert into {students_table} (id, name, email, school, start_date, end_date, signup_at) values(default, '{name}', '{email}', '{school}', '{start_date}', '{end_date}', '{signup_at}');"

        cur.execute(command)
        conn.commit()
        return render_template("success_signup.html")

    except Exception as e:
        conn.rollback()
        print(e)
        return render_template("error_signup.html")


# Company signup
@app.route('/signup-company')
def submit_signup_company():
    return render_template("signup-company.html")

@app.route("/submit-signup-company", methods=["POST"])
def upload_signup_company():
    """
    Load company info into the database
    """
    try:
        name = request.form['name']

        tz = pytz.timezone("Europe/Stockholm")
        signup_at = datetime.datetime.now(tz)

        command = f"insert into {companies_table}(id, name, signup_at) values(default, '{name}', '{signup_at}');"

        cur.execute(command)
        conn.commit()
        return render_template("success_signup.html")

    except Exception as e:
        conn.rollback()
        print(e)
        return render_template("error_signup.html")

# Project signup
@app.route('/signup-project')
def submit_signup_project():
    return render_template("signup-project.html")

@app.route("/submit-signup-project", methods=["POST"])
def upload_signup_project():
    """
    Load project info into the database
    """
    try:
        name = request.form['name']
        company = request.form['company_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        hours_per_week = request.form['hours_per_week']
        skills = request.form['skills']

        tz = pytz.timezone("Europe/Stockholm")
        signup_at = datetime.datetime.now(tz)

        command = f"insert into {projects_table} (id, name, company, start_date, end_date, hours_per_week, skills, signup_at) values(default, '{name}', '{company}', '{start_date}', '{end_date}', '{hours_per_week}', '{skills}', '{signup_at}');"

        cur.execute(command)
        conn.commit()
        return render_template("success_signup.html")

    except Exception as e:
        conn.rollback()
        print(e)
        return render_template("error_signup.html")

@app.route('/match')
def compute_matches():
    # Read required tables
    try:
        metadata = sqlalchemy.MetaData()
        engine = databases.get_engine(db)
        connection = engine.connect()
    except Exception as e:
        print("initial connect")
        print(e)
        raise(e)

    try:
        students = sqlalchemy.Table('students', metadata,
                        autoload=True, autoload_with=engine)
        projects = sqlalchemy.Table('projects', metadata,
                        autoload=True, autoload_with=engine)

        # Retrieve students table
        query = sqlalchemy.select(students)
        results = connection.execute(query).fetchall()
        df_students = pd.DataFrame(results)
        df_students.columns = results[0].keys()
        
        # Retrieve projects table
        query = sqlalchemy.select(projects)
        results = connection.execute(query).fetchall()
        df_projects = pd.DataFrame(results)
        df_projects.columns = results[0].keys()

    except Exception as e:
        print("reads from sqlalchemy")
        print(e)
        raise(e)

    try:
        df_matches = general.find_matches(df_students, df_projects)
    except Exception as e:
        print("df_matches")
        print(e)
        raise(e)

    print("just before render template")
    return make_response(render_template_string(df_matches.to_html()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)