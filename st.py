from flask import Flask, render_template, url_for, request, flash, redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
import sqlite3
import os



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
    extract_management_data = extract_management_fn()
    extract_department_data = extract_department_fn()
    extract_all_user = extract_all_user_fn()
    extract_count = extract_count_fn()
    return render_template('search.html', extract_count=extract_count, extract_all_user=extract_all_user, side_pos='active', extract_department_data=extract_department_data, extract_management_data=extract_management_data)

def extract_all_user_fn():
    conn = sqlite3.connect(path_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM card_user ")
    result = cursor.fetchall()
    print(result)
    return result


@app.route ('/search/dep_list', methods=['GET', 'POST'])
def dep_list():
    if request.method == 'POST':
        form = request.form
        dep_list_data = dep_list_fn(form)
        return render_template('dep_list.html', dep_list_data=dep_list_data)
    
def dep_list_fn(form):
    mgm_value = request.form['management']
    conn = sqlite3.connect(path_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mgm_dep WHERE management_name = ?", (mgm_value,))
    result = cursor.fetchall()
    conn.close()
    return result

@app.route('/card', methods=['GET', 'POST'])
def card():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        form_keys = request.form.keys()
        if 'management' in form_keys:
            value = form_data['management']
            data_type = 'management'
            extract_count_mgm_dep = extract_count_mgm_dep_fn(data_type,value)
            extract_user_data_search = extract_user_data_search_fn(value,data_type)
            if extract_user_data_search is None:
                return render_template('card_no_data.html')
            return render_template('card.html', extract_count_mgm_dep=extract_count_mgm_dep, extract_user_data_search=extract_user_data_search)
        if 'department' in form_keys:
            value = form_data['department']
            data_type = 'department'
            extract_user_data_search = extract_user_data_search_fn(value,data_type)
            extract_count_mgm_dep = extract_count_mgm_dep_fn(data_type,value)
            if extract_user_data_search is None:
                return render_template('card_no_data.html')
            return render_template('card.html', extract_count_mgm_dep=extract_count_mgm_dep, extract_user_data_search=extract_user_data_search)

def extract_count_mgm_dep_fn(data_type,value):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(user_name) FROM card_user WHERE {data_type}_name = ?", (value,))
    result = cursor.fetchone()[0]
    conn.close()
    return result


@app.route('/card_no_data', methods=['GET', 'POST'])
def card_no_data():
    return render_template('card_no_data.html')

def extract_user_data_search_fn(value, data_type):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(f"SELECT user_name FROM card_user WHERE {data_type}_name = ?", (value,))
    result = cursor.fetchone()
    if result is None:
        return result
    else:
        cursor.execute(f"SELECT management_name, department_name, job_name, user_name, user_card_text, photo_name, type_name FROM card_user WHERE {data_type}_name = ?", (value,))
        result = cursor.fetchall()
        print (result)
        return result

@app.route('/card_user', methods=['GET', 'POST'])
def card_user():
    extract_management_data = extract_management_fn()
    extract_department_data = extract_department_fn()
    extract_job_data = extract_job_fn()
    extract_user_name_data = extract_user_name_fn()
    extract_type_user = extract_type_user_fn()
    
    if request.method == 'POST' and 'photo' in request.files:
        form = request.form
        photo = request.files['photo']
        photo_name = secure_filename(photo.filename)
        file_path = 'static/uploads/photos/' + photo_name
        if os.path.exists(file_path):
            os.remove(file_path)
        photos.save(request.files['photo'])
        add_card_user_fn(form, photo_name)
        return render_template('card_user.html',  side_pos='active', extract_type_user=extract_type_user, extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data, extract_user_name_data=extract_user_name_data)
    
    if request.method == 'POST':
        form = request.form
        photo_name = 'no_photo.png'
        add_card_user_fn(form, photo_name)
        return render_template('card_user.html', side_pos='active', extract_type_user=extract_type_user, extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data, extract_user_name_data=extract_user_name_data)
    
    return render_template('card_user.html',  side_pos='active', extract_type_user=extract_type_user, extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data, extract_user_name_data=extract_user_name_data)

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
        photo_name = 'no_photo.png'
        add_card_user_fn(form, photo_name)
        return redirect(url_for('data'))
    
@app.route('/find/update', methods=['GET', 'POST'])
def find_update():    
    if request.method == 'POST' and 'photo' in request.files:
        form = request.form
        photo = request.files['photo']
        photo_name = secure_filename(photo.filename)
        file_path = 'static/uploads/photos/' + photo_name
        if os.path.exists(file_path):
            os.remove(file_path)
        photos.save(request.files['photo'])
        add_card_user_fn(form, photo_name)
        return redirect(url_for('search'))

    if request.method == 'POST':
        form = request.form
        # photo_name = 'no_photo.png'
        photo_name = extract_photo_name_fn(form)
        add_card_user_fn(form, photo_name)
        return redirect(url_for('search'))    

def extract_photo_name_fn(form):
    user = request.form['user']
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("SELECT photo_name FROM card_user WHERE user_name = ?", (user,))
    result = cursor.fetchone()
    if result:
        value = result[0]
        conn.close()
        return value
    
def add_card_user_fn(form, photo_name):
    management = request.form['management']
    department = request.form['department']
    job = request.form['job']
    user = request.form['user']
    user_card_text = request.form['user_card_text']
    type_user = request.form['type_user']
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
        cursor.execute("INSERT INTO card_user (management_name, department_name, job_name, user_name, user_card_text, photo_name, type_name) VALUES (?,?,?,?,?,?,?)", (management, department, job, user, user_card_text, photo_name, type_user))
        flash (f'{user} ', 'user_card_add-info')
    else:
        cursor.execute("UPDATE card_user SET management_name = ?, department_name = ?, job_name = ?, user_card_text = ?, photo_name = ?, type_name = ? WHERE user_name = ?", (management, department, job, user_card_text, photo_name, type_user, user))
        flash (f'{user} ', 'user_card_update-info')
    conn.commit()
    conn.close()

def create_table_card_user_fn():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS card_user (id INTEGER PRIMARY KEY, management_name varchar(300), department_name varchar(300), job_name varchar(300), user_name varchar(300), user_card_text text, photo_name varchar(300), type_name varchar(300))")
    conn.commit()
    conn.close()

@app.route('/data', methods=['GET', 'POST', 'PUT', 'DELETE'])
def data():
    extract_management_data = extract_management_fn()
    extract_department_data = extract_department_fn()
    extract_job_data = extract_job_fn()
    extract_user_name_data = extract_user_name_fn()
    extract_count = extract_count_fn()
 
    if request.method == 'POST':
        form = request.form
        add_data_fn(form)
        extract_management_data = extract_management_fn()
        extract_department_data = extract_department_fn()
        extract_job_data = extract_job_fn()
        extract_user_name_data = extract_user_name_fn()
        extract_count = extract_count_fn()
        return render_template('data.html', side_pos='active', extract_count=extract_count, extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data, extract_user_name_data=extract_user_name_data)
    return render_template('data.html', side_pos='active', extract_count=extract_count, extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data, extract_user_name_data=extract_user_name_data)

def extract_count_fn():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT management_name) FROM mgm_dep")
    mgm = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(department_name) FROM mgm_dep")
    dep = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(job_name) FROM job")
    job = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(user_name) FROM user")
    user = cursor.fetchone()[0]
    conn.close()
    print(mgm, dep, job, user)
    return mgm, dep, job, user

@app.route('/data/no_data', methods=['GET', 'POST'])
def no_data():
    no_data = request.form['no_data']
    if no_data == '':
        flash(f'{no_data} ', 'mgm_dep-nodata-info')
    return redirect(url_for('data'))

@app.route('/data/mgm_edit_modal', methods=['GET', 'POST'])
def mgm_edit_modal():
    if request.method == 'POST':
        form = request.form
        extract_management_data_modal = extract_management_data_modal_fn(form)
        return render_template('mgm_edit_modal.html', extract_management_data_modal = extract_management_data_modal)

def extract_management_data_modal_fn(form):
    management_edit = request.form['management_edit']
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT management_name FROM mgm_dep WHERE management_name = ?", (management_edit,))
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
    department_edit = request.form['department_edit']
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("SELECT department_name FROM mgm_dep WHERE department_name = ?", (department_edit,))
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
        extract_user_data_modal = extract_find_user_data_modal_fn(form)
        return render_template('user_edit_modal.html', extract_user_data_modal=extract_user_data_modal)
    
def extract_find_user_data_modal_fn(form):
    user_edit_id = request.form['user_edit_id']
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("SELECT user_name FROM user WHERE id = ?", (user_edit_id,))
    result = cursor.fetchone()
    if result:
        value = result[0]
        conn.close()
        return value

@app.route('/data/find_edit_modal', methods=['GET', 'POST'])
def find_edit_modal():
    if request.method == 'POST':
        form = request.form
        extract_user_name = extract_user_name_fn()
        extract_user_data_modal = extract_user_data_modal_fn(form)
        extract_management_data = extract_management_fn()
        extract_department_data = extract_department_fn()
        extract_job_data = extract_job_fn()
        return render_template('find_edit_modal.html', extract_user_name=extract_user_name, extract_user_data_modal=extract_user_data_modal, extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data)

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
            table_name = 'mgm_dep'
            table_name_card_user = 'card_user'
            value_new = form_data['management']
        if 'management_old' in form_keys:
            value_old = form_data['management_old']
            update_data_fn(table_name,value_new,type_data_new,value_old)
            card_user_change_data_fn(value_new,table_name_card_user,type_data_new,value_old)
            return redirect(url_for('data'))

        if 'department' in form_keys:
            type_data_new = 'department'
            table_name = 'mgm_dep'
            table_name_card_user = 'card_user'
            value_new = form_data['department']
        if 'department_old' in form_keys:
            value_old = form_data['department_old']
            update_data_fn(table_name,value_new,type_data_new,value_old)
            card_user_change_data_fn(value_new,table_name_card_user,type_data_new,value_old)
            return redirect(url_for('data'))
        
        if 'job' in form_keys:
            type_data_new = 'job'
            value_new = form_data['job']
            table_name = 'job'
            table_name_card_user = 'card_user'
        if 'job_old' in form_keys:
            value_old = form_data['job_old']
            update_data_fn(table_name,value_new,type_data_new,value_old)
            card_user_change_data_fn(value_new,table_name_card_user,type_data_new,value_old)
            return redirect(url_for('data'))
        
        if 'user' in form_keys:
            type_data_new = 'user'
            table_name = 'user'
            table_name_card_user = 'card_user'
            value_new = form_data['user']
        if 'user_old' in form_keys:
            value_old = form_data['user_old']
            update_data_fn(table_name,value_new,type_data_new,value_old)
            card_user_change_data_fn(value_new,table_name_card_user,type_data_new,value_old) 
            return redirect(url_for('data'))

def update_data_fn(table_name,value_new,type_data_new,value_old):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    # Существует запись или нет?
    cursor.execute(f"SELECT {type_data_new}_name FROM {table_name} WHERE {type_data_new}_name = ?", (value_new,))
    # Если запись не существует, заменить старую на новую
    result = cursor.fetchone()
    if result is None:
        cursor.execute(f"UPDATE {table_name} SET {type_data_new}_name = ? WHERE {type_data_new}_name = ?", (value_new, value_old))
        conn.commit()
        conn.close()

def card_user_change_data_fn(value_new,table_name_card_user,type_data_new,value_old):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {table_name_card_user} SET {type_data_new}_name = ? WHERE {type_data_new}_name = ?", (value_new, value_old))
    conn.commit()
    conn.close()

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
    if type_data == 'user':
        cursor.execute(f"DELETE FROM user WHERE user_name = ?", (value,))
        cursor.execute(f"DELETE FROM card_user WHERE user_name = ?", (value,))
        flash (f'{value} ', f'{type_data}-remove-info')
        conn.commit()
    if type_data == 'job':
        cursor.execute(f"DELETE FROM job WHERE job_name = ?", (value,))
        flash (f'{value} ', f'{type_data}-remove-info')
        conn.commit()
    if type_data == 'management':
        cursor.execute(f"DELETE FROM mgm_dep WHERE management_name = ?", (value,))
        flash (f'{value} ', f'{type_data}-remove-info')
        conn.commit()
    if type_data == 'department':
        cursor.execute(f"DELETE FROM mgm_dep WHERE department_name = ?", (value,))
        flash (f'{value} ', f'{type_data}-remove-info')
        conn.commit()    


def create_table_data_fn():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    type = [('Отпуск по беременности и родам',), ('Больничный',), ('Работает',)]
    cursor.execute("CREATE TABLE IF NOT EXISTS type_user (id INTEGER PRIMARY KEY, type_name varchar(300) UNIQUE)")
    cursor.executemany('INSERT OR IGNORE INTO type_user (type_name) VALUES (?)', type)
    cursor.execute("CREATE TABLE IF NOT EXISTS mgm_dep (id INTEGER PRIMARY KEY, management_name varchar(300), department_name varchar(300) UNIQUE)")
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
    if management and department != '':
        cursor.execute("INSERT OR REPLACE INTO mgm_dep (management_name, department_name) VALUES (?,?)", (management, department))
        flash (f'{management} и {department}', 'mgm_dep-info')

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
        cursor.execute("SELECT DISTINCT management_name FROM mgm_dep")
        management = cursor.fetchall()
        conn.close()
        return management
def extract_department_fn():
        conn = sqlite3.connect(path_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mgm_dep")
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

def extract_type_user_fn():
        conn = sqlite3.connect(path_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM type_user")
        type_user = cursor.fetchall()
        conn.close()
        return type_user

@app.route('/export', methods=['GET', 'POST'])
def export():
    return render_template('export.html', side_pos='active')


if __name__ == '__main__':
    app.run(debug=True)