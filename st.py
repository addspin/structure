from flask import Flask, render_template, url_for, request, jsonify, session, flash, redirect, send_file
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some random string'
path_db = 'db/st.db'

@app.route('/', methods=['GET', 'POST'])
def search():
    return render_template('search.html', side_pos='active')


@app.route('/card_user', methods=['GET', 'POST'])
def card_user():
    return render_template('card_user.html', side_pos='active')

@app.route('/data', methods=['GET', 'POST'])
def data():
    extract_management_data = extract_management_fn()
    extract_department_data = extract_department_fn()
    extract_job_data = extract_job_fn()
    if request.method == 'POST':
        form = request.form
        add_data_fn(form)
        extract_management_data = extract_management_fn()
        extract_department_data = extract_department_fn()
        extract_job_data = extract_job_fn()
        return render_template('data.html', side_pos='active', extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data)
    return render_template('data.html', side_pos='active', extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data)

def add_data_fn(form):
    management = request.form['management']
    department = request.form['department']
    job = request.form['job']
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS management (management_name varchar(300) PRIMARY KEY)")
    cursor.execute("CREATE TABLE IF NOT EXISTS department (department_name varchar(300) PRIMARY KEY)")
    cursor.execute("CREATE TABLE IF NOT EXISTS job (job_name varchar(300) PRIMARY KEY)")
    if management != '':
        cursor.execute("INSERT OR REPLACE INTO management (management_name) VALUES (?)", (management,))
        flash (f'{management} ', 'management-info')
    if department != '':
        cursor.execute("INSERT OR REPLACE INTO department (department_name) VALUES (?)", (department,))
        flash (f'{department} ', 'department-info')
    if job != '':
        cursor.execute("INSERT OR REPLACE INTO job (job_name) VALUES (?)", (job,))
        flash (f'{job} ', 'job-info')
    conn.commit()
    conn.close()

def extract_management_fn():
        conn = sqlite3.connect(path_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM management")
        management = cursor.fetchall()
        conn.close()
        return management
def extract_department_fn():
        conn = sqlite3.connect(path_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM department")
        department = cursor.fetchall()
        conn.close()
        return department
def extract_job_fn():
        conn = sqlite3.connect(path_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM job")
        job = cursor.fetchall()
        conn.close()
        return job


@app.route('/export', methods=['GET', 'POST'])
def export():
    return render_template('export.html', side_pos='active')


if __name__ == '__main__':
    app.run(debug=True)