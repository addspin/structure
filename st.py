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
    extract_management_data = extract_management_fn()
    extract_department_data = extract_department_fn()
    extract_job_data = extract_job_fn()
    extract_user_name_data = extract_user_name_fn()
    return render_template('card_user.html', side_pos='active', extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data, extract_user_name_data=extract_user_name_data)

def create_table_card_user_fn():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS card_user (management_name varchar(300), department_name varchar(300), job_name varchar(300), user_name varchar(300), user_card_text text)")
    conn.commit()
    conn.close()
    
@app.route('/data', methods=['GET', 'POST'])
def data():
    create_table_data_fn()
    extract_management_data = extract_management_fn()
    extract_department_data = extract_department_fn()
    extract_job_data = extract_job_fn()
    extract_user_name_data = extract_user_name_fn()
    if request.method == 'POST':
        form = request.form
        add_data_fn(form)
        extract_management_data = extract_management_fn()
        extract_department_data = extract_department_fn()
        extract_job_data = extract_job_fn()
        extract_user_name_data = extract_user_name_fn()
        return render_template('data.html', side_pos='active', extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data, extract_user_name_data=extract_user_name_data)
    return render_template('data.html', side_pos='active', extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data, extract_user_name_data=extract_user_name_data)

def create_table_data_fn():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS management (management_name varchar(300) PRIMARY KEY)")
    cursor.execute("CREATE TABLE IF NOT EXISTS department (department_name varchar(300) PRIMARY KEY)")
    cursor.execute("CREATE TABLE IF NOT EXISTS job (job_name varchar(300) PRIMARY KEY)")
    cursor.execute("CREATE TABLE IF NOT EXISTS user (user_name varchar(300) PRIMARY KEY)")
    conn.commit()
    conn.close()

def add_data_fn(form):
    management = request.form['management']
    department = request.form['department']
    job = request.form['job']
    user = request.form['user']
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    if management != '':
        cursor.execute("INSERT OR REPLACE INTO management (management_name) VALUES (?)", (management,))
        flash (f'{management} ', 'management-info')
    if department != '':
        cursor.execute("INSERT OR REPLACE INTO department (department_name) VALUES (?)", (department,))
        flash (f'{department} ', 'department-info')
    if job != '':
        cursor.execute("INSERT OR REPLACE INTO job (job_name) VALUES (?)", (job,))
        flash (f'{job} ', 'job-info')
    if user != '':
        cursor.execute("INSERT OR REPLACE INTO user (user_name) VALUES (?)", (user,))
        flash (f'{user} ', 'user-info')
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

def extract_user_name_fn():
        conn = sqlite3.connect(path_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        user = cursor.fetchall()
        conn.close()
        return user
@app.route('/remove_data', methods=['GET', 'POST'])
def remove_data():
    if request.method == 'POST':
        form = request.form
        remove_data_fn(form)
    return redirect(url_for('data'))

def remove_data_fn(form):
    management = request.form['management']
    department = request.form['department']
    job = request.form['job']
    user = request.form['user']
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    if management != '':
        cursor.execute("DELETE FROM management WHERE management_name = ?", (management,))
        flash (f'{management} ', 'management-remove-info')
    if department != '':
        cursor.execute("DELETE FROM department WHERE department_name = ?", (department,))
        flash (f'{department} ', 'department-remove-info')
    if job != '':
        cursor.execute("DELETE FROM job WHERE job_name = ?", (job,))
        flash (f'{job} ', 'job-remove-info')
    if user != '':
        cursor.execute("DELETE FROM user WHERE user_name = ?", (user,))
        flash (f'{user} ', 'user-remove-info')
    conn.commit()
    conn.close()

@app.route('/export', methods=['GET', 'POST'])
def export():
    return render_template('export.html', side_pos='active')


if __name__ == '__main__':
    app.run(debug=True)