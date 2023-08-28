from flask import Flask, render_template, url_for, request, flash, redirect, send_file, make_response, Response
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
import sqlite3
import os
import ssl
from flask_mail import Mail, Message
from celery import Celery
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some random string'
path_db = 'db/st.db'

app.config.from_object('config')
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE


client = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])


mail = Mail(app)
@client.task
def send_email(body):
    with app.app_context():
        msg = Message(subject=app.config['SUBJECT'], sender=app.config['SENDER'], recipients=app.config['RECIPIENTS'])
        msg.html = body
        mail.send(msg)

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
    cursor.execute("SELECT * FROM card_user WHERE user_name !=''")
    result = cursor.fetchall()
    return result

@app.route ('/search/dep_list', methods=['GET', 'POST'])
def dep_list():
    if request.method == 'POST':
        form = request.form
        dep_list_data = dep_list_fn(form)
        return render_template('dep_list.html', dep_list_data=dep_list_data)

@app.route ('/search/mgm_list', methods=['GET', 'POST'])
def mgm_list():
    if request.method == 'POST':
        form = request.form
        mgm_list_data = mgm_list_fn(form)
        extract_management_data = extract_management_fn()
        return render_template('mgm_list.html', extract_management_data=extract_management_data, mgm_list_data=mgm_list_data)
    
