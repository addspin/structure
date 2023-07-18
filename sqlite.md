# создание таблицы:
```sql
CREATE TABLE service (id integer, name varchar(100), type varchar(100), firm varchar(100), data_src integer, data_die integer);
CREATE TABLE service (id integer, name varchar(100), type varchar(100), firm varchar(100), data_src integer, data_die integer, vdel integer PRIMARY KEY AUTOINCREMENT NOT NULL);
```
# Таблица для сервисов

```sql
CREATE TABLE service (id integer, service_name varchar(300) PRIMARY KEY, service_url varchar(300), service_text text, service_owner varchar(300));
```

# Таблица для устройств

```sql
CREATE TABLE device (id integer, device_type_name varchar(300), device_inv varchar(300), device_ident varchar(300) PRIMARY KEY, device_text varchar(300));
```
# Таблица для типов устройств
```sql
CREATE TABLE device_type (device_type_name varchar(300) PRIMARY KEY);
```


# Таблица для пользователей
```sql
CREATE TABLE users (id integer, user_name varchar(300) PRIMARY KEY);
CREATE TABLE users (user_name varchar(300) PRIMARY KEY);
```

# Таблица для пользователей c данными
```sql
CREATE TABLE user_data (id integer, user_name varchar(300) PRIMARY KEY);
CREATE TABLE user_data (user_name varchar(300), service_name varchar(300), device_ident varchar(300));
CREATE TABLE user_data (user_name varchar(300), service_name_value varchar(300), service_url_value varchar(300), service_text_value varchar(1000), service_owner_value varchar(300), device_ident_value varchar(300), device_inv_value varchar(300), device_type_value varchar(300), device_text_value varchar(300));

CREATE TABLE service_data (user_name varchar(300), service_name varchar(300), service_url varchar(300), service_text varchar(1000), service_owner varchar(300));
CREATE TABLE object_data (user_name varchar(300), device_ident varchar(300), device_inv varchar(300), device_type varchar(300), device_text varchar(300));
```

# Создать таблицу если ее нет
```sql
create table if not exists users (user_name varchar(300) PRIMARY KEY);
```

PRIMARY KEY - не повторяющиеся занчение.
NOT NULL - значение не может быть null, это не одно и тоже с пустым значением.
DEFAULT "Нет информации" - значение по умолчанию, если ничего не прилетает.

# удаление таблицы:
```sql
DROP TABLE service;
DROP TABLE users;
DROP TABLE device;
DROP TABLE object_data;
DROP TABLE service_data;
DROP TABLE user_data;
DROP TABLE domain;


```

# список  имена столбцов:
```sql
PRAGMA table_info(service);
PRAGMA table_info(users);
PRAGMA table_info(device_type);
```

# Удлить все записи в таблице
```sql
DELETE FROM users;
```

# посмотреть содержимое таблицы:
```sql
SELECT * FROM service;
```

# колличество строк:
```sql
SELECT COUNT(id) FROM service;
SELECT Count(*) FROM service;
```

# Выведет все записи без повторений 
```sql
select * from service group by name;
```

# Удаление записи по имени
```sql
DELETE FROM service WHERE name = 'TEST';

 SELECT * FROM service where type='123';
 select * from service where service_name = 'test';
```

# Выбрать не нулевые значения service_name у пользователя agip-cloud 
```sql
select service_name  from user_data where user_name = 'agip-cloud' and service_name is not null;
```


SELECT EXISTS (SELECT * FROM service where service_name = ssh) 


# Выборка пользователей из AD
```powershell
 Get-ADUser -filter *  -SearchBase 'OU=AGIP-service-accounts,OU=AGIP,DC=intra,DC=apur' | select Name | Export-csv -path C:\distrib\project\user.csv -Append -Encoding UTF8
```