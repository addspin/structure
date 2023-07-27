from flask import Flask, render_template, url_for, request, flash, redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES
import sqlite3
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some random string'
path_db = 'db/st.db'

# Конфигурация загрузки файлов
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads/photos'  # Папка для сохранения загруженных фотографий
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


@app.route('/', methods=['GET', 'POST'])
def search():
    create_table_card_user_fn()
    create_table_data_fn()
    return render_template('search.html', side_pos='active')


@app.route('/card_user', methods=['GET', 'POST'])
def card_user():
    extract_management_data = extract_management_fn()
    extract_department_data = extract_department_fn()
    extract_job_data = extract_job_fn()
    extract_user_name_data = extract_user_name_fn()
    
    if request.method == 'POST' and 'photo' in request.files:
        form = request.form
        photo = request.files['photo']
        photo_name = secure_filename(photo.filename)
        file_path = 'static/uploads/photos/' + photo_name
        if os.path.exists(file_path):
            os.remove(file_path)
        photos.save(request.files['photo'])
        add_card_user_fn(form, photo_name)
        return render_template('card_user.html',  side_pos='active', extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data, extract_user_name_data=extract_user_name_data)
    
    if request.method == 'POST':
        form = request.form
        photo_name = 'no_photo.png'
        add_card_user_fn(form, photo_name)
        return render_template('card_user.html', side_pos='active', extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data, extract_user_name_data=extract_user_name_data)
    
    return render_template('card_user.html',  side_pos='active', extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data, extract_user_name_data=extract_user_name_data)

@app.route('/card_user/update', methods=['GET', 'POST'])
def card_user_update():    
    if request.method == 'POST' and 'photo' in request.files:
        form = request.form
        photo = request.files['photo']
        photo_name = secure_filename(photo.filename)
        file_path = 'static/uploads/photos/' + photo_name
        if os.path.exists(file_path):
            os.remove(file_path)
        photos.save(request.files['photo'])
        add_card_user_fn(form, photo_name)
        return redirect(url_for('data'))

    if request.method == 'POST':
        form = request.form
        photo_name = ''
        add_card_user_fn(form, photo_name)
        return redirect(url_for('data'))    
    