def mgm_list_fn(form):
    dep_value = request.form['department']
    conn = sqlite3.connect(path_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT management_name FROM mgm_dep WHERE department_name = ?", (dep_value,))
    result = cursor.fetchall()
    print(result)
    conn.close()
    return result

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
            extract_count_free, extract_count_mgm_dep = extract_count_mgm_dep_fn(data_type,value)
            extract_user_data_search = extract_user_data_search_fn(value,data_type)
            extract_free_job = extract_free_job_fn(value,data_type)
            if extract_user_data_search is None:
                return render_template('card_no_data.html')
            return render_template('card.html', extract_count_free=extract_count_free, extract_free_job=extract_free_job, extract_count_mgm_dep=extract_count_mgm_dep, extract_user_data_search=extract_user_data_search)

        if 'department' in form_keys:
            value = form_data['department']
            data_type = 'department'
            extract_user_data_search = extract_user_data_search_fn(value,data_type)
            extract_count_free, extract_count_mgm_dep = extract_count_mgm_dep_fn(data_type,value)
            extract_free_job = extract_free_job_fn(value,data_type)
            if extract_user_data_search is None:
                return render_template('card_no_data.html')
            return render_template('card.html', extract_count_free=extract_count_free, extract_free_job=extract_free_job, extract_count_mgm_dep=extract_count_mgm_dep, extract_user_data_search=extract_user_data_search)


def extract_count_mgm_dep_fn(data_type,value):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(user_name) FROM card_user WHERE {data_type}_name = ? AND user_name != '' ", (value,))
    result = cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(user_name) FROM card_user WHERE {data_type}_name = ? AND user_name = '' ", (value,))
    result2 = cursor.fetchone()[0]
    conn.close()
    return (result2, result)


@app.route('/card_no_data', methods=['GET', 'POST'])
def card_no_data():
    return render_template('card_no_data.html')

def extract_free_job_fn(value, data_type):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, management_name, department_name, job_name, user_name, user_card_text, photo_name, type_name FROM card_user WHERE {data_type}_name = ? AND user_name = ''", (value,))
    result = cursor.fetchall()
    return result
    
def extract_user_data_search_fn(value, data_type):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(f"SELECT user_name FROM card_user WHERE {data_type}_name = ?", (value,))
    result = cursor.fetchone()
    if result is None:
        return result
    else:
        cursor.execute(f"SELECT id, management_name, department_name, job_name, user_name, user_card_text, photo_name, type_name, mail_name, phone_long_name, phone_short_name FROM card_user WHERE {data_type}_name = ? AND user_name != '' ", (value,))
        result = cursor.fetchall()
        return result

@app.route('/card_user', methods=['GET', 'POST'])
def card_user():
    extract_management_data = extract_management_fn()
    extract_department_data = extract_department_fn()
    extract_job_data = extract_job_fn()
    extract_user_name_data = extract_user_name_fn()
    extract_type_user = extract_type_user_fn()
    extract_phone_data = extract_phone_data_fn()
    extract_mail_data = extract_mail_data_fn()
    
    if request.method == 'POST' and 'photo' in request.files:
        form = request.form
        photo = request.files['photo']
        photo_name = secure_filename(photo.filename)
        file_path = 'static/uploads/photos/' + photo_name
        if os.path.exists(file_path):
            os.remove(file_path)
        photos.save(request.files['photo'])
        add_card_user_fn(form, photo_name)
        return render_template('card_user.html',  side_pos='active', extract_mail_data=extract_mail_data, extract_phone_data=extract_phone_data, extract_type_user=extract_type_user, extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data, extract_user_name_data=extract_user_name_data)
    
    if request.method == 'POST':
        form = request.form
        photo_name = 'no_photo.png'
        add_card_user_fn(form, photo_name)
        return render_template('card_user.html', side_pos='active', extract_mail_data=extract_mail_data, extract_phone_data=extract_phone_data, extract_type_user=extract_type_user, extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data, extract_user_name_data=extract_user_name_data)
    
    return render_template('card_user.html',  side_pos='active', extract_mail_data=extract_mail_data, extract_phone_data=extract_phone_data, extract_type_user=extract_type_user, extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data, extract_user_name_data=extract_user_name_data)

def extract_phone_data_fn():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM phone")
    result = cursor.fetchall()
    conn.close()
    return result

def extract_mail_data_fn():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mail")
    result = cursor.fetchall()
    conn.close()
    return result

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
    
@app.route('/find/search_modal', methods=['GET', 'POST'])
def search_modal(): 
    return render_template('search_modal.html')   

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
        update_find_user_fn(form, photo_name)

        
        form_data = request.form.to_dict()
        form_keys = request.form.keys()
        
        if 'management' in form_keys:
            value = form_data['management']
            data_type = 'management'
            extract_user_data_search = extract_user_data_search_fn(value,data_type)
            extract_free_job = extract_free_job_fn(value,data_type)
            extract_count_free, extract_count_mgm_dep = extract_count_mgm_dep_fn(data_type,value)
            return render_template('update_search_mgm_dep.html', extract_count_free=extract_count_free, extract_count_mgm_dep=extract_count_mgm_dep, extract_user_data_search=extract_user_data_search, extract_free_job=extract_free_job)
            
        if 'department' in form_keys:
            value = form_data['department']
            data_type = 'department'
            extract_user_data_search = extract_user_data_search_fn(value,data_type)
            extract_free_job = extract_free_job_fn(value,data_type)
            extract_count_free, extract_count_mgm_dep = extract_count_mgm_dep_fn(data_type,value)
            return render_template('update_search_mgm_dep.html', extract_count_free=extract_count_free, extract_count_mgm_dep=extract_count_mgm_dep, extract_user_data_search=extract_user_data_search, extract_free_job=extract_free_job)

    if request.method == 'POST':
        form = request.form
        photo_name = extract_photo_name_fn(form)
        update_find_user_fn(form, photo_name)

        form_data = request.form.to_dict()
        form_keys = request.form.keys()
        
        if 'management' in form_keys:
            value = form_data['management']
            data_type = 'management'
            extract_user_data_search = extract_user_data_search_fn(value,data_type)
            extract_free_job = extract_free_job_fn(value,data_type)
            extract_count_free, extract_count_mgm_dep = extract_count_mgm_dep_fn(data_type,value)
            return render_template('update_search_mgm_dep.html', extract_count_free=extract_count_free, extract_count_mgm_dep=extract_count_mgm_dep, extract_user_data_search=extract_user_data_search, extract_free_job=extract_free_job)
            
        if 'department' in form_keys:
            value = form_data['department']
            data_type = 'department'
            extract_user_data_search = extract_user_data_search_fn(value,data_type)
            extract_free_job = extract_free_job_fn(value,data_type)
            return render_template('update_search_mgm_dep.html', extract_user_data_search=extract_user_data_search, extract_free_job=extract_free_job)

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
    else:
        value = 'no_photo.png'
        return value
    
def add_card_user_fn(form, photo_name):
    management = request.form['management']
    department = request.form['department']
    job = request.form['job']
    user = request.form['user']
    user_card_text = request.form['user_card_text']
    type_user = request.form['type_user']
    mail = request.form['mail']
    phone_long = request.form['phone_long']
    phone_short = request.form['phone_short']
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    #    Добавить свободную ставку
    if management != '' and department != '' and job != '' and type_user == 'Свободная ставка':
        cursor.execute("INSERT INTO card_user (management_name, department_name, job_name, user_name, user_card_text, photo_name, type_name, mail_name, phone_long_name, phone_short_name) VALUES (?,?,?,?,?,?,?,?,?,?)", (management, department, job, user, user_card_text, photo_name, type_user, mail, phone_long, phone_short))
        flash (f'Свободная ставка - {job} ', 'user_card_add-info')
        body = f'''<h5>Новая карточка пользователя:</h5><br> 
                <strong>Управление:</strong> {management}<br><br> 
                <strong>Отдел:</strong> {department}<br><br> 
                <strong>Должность:</strong> {job}<br><br>
                <strong>Примечание:</strong> {user_card_text}<br><br>
                <strong>Статус:</strong> {type_user}'''
        send_email.delay(body)
        conn.commit()
        return redirect(url_for('card_user'))
    # Проверка отправки пустой формы
    if  management == '' or department == '' or job == '' or user == '':
        flash (f'{management} ', 'user_card_nodata-info')
        return redirect(url_for('card_user'))

    #  Добавить новую карточку пользователя
    cursor.execute("SELECT user_name FROM card_user WHERE user_name = ?", (user,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO card_user (management_name, department_name, job_name, user_name, user_card_text, photo_name, type_name, mail_name, phone_long_name, phone_short_name) VALUES (?,?,?,?,?,?,?,?,?,?)", (management, department, job, user, user_card_text, photo_name, type_user, mail, phone_long, phone_short))
        flash (f'{user} ', 'user_card_add-info')
        body = f'''<h5>Новая карточка пользователя:</h5><br> 
                <strong>Пользователь:</strong>  {user}<br><br> 
                <strong>Управление:</strong> {management}<br><br> 
                <strong>Отдел:</strong> {department}<br><br> 
                <strong>Должность:</strong> {job}<br><br>
                <strong>Почта:</strong> {mail}<br>
                <strong>Городской номер:</strong> {phone_long}<br>
                <strong>Внутренний номер:</strong> {phone_short}<br>
                <strong>Примечание:</strong> {user_card_text}<br><br>
                <strong>Статус:</strong> {type_user}'''
        send_email.delay(body)
    else:
        cursor.execute("UPDATE card_user SET management_name = ?, department_name = ?, job_name = ?, user_card_text = ?, photo_name = ?, type_name = ? mail_name = ?, phone_long_name = ?, phone_short_name = ? WHERE user_name = ?", (management, department, job, user_card_text, photo_name, type_user, mail, phone_long, phone_short, user))
        flash (f'{user} ', 'user_card_update-info')
        body = f'''<h5>Карточка пользователя обновлена:</h5><br>
                <strong>Пользователь:</strong>  {user}<br><br> 
                <strong>Управление:</strong> {management}<br><br> 
                <strong>Отдел:</strong> {department}<br><br> 
                <strong>Должность:</strong> {job}<br><br>
                <strong>Почта:</strong> {mail}<br>
                <strong>Городской номер:</strong> {phone_long}<br>
                <strong>Внутренний номер:</strong> {phone_short}<br>
                <strong>Примечание:</strong> {user_card_text}<br><br>
                <strong>Статус:</strong> {type_user}'''
        send_email.delay(body)
    conn.commit()
    conn.close()

def update_find_user_fn(form, photo_name):
    management = request.form['management']
    old_management = request.form['old_management']
    department = request.form['department']
    old_department = request.form['old_department']
    job = request.form['job']
    old_job = request.form['old_job']
    user = request.form['user']
    old_user = request.form['old_user']
    user_card_text = request.form['user_card_text']
    old_user_card_text = request.form['old_user_card_text']
    type_user = request.form['type_user']
    old_type_user = request.form['old_type_user']
    free_job_id = request.form['free_job_id']
    mail = request.form['mail']
    old_mail = request.form['old_mail']
    phone_long = request.form['phone_long']
    old_phone_long = request.form['old_phone_long']
    phone_short = request.form['phone_short']
    old_phone_short = request.form['old_phone_short']
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

    
    if old_type_user == '':
        cursor.execute("DELETE FROM card_user WHERE management_name = ? AND department_name = ? AND job_name = ? AND type_name= ? AND id = ?", (old_management, old_department, old_job, old_type_user, free_job_id))

   
    # Добавить новую карточку пользователя
    if old_management == '' and old_department == '' and old_job == '' and old_user == '':
        cursor.execute("SELECT user_name FROM card_user WHERE user_name = ?", (user,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO card_user (management_name, department_name, job_name, user_name, user_card_text, photo_name, type_name) VALUES (?,?,?,?,?,?,?)", (management, department, job, user, user_card_text, photo_name, type_user))
            flash (f'{user} ', 'user_card_add-info')
    # Обновить карточку, перевести занятую ставку в "Свободную ставку"   
    if type_user == 'Свободная ставка' and user != '':
        cursor.execute("UPDATE card_user SET management_name = ?, department_name = ?, job_name = ?, user_name = ?, user_card_text = ?, photo_name = ?, type_name = ?, mail_name = ?, phone_long_name = ?, phone_short_name = ? WHERE id = ?", (management, department, job, '', user_card_text, 'no_photo.png', type_user, '', '', '', free_job_id))
        flash (f'{user} ', 'user_card_update-info')
        body = f'''<h5>Старая карточка пользователя:</h5><br>
                <strong>Пользователь:</strong>  {old_user}<br>
                <strong>Управление:</strong> {old_management}<br>
                <strong>Отдел:</strong> {old_department}<br>
                <strong>Должность:</strong> {old_job}<br>
                <strong>Почта:</strong> {old_mail}<br>
                <strong>Городской номер:</strong> {old_phone_long}<br>
                <strong>Внутренний номер:</strong> {old_phone_short}<br>
                <strong>Примечание:</strong> {old_user_card_text}<br>
                <strong>Статус:</strong> {old_type_user}<br><br>

                <h5>Новая карточка пользователя:</h5><br>
                <strong>Пользователь:</strong>  {user}<br>
                <strong>Управление:</strong> {management}<br>
                <strong>Отдел:</strong> {department}<br>
                <strong>Должность:</strong> {job}<br>
                <strong>Примечание:</strong> {user_card_text}<br>
                <strong>Статус:</strong> {type_user}<br><br><br><br>'''
        send_email.delay(body)

    # Обновить карточку со "Свободной ставкой"
    if type_user == 'Свободная ставка' and user == '':
        cursor.execute("UPDATE card_user SET management_name = ?, department_name = ?, job_name = ?, user_name = ?, user_card_text = ?, photo_name = ?, type_name = ? WHERE id = ?", (management, department, job, '', user_card_text, 'no_photo.png', type_user, free_job_id))
        flash (f' ', 'user_card_update-info')
        body = f'''<h5>Старая карточка пользователя:</h5><br>
                <strong>Пользователь:</strong>  {old_user}<br>
                <strong>Управление:</strong> {old_management}<br>
                <strong>Отдел:</strong> {old_department}<br>
                <strong>Должность:</strong> {old_job}<br>
                <strong>Примечание:</strong> {old_user_card_text}<br>
                <strong>Статус:</strong> {old_type_user}<br><br>

                <h5>Новая карточка пользователя:</h5><br>
                <strong>Пользователь:</strong>  {user}<br>
                <strong>Управление:</strong> {management}<br>
                <strong>Отдел:</strong> {department}<br>
                <strong>Должность:</strong> {job}<br>
                <strong>Примечание:</strong> {user_card_text}<br>
                <strong>Статус:</strong> {type_user}<br><br><br><br>'''
        send_email.delay(body)


    else:
        cursor.execute("SELECT user_name FROM card_user WHERE user_name = ? AND id != ?", (user, free_job_id))
        result = cursor.fetchone()
        if result is not None:
            flash (f'{user} ', 'user_card_user_name_exist-info')
        else:
            # Перевести свободную ставку в карточку пользователя
            if type_user != 'Свободная ставка' and old_type_user == "Свободная ставка":
                cursor.execute("UPDATE card_user SET management_name = ?, department_name = ?, job_name = ?, user_name = ?, user_card_text = ?, photo_name = ?, type_name = ?, mail_name = ?, phone_long_name = ?, phone_short_name = ? WHERE id = ?", (management, department, job, user, user_card_text, photo_name, type_user, mail, phone_long, phone_short, free_job_id))
                flash (f'{old_user} ', 'user_card_update-info')
                body = f'''<h5>Старая карточка пользователя:</h5><br>
                        <strong>Пользователь:</strong>  {old_user}<br>
                        <strong>Управление:</strong> {old_management}<br>
                        <strong>Отдел:</strong> {old_department}<br>
                        <strong>Должность:</strong> {old_job}<br>
                        <strong>Примечание:</strong> {old_user_card_text}<br>
                        <strong>Статус:</strong> {old_type_user}<br><br>

                        <h5>Новая карточка пользователя:</h5><br>
                        <strong>Пользователь:</strong>  {user}<br>
                        <strong>Управление:</strong> {management}<br>
                        <strong>Отдел:</strong> {department}<br>
                        <strong>Должность:</strong> {job}<br>
                        <strong>Почта:</strong> {mail}<br>
                        <strong>Городской номер:</strong> {phone_long}<br>
                        <strong>Внутренний номер:</strong> {phone_short}<br>
                        <strong>Примечание:</strong> {user_card_text}<br>
                        <strong>Статус:</strong> {type_user}<br><br><br><br>'''
                send_email.delay(body)
            # Обновить карточку
            if type_user != 'Свободная ставка' and old_type_user != "Свободная ставка":
                cursor.execute("UPDATE card_user SET management_name = ?, department_name = ?, job_name = ?, user_name = ?, user_card_text = ?, photo_name = ?, type_name = ?, mail_name = ?, phone_long_name = ?, phone_short_name =? WHERE id = ?", (management, department, job, user, user_card_text, photo_name, type_user, mail, phone_long, phone_short, free_job_id))
                flash (f'{old_user} ', 'user_card_update-info')
                body = f'''<h5>Старая карточка пользователя:</h5><br>
                        <strong>Пользователь:</strong>  {old_user}<br>
                        <strong>Управление:</strong> {old_management}<br>
                        <strong>Отдел:</strong> {old_department}<br>
                        <strong>Должность:</strong> {old_job}<br>
                        <strong>Почта:</strong> {old_mail}<br>
                        <strong>Городской номер:</strong> {old_phone_long}<br>
                        <strong>Внутренний номер:</strong> {old_phone_short}<br>
                        <strong>Примечание:</strong> {old_user_card_text}<br>
                        <strong>Статус:</strong> {old_type_user}<br><br>

                        <h5>Новая карточка пользователя:</h5><br>
                        <strong>Пользователь:</strong>  {user}<br>
                        <strong>Управление:</strong> {management}<br>
                        <strong>Отдел:</strong> {department}<br>
                        <strong>Должность:</strong> {job}<br>
                        <strong>Почта:</strong> {mail}<br>
                        <strong>Городской номер:</strong> {phone_long}<br>
                        <strong>Внутренний номер:</strong> {phone_short}<br>
                        <strong>Примечание:</strong> {user_card_text}<br>
                        <strong>Статус:</strong> {type_user}<br><br><br><br>'''
                send_email.delay(body)
    conn.commit()
    conn.close()

def create_table_card_user_fn():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS card_user (id INTEGER PRIMARY KEY, management_name varchar(300), department_name varchar(300), job_name varchar(300), user_name varchar(300), user_card_text text, photo_name varchar(300), type_name varchar(300), mail_name varchar(300), phone_long_name varchar(300), phone_short_name varchar(300))")
    conn.commit()
    conn.close()

@app.route('/data', methods=['GET', 'POST', 'PUT', 'DELETE'])
def data():
    extract_management_data = extract_management_fn()
    extract_department_data = extract_department_fn()
    extract_job_data = extract_job_fn()
    extract_user_name_data = extract_user_name_fn()
    extract_count = extract_count_fn()
    extract_phone_data = extract_phone_data_fn()
    extract_mail_data = extract_mail_data_fn()
 
    if request.method == 'POST':
        form = request.form
        add_data_fn(form)
        extract_management_data = extract_management_fn()
        extract_department_data = extract_department_fn()
        extract_job_data = extract_job_fn()
        extract_user_name_data = extract_user_name_fn()
        extract_count = extract_count_fn()
        extract_phone_data = extract_phone_data_fn()
        extract_mail_data = extract_mail_data_fn()
        return render_template('data.html', side_pos='active', extract_mail_data=extract_mail_data, extract_phone_data=extract_phone_data, extract_count=extract_count, extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data, extract_user_name_data=extract_user_name_data)
    return render_template('data.html', side_pos='active', extract_mail_data=extract_mail_data, extract_phone_data=extract_phone_data, extract_count=extract_count, extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data, extract_user_name_data=extract_user_name_data)

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
    cursor.execute("SELECT COUNT(user_name) FROM card_user where type_name = 'Свободная ставка'")
    user_free = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(user_name) FROM card_user where user_name != ''")
    user_in_card = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(mail_name) FROM mail")
    mail = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(phone_name) FROM phone")
    phone = cursor.fetchone()[0]
    conn.close()
    return mgm, dep, job, user, user_free, user_in_card, mail, phone

@app.route('/data/no_data', methods=['GET', 'POST'])
def no_data():
    no_data = request.form['no_data']
    if no_data == 'card_user':
        flash(f'{no_data} ', 'user_card_nodata-info')
        return redirect(url_for('card_user'))
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

@app.route('/data/mail_edit_modal', methods=['GET', 'POST'])
def mail_edit_modal():
    if request.method == 'POST':
        form = request.form
        extract_mail_data_modal = extract_mail_data_modal_fn(form)
        return render_template('mail_edit_modal.html', extract_mail_data_modal=extract_mail_data_modal)

def extract_mail_data_modal_fn(form):
    mail_edit_id = request.form['mail_edit_id']
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("SELECT mail_name FROM mail WHERE id = ?", (mail_edit_id,))
    result = cursor.fetchone()
    if result:
        value = result[0]
        conn.close()
        return value

@app.route('/data/phone_edit_modal', methods=['GET', 'POST'])
def phone_edit_modal():
    if request.method == 'POST':
        form = request.form
        extract_phone_data_modal = extract_phone_data_modal_fn(form)
        return render_template('phone_edit_modal.html', extract_phone_data_modal=extract_phone_data_modal)

def extract_phone_data_modal_fn(form):
    phone_edit_id = request.form['phone_edit_id']
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute("SELECT phone_name FROM phone WHERE id = ?", (phone_edit_id,))
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
        free_job_id = request.form['free_job_id']
        old_type_user = request.form['old_type_user']
        extract_user_name = extract_user_name_fn()
        extract_user_data_modal = extract_user_data_modal_fn(form)
        extract_management_data = extract_management_fn()
        extract_department_data = extract_department_fn()
        extract_job_data = extract_job_fn()
        extract_type_user = extract_type_user_fn()
        extract_mail_data = extract_mail_data_fn()
        extract_phone_data = extract_phone_data_fn()
        return render_template('find_edit_modal.html', extract_phone_data=extract_phone_data, extract_mail_data=extract_mail_data, old_type_user=old_type_user, free_job_id=free_job_id, extract_type_user=extract_type_user, extract_user_name=extract_user_name, extract_user_data_modal=extract_user_data_modal, extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data)

@app.route('/data/find_edit_free_job_modal', methods=['GET', 'POST'])
def find_edit_free_job_modal():
    if request.method == 'POST':
        form = request.form
        free_job_id = request.form['free_job_id']
        old_type_user = request.form['old_type_user']
        extract_user_name = extract_user_name_fn()
        extract_user_data_modal = extract_user_data_modal_fn(form)
        extract_management_data = extract_management_fn()
        extract_department_data = extract_department_fn()
        extract_job_data = extract_job_fn()
        extract_type_user = extract_type_user_fn()
        extract_mail_data = extract_mail_data_fn()
        extract_phone_data = extract_phone_data_fn()
        return render_template('find_edit_free_job_modal.html', extract_phone_data=extract_phone_data, extract_mail_data=extract_mail_data, old_type_user=old_type_user, free_job_id=free_job_id, extract_type_user=extract_type_user, extract_user_name=extract_user_name, extract_user_data_modal=extract_user_data_modal, extract_management_data=extract_management_data, extract_department_data=extract_department_data, extract_job_data=extract_job_data)


def extract_user_data_modal_fn(form):
    user_edit_name = request.form['user_edit_name']
    free_job_id = request.form['free_job_id']
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    if user_edit_name != '':
        cursor.execute("SELECT id, management_name, department_name, job_name, user_name, user_card_text, photo_name, type_name, mail_name, phone_long_name, phone_short_name FROM card_user WHERE user_name = ?", (user_edit_name,))
        result = cursor.fetchall()
        return result
    if user_edit_name == '':
        cursor.execute("SELECT id, management_name, department_name, job_name, user_name, user_card_text, photo_name, type_name, mail_name, phone_long_name, phone_short_name FROM card_user WHERE id = ?", (free_job_id,))
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
        
        if 'phone' in form_keys:
            type_data_new = 'phone'
            value_new = form_data['phone']
            table_name = 'phone'
            table_name_card_user = 'card_user'
        if 'phone_old' in form_keys:
            value_old = form_data['phone_old']
            update_data_fn(table_name,value_new,type_data_new,value_old)
            return redirect(url_for('data'))

        if 'mail' in form_keys:
            type_data_new = 'mail'
            table_name = 'mail'
            table_name_card_user = 'card_user'
            value_new = form_data['mail']
        if 'mail_old' in form_keys:
            value_old = form_data['mail_old']
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
        if type_data_new == 'management':
            body = f'''<h5>Изменение названия Управления</h5><br> 
                    <strong>Старое:</strong> {value_old}<br>
                    <strong>Новое:</strong> {value_new}'''
            flash (f'{value_old} изменена на {value_new}', 'data_update-info')
            send_email.delay(body)
        if type_data_new == 'department':
            body = f'''<h5>Изменение названия Отдела</h5><br> 
                    <strong>Старое:</strong> {value_old}<br>
                    <strong>Новое:</strong> {value_new}'''
            flash (f'{value_old} изменена на {value_new}', 'data_update-info')
            send_email.delay(body)
        if type_data_new == 'job':
            body = f'''<h5>Изменение названия Должности</h5><br> 
                    <strong>Старое:</strong> {value_old}<br>
                    <strong>Новое:</strong> {value_new}'''
            flash (f'{value_old} изменена на {value_new}', 'data_update-info')
            send_email.delay(body)
        if type_data_new == 'user':
            body = f'''<h5>Изменение ФИО пользователя</h5><br> 
                    <strong>Старое:</strong> {value_old}<br>
                    <strong>Новое:</strong> {value_new}'''
            flash (f'{value_old} изменена на {value_new}', 'data_update-info')
            send_email.delay(body)
        if type_data_new == 'phone':
            body = f'''<h5>Изменение номера телефона</h5><br> 
                    <strong>Старый:</strong> {value_old}<br>
                    <strong>Новый:</strong> {value_new}'''
            flash (f'{value_old} изменен на {value_new}', 'data_update-info')
            send_email.delay(body)
        if type_data_new == 'mail':
            body = f'''<h5>Изменение адреса почты</h5><br> 
                    <strong>Старый:</strong> {value_old}<br>
                    <strong>Новый:</strong> {value_new}'''
            flash (f'{value_old} изменен на {value_new}', 'data_update-info')
            send_email.delay(body)
        

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
        if 'phone_delete_name' in form_data:
            type_data = 'phone'
            value = form_data['phone_delete_name']
            delete_data_fn(value,type_data)
            return redirect(url_for('data'))
        if 'mail_delete_name' in form_data:
            type_data = 'mail'
            value = form_data['mail_delete_name']
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
        body = f'''<h5>Удаление пользователя</h5><br>
                <strong>Пользователь:</strong> {value}'''
        send_email.delay(body)
    if type_data == 'job':
        cursor.execute(f"DELETE FROM job WHERE job_name = ?", (value,))
        flash (f'{value} ', f'{type_data}-remove-info')
        conn.commit()
        body = f'''<h5>Удаление должности</h5><br>
                <strong>Должность:</strong> {value}'''
        send_email.delay(body)
    if type_data == 'phone':
        cursor.execute(f"DELETE FROM phone WHERE phone_name = ?", (value,))
        flash (f'{value} ', f'{type_data}-remove-info')
        conn.commit()
        body = f'''<h5>Удаление телефона</h5><br>
                <strong>Телефон:</strong> {value}'''
        send_email.delay(body)
    if type_data == 'mail':
        cursor.execute(f"DELETE FROM mail WHERE mail_name = ?", (value,))
        flash (f'{value} ', f'{type_data}-remove-info')
        conn.commit()
        body = f'''<h5>Удаление почтового адреса</h5><br>
                <strong>Почтовый адрес:</strong> {value}'''
        send_email.delay(body)
    if type_data == 'management':
        # если в управлении не осталось ни одного пользователя, удаляем управление
        cursor.execute(f"SELECT management_name FROM card_user WHERE management_name = ?", (value,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute(f"DELETE FROM mgm_dep WHERE management_name = ?", (value,))
            flash (f'{value} ', f'{type_data}-remove-info')
            conn.commit()
            body = f'''<h5>Удаление управления</h5><br>
                    <strong>Управление:</strong> {value}'''
            send_email.delay(body)
        else:
            flash (f'{value} ', f'{type_data}-noremove-info')

    if type_data == 'department':
        # если в отделе не осталось ни одного пользователя, удаляем отдел
        cursor.execute(f"SELECT department_name FROM card_user WHERE department_name = ?", (value,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute(f"DELETE FROM mgm_dep WHERE department_name = ?", (value,))
            flash (f'{value} ', f'{type_data}-remove-info')
            conn.commit()
        else:
            flash (f'{value} ', f'{type_data}-noremove-info')
    conn.close()


def create_table_data_fn():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    type = [('Отпуск по беременности и родам',), ('Больничный',), ('Работает',), ('Свободная ставка',)]
    cursor.execute("CREATE TABLE IF NOT EXISTS type_user (id INTEGER PRIMARY KEY, type_name varchar(300) UNIQUE)")
    cursor.executemany('INSERT OR IGNORE INTO type_user (type_name) VALUES (?)', type)
    cursor.execute("CREATE TABLE IF NOT EXISTS mgm_dep (id INTEGER PRIMARY KEY, management_name varchar(300), department_name varchar(300) UNIQUE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS job (id INTEGER PRIMARY KEY, job_name varchar(300) UNIQUE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, user_name varchar(300) UNIQUE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS phone (id INTEGER PRIMARY KEY, phone_name varchar(300) UNIQUE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS mail (id INTEGER PRIMARY KEY, mail_name varchar(300) UNIQUE)")
    conn.commit()
    conn.close()

def add_data_fn(form):
    management = request.form['management']
    department = request.form['department']
    job = request.form['job']
    user = request.form['user']
    mail = request.form['mail']
    phone_long = request.form['phone_long']
    phone_short = request.form['phone_short']
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    if management and department != '':
        cursor.execute(f"SELECT management_name FROM mgm_dep WHERE management_name = ?", (management,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO mgm_dep (management_name, department_name) VALUES (?,?)", (management, department))
            flash (f'{management} и {department}', 'mgm_dep-info')
            body = f'''<h5>Добавление управления и отдела</h5><br>
                    Добавлено управление: <strong>{management}</strong><br>Добавлен отдел: <strong>{department}</strong>'''
            send_email.delay(body)
        if result is not None:
            cursor.execute("SELECT department_name FROM mgm_dep WHERE department_name = ?", (department,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute("INSERT INTO mgm_dep (management_name, department_name) VALUES (?,?)", (management, department))
                flash (f'{department}', 'mgm_dep-info')
                body = f'''<h5>Добавление нового отдела в управление</h5><br>
                        В управление: <strong>{management}</strong><br>Добавлен отдел: <strong>{department}</strong>'''
                send_email.delay(body)
            else:
                flash (f'{department}', 'management-update-warning')
    if job != '':
        cursor.execute("INSERT OR REPLACE INTO job (job_name) VALUES (?)", (job,))
        flash (f'{job} ', 'add-info')
        body = f'Добавлена новая должность: <strong>{job}</strong>'
        send_email.delay(body)
    if user != '':
        cursor.execute("INSERT OR REPLACE INTO user (user_name) VALUES (?)", (user,))
        flash (f'{user} ', 'add-info')
        body = f'Добавлен новый пользователь: <strong>{user}</strong>'
        send_email.delay(body)
    if mail != '':
        cursor.execute("INSERT OR REPLACE INTO mail (mail_name) VALUES (?)", (mail,))
        flash (f'{mail} ', 'add-info')
        body = f'Добавлен новый почтовый адрес: <strong>{mail}</strong>'
        send_email.delay(body)
    if phone_long != '':
        cursor.execute("INSERT OR REPLACE INTO phone (phone_name) VALUES (?)", (phone_long,))
        flash (f'{phone_long} ', 'add-info')
        body = f'Добавлен новый городской номер телефона: <strong>{phone_long}</strong>'
        send_email.delay(body)
    if phone_short != '':
        cursor.execute("INSERT OR REPLACE INTO phone (phone_name) VALUES (?)", (phone_short,))
        flash (f'{phone_short} ', 'add-info')
        body = f'Добавлен новый внутренний номер телефона: <strong>{phone_short}</strong>'
        send_email.delay(body)
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
    conn = sqlite3.connect(path_db)
    export_data = pd.read_sql('SELECT * FROM card_user' ,conn)

    # Замена имен колонок
    export_data = export_data.rename(columns={'management_name': 'Управления:', 'department_name': 'Отделы:', 'job_name': 'Должность:', 'user_name': 'ФИО:', 'user_card_text': 'Примечания:', 'type_name': 'Статус:', 'mail_name': 'Почта:', 'phone_long_name': 'Городской номер:', 'phone_short_name': 'Внутренний номер:'})
    
    # Исключение колонок
    columns_to_exclude = ['id', 'photo_name']
    export_data = export_data.drop(columns_to_exclude, axis=1)

    export_data.to_excel('export/structure.xlsx', index=False)
    export_path = 'export/structure.xlsx'  # Путь для сохранения файла в формате Excel
    conn.close()

    # Создание файла Excel с помощью openpyxl
    workbook = Workbook()
    sheet = workbook.active

    # Запись данных в файл Excel
    for row in dataframe_to_rows(export_data, index=False, header=True):
        sheet.append(row)

    # Сохранение файла
    workbook.save(export_path)

    return send_file(export_path, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    

if __name__ == '__main__':
    app.run(debug=True)