def add_card_user_fn(form, photo_name):
    management = request.form['management']
    department = request.form['department']
    job = request.form['job']
    user = request.form['user']
    user_card_text = request.form['user_card_text']
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    if management == '':
        flash (f'{management} ', 'user_card_nodata-info')
        return redirect(url_for('card_user'))
    if department == '':
        flash (f'{department} ', 'user_card_nodata-info')
        return redirect(url_for('card_user'))
    if job == '':
        flash (f'{job} ', 'user_card_nodata-info')
        return redirect(url_for('card_user'))
    if user == '':
        flash (f'{user} ', 'user_card_nodata-info')
        return redirect(url_for('card_user'))
    cursor.execute("SELECT user_name FROM card_user WHERE user_name = ?", (user,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO card_user (management_name, department_name, job_name, user_name, user_card_text, photo_name) VALUES (?,?,?,?,?,?)", (management, department, job, user, user_card_text, photo_name))
        flash (f'{user} ', 'user_card_add-info')
    else:
        cursor.execute("UPDATE card_user SET management_name = ?, department_name = ?, job_name = ?, user_card_text = ?, photo_name = ? WHERE user_name = ?", (management, department, job, user_card_text, photo_name, user))
        flash (f'{user} ', 'user_card_update-info')
    conn.commit()
    conn.close()

def create_table_card_user_fn():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS card_user (management_name varchar(300), department_name varchar(300), job_name varchar(300), user_name varchar(300) PRIMARY KEY, user_card_text text, photo_name varchar(300))")
    conn.commit()
    conn.close()

@app.route('/data', methods=['GET', 'POST', 'PUT', 'DELETE'])
def data():
   
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


@app.route('/data/mgm_edit_modal', methods=['GET', 'POST'])
def mgm_edit_modal():
    if request.method == 'POST':
        form = request.form
        extract_management_data_modal = extract_management_data_modal_fn(form)
        return render_template('mgm_edit_modal.html', extract_management_data_modal = extract_management_data_modal)

def extract_management_data_modal_fn(form):
    management_edit_id = request.form['management_edit_id']
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("SELECT management_name FROM management WHERE id = ?", (management_edit_id,))
    result = cursor.fetchone()
    if result:
        value = result[0]
        conn.close()
        return value

@app.route('/data/dep_edit_modal', methods=['GET', 'POST'])
def dep_edit_modal():
    if request.method == 'POST':
        form = request.form
        extract_department_data_modal = extract_department_data_modal_fn(form)
        return render_template('dep_edit_modal.html', extract_department_data_modal=extract_department_data_modal)
    
def extract_department_data_modal_fn(form):
    department_edit_id = request.form['department_edit_id']
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("SELECT department_name FROM department WHERE id = ?", (department_edit_id,))
    result = cursor.fetchone()
    if result:
        value = result[0]
        conn.close()
        return value

@app.route('/data/job_edit_modal', methods=['GET', 'POST'])
def job_edit_modal():
    if request.method == 'POST':
        form = request.form
        extract_job_data_modal = extract_job_data_modal_fn(form)
        return render_template('job_edit_modal.html', extract_job_data_modal=extract_job_data_modal)
    
def extract_job_data_modal_fn(form):
    job_edit_id = request.form['job_edit_id']
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("SELECT job_name FROM job WHERE id = ?", (job_edit_id,))
    result = cursor.fetchone()
    if result:
        value = result[0]
        conn.close()
        return value
    
@app.route('/data/user_edit_modal', methods=['GET', 'POST'])
def user_edit_modal():
    if request.method == 'POST':
        form = request.form
        extract_user_name = extract_user_name_fn()
        extract_user_data_modal = extract_user_data_modal_fn(form)
        extract_management_data = extract_management_fn()
        extract_department_data = extract_department_fn()
        extract_job_data = extract_job_fn()
        return render_template('user_edit_modal.html', extract_user_name=extract_user_name, extract_user_data_modal=extract_user_data_modal, extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data)
    
def extract_user_data_modal_fn(form):
    user_edit_name = request.form['user_edit_name']
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("SELECT management_name, department_name, job_name, user_name, user_card_text, photo_name FROM card_user WHERE user_name = ?", (user_edit_name,))
    result = cursor.fetchall()
    return result

@app.route('/data/update', methods=['PUT'])
def update():
    if request.method == 'PUT':
        form_data = request.form.to_dict()
        form_keys = request.form.keys()
        if 'management' in form_keys:
            type_data_new = 'management'
            value_new = form_data['management']
        if 'management_old' in form_keys:
            type_data_old = 'management_old'
            value_old = form_data['management_old']
            update_data_fn(value_new,type_data_new,value_old,type_data_old)
            return redirect(url_for('data'))

        if 'department' in form_keys:
            type_data_new = 'department'
            value_new = form_data['department']
        if 'department_old' in form_keys:
            type_data_old = 'department_old'
            value_old = form_data['department_old']
            update_data_fn(value_new,type_data_new,value_old,type_data_old)
            return redirect(url_for('data'))
        
        if 'job' in form_keys:
            type_data_new = 'job'
            value_new = form_data['job']
        if 'job_old' in form_keys:
            type_data_old = 'job_old'
            value_old = form_data['job_old']
            update_data_fn(value_new,type_data_new,value_old,type_data_old)
            return redirect(url_for('data'))
        
        if 'user' in form_keys:
            type_data_new = 'user'
            value_new = form_data['user']
        if 'user_old' in form_keys:
            type_data_old = 'user_old'
            value_old = form_data['user_old']
            update_data_fn(value_new,type_data_new,value_old,type_data_old)
            return redirect(url_for('data'))

def update_data_fn(value_new,type_data_new,value_old,type_data_old):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    # Существует запись или нет?
    cursor.execute(f"SELECT {type_data_new}_name FROM {type_data_new} WHERE {type_data_new}_name = ?", (value_new,))
    # Если запись не существует, заменить старую на новую
    result = cursor.fetchone()
    if result is None:
        cursor.execute(f"UPDATE {type_data_new} SET {type_data_new}_name = ? WHERE {type_data_new}_name = ?", (value_new, value_old))
        conn.commit()
        conn.close()
    # else:
    #      flash (f'{value_new} ', 'management-update-warning')

@app.route('/data/delete', methods=['DELETE', 'POST'])
def delete():
    if request.method == 'DELETE':
        form_data = request.form.to_dict()
        form_keys = request.form.keys()
        if 'management_delete_name' in form_keys:
            type_data = 'management'
            value = form_data['management_delete_name']
            delete_data_fn(value,type_data)
            return redirect(url_for('data'))
        if 'department_delete_name' in form_data:
            type_data = 'department'
            value = form_data['department_delete_name']
            delete_data_fn(value,type_data)
            return redirect(url_for('data'))
        if 'job_delete_name' in form_data:
            type_data = 'job'
            value = form_data['job_delete_name']
            delete_data_fn(value,type_data)
            return redirect(url_for('data'))
        if 'user_delete_name' in form_data:
            type_data = 'user'
            value = form_data['user_delete_name']
            delete_data_fn(value,type_data)
            return redirect(url_for('data'))
   
def delete_data_fn(value,type_data):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {type_data} WHERE {type_data}_name = ?", (value,))
    flash (f'{value} ', f'{type_data}-remove-info')
    conn.commit()
    conn.close()

def create_table_data_fn():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS management (id INTEGER PRIMARY KEY, management_name varchar(300) UNIQUE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS department (id INTEGER PRIMARY KEY, department_name varchar(300) UNIQUE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS job (id INTEGER PRIMARY KEY, job_name varchar(300) UNIQUE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, user_name varchar(300) UNIQUE)")
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

@app.route('/export', methods=['GET', 'POST'])
def export():
    return render_template('export.html', side_pos='active')


if __name__ == '__main__':
    app.run(debug=True)