import sqlite3, json
from PyQt5.QtCore import QDateTime,QDate,QTime

'''
   ####   ####       ##      #####   #######   #####
  ##  ##   ##       ####    ##   ##   ##   #  ##   ##
 ##        ##      ##  ##   #         ## #    #
 ##        ##      ##  ##    #####    ####     #####
 ##        ##   #  ######        ##   ## #         ##
  ##  ##   ##  ##  ##  ##   ##   ##   ##   #  ##   ##
   ####   #######  ##  ##    #####   #######   #####
'''

class User:
    def __init__(self,username,mail,password,
                 object_id = None):
        
        self.username = username
        self.mail = mail
        self.password = password
        self.object_id = object_id

class Note:
    def __init__(self,name,description,
                 object_id = None):
        
        self.name = name
        self.description = description
        self.object_id = object_id

class Reminder:
    def __init__(self,name,
                 date = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm"),
                 object_id = None):
        
        self.name = name
        self.date = date
        self.object_id = object_id

class Birthday:
    def __init__(self,name,
                 date = QDate.currentDate().toString("MM-dd"),
                 object_id = None):
        
        self.name = name
        self.date = date
        self.object_id = object_id

class Accounting:
    def __init__(self,name,amount:float,
                 object_id = None):
        
        self.name = name
        self.amount = amount
        self.object_id = object_id

class AccountMove:
    def __init__(self,name,amount:float,
                 date = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm"),
                 object_id = None, account_id:int = None):

        self.account_id = account_id
        self.name = name
        self.amount = amount
        self.date = date 
        self.object_id = object_id

class Exercise:
    def __init__(self,name,description,
                 object_id = None):
        
        self.name = name
        self.description = description
        self.object_id = object_id

class Routine:
    def __init__(self,name,description,
                 object_id = None):
        
        self.name = name
        self.description = description
        self.object_id = object_id

class Food:
    def __init__(self,name,price:float,measure:int,
                 object_id = None):
        
        self.name = name
        self.price = price
        self.measure = measure
        self.object_id = object_id

class Diet:
    def __init__(self,name,price:float,
                 monday_list,tuesday_list,wednesday_list,
                 thursday_list,friday_list,saturday_list,sunday_list,
                 object_id = None):
        
        self.name = name
        self.price = price
        self.object_id = object_id

        self.monday_list = monday_list
        self.tuesday_list = tuesday_list
        self.wednesday_list = wednesday_list
        self.thursday_list = thursday_list
        self.friday_list = friday_list
        self.saturday_list = saturday_list
        self.sunday_list = sunday_list

'''
 ######     ##     ######   ####       ##      #####
 # ## #    ####     ##  ##   ##       ####    ##   ##
   ##     ##  ##    ##  ##   ##      ##  ##   #
   ##     ##  ##    #####    ##      ##  ##    #####
   ##     ######    ##  ##   ##   #  ######        ##
   ##     ##  ##    ##  ##   ##  ##  ##  ##   ##   ##
  ####    ##  ##   ######   #######  ##  ##    #####
'''

class DatabaseManager:
    def __init__(self, db_name="res/ddiario.db"):
        # Inicia la conexión con la base de datos y crea las tablas
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        # Inicia el cursor con la conexión a la db
        cursor = self.connection.cursor()
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                mail TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )''')

        # Tabla notas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )''')
        
        # Tabla recordatorios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )''')
        
        # Tabla cumpleaños
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS birthdays (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )''')

        # Tabla contabilidad
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accountings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                amount REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )''')
        
        # Tabla movimientos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (account_id) REFERENCES accountings(id) ON DELETE CASCADE
            )''')

        # Tabla alimentos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS foods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                measure INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )''')
        
        # Tabla dietas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                monday_list TEXT NOT NULL,
                tuesday_list TEXT NOT NULL,
                wednesday_list TEXT NOT NULL,
                thursday_list TEXT NOT NULL,
                friday_list TEXT NOT NULL,
                saturday_list TEXT NOT NULL,
                sunday_list TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )''')

        # Tabla ejercicios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )''')
        
        # Tabla rutinas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS routines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )''')
        
        # Commit
        self.connection.commit()
        cursor.close()
    
    '''
 ##   ##  #######  ######    #####   #####     #####    #####
 ### ###   ##   #  # ## #   ##   ##   ## ##   ##   ##  ##   ##
 #######   ## #      ##     ##   ##   ##  ##  ##   ##  #
 #######   ####      ##     ##   ##   ##  ##  ##   ##   #####
 ## # ##   ## #      ##     ##   ##   ##  ##  ##   ##       ##
 ##   ##   ##   #    ##     ##   ##   ## ##   ##   ##  ##   ##
 ##   ##  #######   ####     #####   #####     #####    #####
    '''

    def close(self):
        # Cierra conexión con la db
        self.connection.close()

    def delete_all(self):
        # Borra todos los datos de la db
        cursor = self.connection.cursor()
        cursor.execute('''DROP TABLE IF EXISTS birthdays''')
        cursor.execute('''DROP TABLE IF EXISTS reminders''')
        cursor.execute('''DROP TABLE IF EXISTS notes''')

        cursor.execute('''DROP TABLE IF EXISTS movements''')
        cursor.execute('''DROP TABLE IF EXISTS accountings''')

        cursor.execute('''DROP TABLE IF EXISTS diets''')
        cursor.execute('''DROP TABLE IF EXISTS foods''')

        cursor.execute('''DROP TABLE IF EXISTS routines''')
        cursor.execute('''DROP TABLE IF EXISTS exercises''')

        cursor.execute('''DROP TABLE IF EXISTS users''')
        self.connection.commit()
        cursor.close()

    '''
 ##   ##   #####   #######  ######
 ##   ##  ##   ##   ##   #   ##  ##
 ##   ##  #         ## #     ##  ##
 ##   ##   #####    ####     #####
 ##   ##       ##   ## #     ## ##
 ##   ##  ##   ##   ##   #   ##  ##
  #####    #####   #######  #### ##
    '''

    def add_user(self, user:User):
        # Coamndo SQL Insert into 
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO users (username, mail, password) 
            VALUES (?, ?, ?)
        ''', (user.username, user.mail, user.password))
        self.connection.commit()
        cursor.close()

    def get_all_users(self):
        # Comando Select * (all) 
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM users''')

        # Los convierte y los devuelve como una lista de usuarios
        rows = cursor.fetchall()
        cursor.close()

        return [User(row[1], row[2], row[3], row[0]) for row in rows]
    
    def update_user(self, user:User):
        # Ejecuta el comando SQL Update en el id solicitado
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE users
            SET username = ?, mail = ?, password = ?
            WHERE id = ?
        ''', (user.username, user.mail, user.password, user.object_id))
        self.connection.commit()
        cursor.close()

    def delete_user(self, object_id):
        # Ejecuta el comando SQL delete según el id dado
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM users WHERE id = ?''', (object_id,))
        self.connection.commit()
        cursor.close()

    def get_user_mail(self, mail):
        # Recorre la lista de usuarios en busqueda del mail
        for u in self.get_all_users():
            if u.mail == mail:
                return u
        
        # Si no lo encuentra devuelve None
        return None
    
    def get_user(self, id):
        # Recorre la lista de usuarios en busqueda del mail
        for u in self.get_all_users():
            if u.object_id == id:
                return u
        
        # Si no lo encuentra devuelve None
        return None

    '''
 ##   ##   #####   ######     ##      #####
 ###  ##  ##   ##  # ## #    ####    ##   ##
 #### ##  ##   ##    ##     ##  ##   #
 ## ####  ##   ##    ##     ##  ##    #####
 ##  ###  ##   ##    ##     ######        ##
 ##   ##  ##   ##    ##     ##  ##   ##   ##
 ##   ##   #####    ####    ##  ##    #####
    '''

    def add_note(self, user, note:Note):
        # Coamndo SQL Insert into
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO notes (user_id, name, description) 
            VALUES (?, ?, ?)
        ''', (user, note.name, note.description))
        self.connection.commit()
        cursor.close()

    def get_all_notes(self):
        # Comando Select * (all)
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM notes''')

        # Los convierte y los devuelve como una lista
        rows = cursor.fetchall()
        cursor.close()

        return [Note(row[2], row[3], row[0]) for row in rows]
    
    def update_note(self, note:Note):
        # Ejecuta el comando SQL Update en el id solicitado
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE notes
            SET name = ?, description = ?
            WHERE id = ?
        ''', (note.name, note.description, note.object_id))
        self.connection.commit()
        cursor.close()

    def delete_note(self, object_id:int):
        # Ejecuta el comando SQL delete según el id dado
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM notes WHERE id = ?''', (object_id,))
        self.connection.commit()
        cursor.close()
    
    def get_user_notes(self, user_id):
        # Select * (all) Where
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM notes WHERE user_id = ?''', (int(user_id),))

        # Convierte el resultado de la consulta en una lista y la devuelve
        rows = cursor.fetchall()
        cursor.close()

        return [Note(row[2], row[3], row[0]) for row in rows]

    '''
 ######   #######    ####    #####   ######   #####      ##     ######    #####   ######    ####     #####    #####
  ##  ##   ##   #   ##  ##  ##   ##   ##  ##   ## ##    ####    # ## #   ##   ##   ##  ##    ##     ##   ##  ##   ##
  ##  ##   ## #    ##       ##   ##   ##  ##   ##  ##  ##  ##     ##     ##   ##   ##  ##    ##     ##   ##  #
  #####    ####    ##       ##   ##   #####    ##  ##  ##  ##     ##     ##   ##   #####     ##     ##   ##   #####
  ## ##    ## #    ##       ##   ##   ## ##    ##  ##  ######     ##     ##   ##   ## ##     ##     ##   ##       ##
  ##  ##   ##   #   ##  ##  ##   ##   ##  ##   ## ##   ##  ##     ##     ##   ##   ##  ##    ##     ##   ##  ##   ##
 #### ##  #######    ####    #####   #### ##  #####    ##  ##    ####     #####   #### ##   ####     #####    #####
    '''

    def add_reminder(self, user, reminder:Reminder):
        # Coamndo SQL Insert into
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO reminders (user_id, name, date) 
            VALUES (?, ?, ?)
        ''', (user, reminder.name, reminder.date))
        self.connection.commit()
        cursor.close()

    def get_all_reminders(self):
        # Comando Select * (all)
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM reminders''')

        # Los convierte y los devuelve como una lista
        rows = cursor.fetchall()
        cursor.close()

        return [Reminder(row[2], row[3], row[0]) for row in rows]
    
    def update_reminder(self, reminder:Reminder):
        # Ejecuta el comando SQL Update en el id solicitado
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE reminders
            SET name = ?, date = ?
            WHERE id = ?
        ''', (reminder.name, reminder.date, reminder.object_id))
        self.connection.commit()
        cursor.close()

    def delete_reminder(self, object_id):
        # Ejecuta el comando SQL delete según el id dado
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM reminders WHERE id = ?''', (object_id,))
        self.connection.commit()
        cursor.close()
    
    def get_user_reminders(self, user_id):
        # Select * (all) Where
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM reminders WHERE user_id = ?''', (int(user_id),))

        # Convierte el resultado de la consulta en una lista y la devuelve
        rows = cursor.fetchall()
        cursor.close()

        return [Reminder(row[2], row[3], row[0]) for row in rows]

    '''
 ######    ####    ######   ######   ##   ##  #####      ##     ##  ##
  ##  ##    ##      ##  ##  # ## #   ##   ##   ## ##    ####    ##  ##
  ##  ##    ##      ##  ##    ##     ##   ##   ##  ##  ##  ##   ##  ##
  #####     ##      #####     ##     #######   ##  ##  ##  ##    ####
  ##  ##    ##      ## ##     ##     ##   ##   ##  ##  ######     ##
  ##  ##    ##      ##  ##    ##     ##   ##   ## ##   ##  ##     ##
 ######    ####    #### ##   ####    ##   ##  #####    ##  ##    ####
    '''

    def add_birthday(self, user, birthday:Birthday):
        # Coamndo SQL Insert into
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO birthdays (user_id, name, date) 
            VALUES (?, ?, ?)
        ''', (user, birthday.name, birthday.date))
        self.connection.commit()
        cursor.close()

    def get_all_birthdays(self):
        # Comando Select * (all)
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM birthdays''')

        # Los convierte y los devuelve como una lista
        rows = cursor.fetchall()
        cursor.close()

        return [Birthday(row[2], row[3], row[0]) for row in rows]
    
    def update_birthday(self, birthday:Birthday):
        # Ejecuta el comando SQL Update en el id solicitado
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE birthdays
            SET name = ?, date = ?
            WHERE id = ?
        ''', (birthday.name, birthday.date, birthday.object_id))
        self.connection.commit()
        cursor.close()

    def delete_birthday(self, object_id):
        # Ejecuta el comando SQL delete según el id dado
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM birthdays WHERE id = ?''', (object_id,))
        self.connection.commit()
        cursor.close()
    
    def get_user_birthdays(self, user_id):
        # Select * (all) Where
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM birthdays WHERE user_id = ?''', (int(user_id),))

        # Convierte el resultado de la consulta en una lista y la devuelve
        rows = cursor.fetchall()
        cursor.close()

        return [Birthday(row[2], row[3], row[0]) for row in rows]

    '''
   ####    #####   ##   ##  ######     ##     ######    ####    ####      ####    #####      ##     #####
  ##  ##  ##   ##  ###  ##  # ## #    ####     ##  ##    ##      ##        ##      ## ##    ####     ## ##
 ##       ##   ##  #### ##    ##     ##  ##    ##  ##    ##      ##        ##      ##  ##  ##  ##    ##  ##
 ##       ##   ##  ## ####    ##     ##  ##    #####     ##      ##        ##      ##  ##  ##  ##    ##  ##
 ##       ##   ##  ##  ###    ##     ######    ##  ##    ##      ##   #    ##      ##  ##  ######    ##  ##
  ##  ##  ##   ##  ##   ##    ##     ##  ##    ##  ##    ##      ##  ##    ##      ## ##   ##  ##    ## ##
   ####    #####   ##   ##   ####    ##  ##   ######    ####    #######   ####    #####    ##  ##   #####
    '''

    def add_accounting(self, user, accounting:Accounting):
        # Coamndo SQL Insert into
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO accountings (user_id, name, amount) 
            VALUES (?, ?, ?)
        ''', (user, accounting.name, accounting.amount))
        self.connection.commit()
        cursor.close()

    def get_all_accountings(self):
        # Comando Select * (all)
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM accountings''')

        # Los convierte y los devuelve como una lista
        rows = cursor.fetchall()
        cursor.close()

        return [Accounting(row[2], row[3], row[0]) for row in rows]
    
    def update_accounting(self, accounting:Accounting):
        # Ejecuta el comando SQL Update en el id solicitado
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE accountings
            SET name = ?, amount = ?
            WHERE id = ?
        ''', (accounting.name, accounting.amount, accounting.object_id))
        self.connection.commit()
        cursor.close()

    def delete_accounting(self, object_id):
        # Ejecuta el comando SQL delete según el id dado
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM accountings WHERE id = ?''', (object_id,))
        self.connection.commit()
        cursor.close()
    
    def get_user_accountings(self, user_id):
        # Select * (all) Where
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM accountings WHERE user_id = ?''', (int(user_id),))

        # Convierte el resultado de la consulta en una lista y la devuelve
        rows = cursor.fetchall()
        cursor.close()

        return [Accounting(row[2], row[3], row[0]) for row in rows]

    '''
 ##   ##   #####   ##   ##   ####    ##   ##   ####    #######  ##   ##  ######    #####    #####
 ### ###  ##   ##  ##   ##    ##     ### ###    ##      ##   #  ###  ##  # ## #   ##   ##  ##   ##
 #######  ##   ##   ## ##     ##     #######    ##      ## #    #### ##    ##     ##   ##  #
 #######  ##   ##   ## ##     ##     #######    ##      ####    ## ####    ##     ##   ##   #####
 ## # ##  ##   ##    ###      ##     ## # ##    ##      ## #    ##  ###    ##     ##   ##       ##
 ##   ##  ##   ##    ###      ##     ##   ##    ##      ##   #  ##   ##    ##     ##   ##  ##   ##
 ##   ##   #####      #      ####    ##   ##   ####    #######  ##   ##   ####     #####    #####
    '''

    def add_movement(self, account, movement:AccountMove):
        # Coamndo SQL Insert into
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO movements (account_id, name, amount, date) 
            VALUES (?, ?, ?, ?)
        ''', (account, movement.name, movement.amount, movement.date))
        self.connection.commit()
        cursor.close()

    def get_all_movements(self):
        # Comando Select * (all)
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM movements''')

        # Los convierte y los devuelve como una lista
        rows = cursor.fetchall()
        cursor.close()

        return [AccountMove(row[1], row[2], row[3], row[4], row[0]) for row in rows]
    
    def update_movement(self, movement:AccountMove):
        # Ejecuta el comando SQL Update en el id solicitado
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE movements
            SET account_id ?, name = ?, amount = ?, date ?
            WHERE id = ?
        ''', (movement.name, movement.amount, movement.object_id))
        self.connection.commit()
        cursor.close()

    def delete_movement(self, object_id):
        # Ejecuta el comando SQL delete según el id dado
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM movements WHERE id = ?''', (object_id,))
        self.connection.commit()
        cursor.close()
    
    def get_account_movements(self, account_id):
        # Select * (all) Where
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM movements WHERE account_id = ?''', (int(account_id),))

        # Convierte el resultado de la consulta en una lista y la devuelve
        rows = cursor.fetchall()
        cursor.close()

        return [AccountMove(row[1], row[2], row[3], row[4], row[0]) for row in rows]

    '''
   ##     ####      ####    ##   ##  #######  ##   ##  ######    #####    #####
  ####     ##        ##     ### ###   ##   #  ###  ##  # ## #   ##   ##  ##   ##
 ##  ##    ##        ##     #######   ## #    #### ##    ##     ##   ##  #
 ##  ##    ##        ##     #######   ####    ## ####    ##     ##   ##   #####
 ######    ##   #    ##     ## # ##   ## #    ##  ###    ##     ##   ##       ##
 ##  ##    ##  ##    ##     ##   ##   ##   #  ##   ##    ##     ##   ##  ##   ##
 ##  ##   #######   ####    ##   ##  #######  ##   ##   ####     #####    #####
    '''

    def add_food(self, user, food:Food):
        # Coamndo SQL Insert into
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO foods (user_id, name, price, measure) 
            VALUES (?, ?, ?, ?)
        ''', (user, food.name, food.price, food.measure))
        self.connection.commit()
        cursor.close()

    def get_all_foods(self):
        # Comando Select * (all)
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM foods''')

        # Los convierte y los devuelve como una lista
        rows = cursor.fetchall()
        cursor.close()

        return [Food(row[2], row[3], row[4], row[0]) for row in rows]
    
    def update_food(self, food:Food):
        # Ejecuta el comando SQL Update en el id solicitado
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE foods
            SET name = ?, price = ?, measure = ?
            WHERE id = ?
        ''', (food.name, food.price, food.measure, food.object_id))
        self.connection.commit()
        cursor.close()

    def delete_food(self, object_id):
        # Ejecuta el comando SQL delete según el id dado
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM foods WHERE id = ?''', (object_id,))
        self.connection.commit()
        cursor.close()

    def get_user_foods(self, user_id):
        # Select * (all) Where
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM foods WHERE user_id = ?''', (int(user_id),))

        # Convierte el resultado de la consulta en una lista y la devuelve
        rows = cursor.fetchall()
        return [Food(row[2], row[3], row[4], row[0]) for row in rows]
    
    '''
 #####     ####    #######  ######     ##      #####
  ## ##     ##      ##   #  # ## #    ####    ##   ##
  ##  ##    ##      ## #      ##     ##  ##   #
  ##  ##    ##      ####      ##     ##  ##    #####
  ##  ##    ##      ## #      ##     ######        ##
  ## ##     ##      ##   #    ##     ##  ##   ##   ##
 #####     ####    #######   ####    ##  ##    #####
    '''

    def add_diet(self, user, diet:Diet):
        # Coamndo SQL Insert into
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO diets (user_id, name, price, monday_list, tuesday_list, wednesday_list, thursday_list, friday_list, saturday_list, sunday_list) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user, diet.name, diet.price, diet.monday_list, diet.tuesday_list, diet.wednesday_list, diet.thursday_list, diet.friday_list, diet.saturday_list, diet.sunday_list))
        self.connection.commit()
        cursor.close()

    def get_all_diets(self):
        # Comando Select * (all)
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM diets''')

        # Los convierte y los devuelve como una lista
        rows = cursor.fetchall()
        cursor.close()

        return [Diet(row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[0]) for row in rows]
    
    def update_diet(self, diet:Diet):
        # Ejecuta el comando SQL Update en el id solicitado
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE diets
            SET name = ?, price = ?, monday_list = ?, tuesday_list = ?, wednesday_list = ?, thursday_list = ?, friday_list = ?, saturday_list = ?, sunday_list = ?
            WHERE id = ?
        ''', (diet.name, diet.price, diet.monday_list, diet.tuesday_list, diet.wednesday_list, diet.thursday_list, diet.friday_list, diet.saturday_list, diet.sunday_list))
        self.connection.commit()
        cursor.close()

    def delete_diet(self, object_id):
        # Ejecuta el comando SQL delete según el id dado
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM diets WHERE id = ?''', (object_id,))
        self.connection.commit()
        cursor.close()

    def get_user_diets(self, user_id):
        # Select * (all) Where
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM diets WHERE user_id = ?''', (int(user_id),))

        # Convierte el resultado de la consulta en una lista y la devuelve
        rows = cursor.fetchall()
        return [Diet(row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[0]) for row in rows]

    '''
 #######     ####  #######  ######     ####    ####      ####    ####     #####    #####
  ##   #      ##    ##   #   ##  ##   ##  ##    ##      ##  ##    ##     ##   ##  ##   ##
  ## #        ##    ## #     ##  ##  ##         ##     ##         ##     ##   ##  #
  ####        ##    ####     #####   ##         ##     ##         ##     ##   ##   #####
  ## #    ##  ##    ## #     ## ##   ##         ##     ##         ##     ##   ##       ##
  ##   #  ##  ##    ##   #   ##  ##   ##  ##    ##      ##  ##    ##     ##   ##  ##   ##
 #######   ####    #######  #### ##    ####    ####      ####    ####     #####    #####
    '''

    def add_exercise(self, user, exercise:Exercise):
        # Coamndo SQL Insert into
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO exercises (user_id, name, description) 
            VALUES (?, ?, ?)
        ''', (user, exercise.name, exercise.description))
        self.connection.commit()
        cursor.close()

    def get_all_exercises(self):
        # Comando Select * (all)
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM exercises''')

        # Los convierte y los devuelve como una lista
        rows = cursor.fetchall()
        cursor.close()

        return [Exercise(row[2], row[3], row[0]) for row in rows]
    
    def update_exercise(self, exercise:Exercise):
        # Ejecuta el comando SQL Update en el id solicitado
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE exercises
            SET name = ?, description = ?
            WHERE id = ?
        ''', (exercise.name, exercise.description, exercise.object_id))
        self.connection.commit()
        cursor.close()

    def delete_exercise(self, object_id):
        # Ejecuta el comando SQL delete según el id dado
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM exercises WHERE id = ?''', (object_id))
        self.connection.commit()
        cursor.close()
    
    def get_user_exercises(self, user_id):
        # Select * (all) Where
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM exercises WHERE user_id = ?''', (int(user_id),))

        # Convierte el resultado de la consulta en una lista y la devuelve
        rows = cursor.fetchall()
        return [Exercise(row[2], row[3], row[0]) for row in rows]

    '''
 ######   ##   ##  ######    ####    ##   ##    ##      #####
  ##  ##  ##   ##  # ## #     ##     ###  ##   ####    ##   ##
  ##  ##  ##   ##    ##       ##     #### ##  ##  ##   #
  #####   ##   ##    ##       ##     ## ####  ##  ##    #####
  ## ##   ##   ##    ##       ##     ##  ###  ######        ##
  ##  ##  ##   ##    ##       ##     ##   ##  ##  ##   ##   ##
 #### ##   #####    ####     ####    ##   ##  ##  ##    #####
    '''

    def add_routine(self, user, routine:Routine):
        # Coamndo SQL Insert into
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO routines (user_id, name, description) 
            VALUES (?, ?, ?)
        ''', (user, routine.name, routine.description))
        self.connection.commit()
        cursor.close()

    def get_all_routines(self):
        # Comando Select * (all)
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM routines''')

        # Los convierte y los devuelve como una lista
        rows = cursor.fetchall()
        cursor.close()

        return [Routine(row[2], row[3], row[0]) for row in rows]
    
    def update_routine(self, routine:Routine):
        # Ejecuta el comando SQL Update en el id solicitado
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE routines
            SET name = ?, description = ?
            WHERE id = ?
        ''', (routine.name, routine.description, routine.object_id))
        self.connection.commit()
        cursor.close()

    def delete_routine(self, object_id):
        # Ejecuta el comando SQL delete según el id dado
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM routines WHERE id = ?''', (object_id))
        self.connection.commit()
        cursor.close()
    
    def get_user_routines(self, user_id):
        # Select * (all) Where
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM routines WHERE user_id = ?''', (int(user_id),))

        # Convierte el resultado de la consulta en una lista y la devuelve
        rows = cursor.fetchall()
        return [Routine(row[2], row[3], row[0]) for row in rows]

'''
 #####    #######  ######   ##   ##    ####
  ## ##    ##   #   ##  ##  ##   ##   ##  ##
  ##  ##   ## #     ##  ##  ##   ##  ##
  ##  ##   ####     #####   ##   ##  ##
  ##  ##   ## #     ##  ##  ##   ##  ##  ###
  ## ##    ##   #   ##  ##  ##   ##   ##  ##
 #####    #######  ######    #####     #####
'''

# DEBUG, Inicia la db y permite realizar acciones aisladas tales como añadir o eliminar datos de prueba
if __name__ == "__main__":
    db = DatabaseManager()

    def test_data():
        def test_users():
            db.add_user(User("Alumno","a@gmail.com","a"))
            db.add_user(User("Eloy","eloy@gmail.com","eloy"))
            db.add_user(User("Vacio","vacio@gmail.com","vacio"))
        test_users()

        def test_notes():
            db.add_note(1,Note("Comprar","Comprar bateria portatil"))
            db.add_note(1,Note("Terminar TFG :(","Añadir bibliografia"))
            db.add_note(2,Note("Ejemplo","Descripción"))
        test_notes()

        def test_reminders():
            db.add_reminder(1,Reminder("Cine","2025-04-02 20:15"))
            db.add_reminder(1,Reminder("Clases de piano","2025-04-04 18:00"))
            db.add_reminder(1,Reminder("Desayuno","2025-04-11 08:30"))
        test_reminders()

        def test_birthdays():
            db.add_birthday(1,Birthday("Cumapleaños Carla","2025-03-08"))
            db.add_birthday(1,Birthday("Cumapleaños Daniel","2025-09-11"))
            db.add_birthday(1,Birthday("Cumapleaños Ruben","2025-02-23"))
        test_birthdays()

        def test_accountings():
            db.add_accounting(1,Accounting("Contabilidad Marzo",0.0))
            db.add_accounting(1,Accounting("Contabilidad Febrero",120.25))
            db.add_accounting(1,Accounting("Fiesta de navidad",-25.0))
        test_accountings()

        def test_movements():
            db.add_movement(1,AccountMove(2,"Compra Alcampo",-145.23,"2025-02-08"))
            db.add_movement(1,AccountMove(2,"Visita al museo",-4.15,"2025-02-16"))
            db.add_movement(1,AccountMove(2,"Gasolina",-85.67,"2025-02-19"))
        test_movements()


        def test_foods():
            db.add_food(1,Food("Arroz",1.30,2))
            db.add_food(1,Food("Agua",0.85,1))
            db.add_food(1,Food("Pollo",5.60,0))
        test_foods()

        def test_diets():
            db.add_diet(1,Diet(
                "Dieta semanal",
                245.78,
                "Crema de calabaza y manzana | Muslos de pollo al horno | Tosta de revuelto de champiñones",
                "Lentejas vegetales | Merluza en salsa verde | Coca de verduras",
                "Macarrones integrales con verduras | Pollo a la cerveza | Tacos de verduras asadas y aguacate",
                "Sopa juliana |Corvina al horno | Huevo frito | Ensalada de tomate",
                "Crema de puerros | Guiso de conejo | Poke de salmón",
                "Calabacines rellenos | Guisantes con jamón",
                "Paella de verduras | Guacamole y nachos integrales"))
        test_diets()

        def test_exercises():
            db.add_exercise(1,Exercise("Bici","30 minutos - 10km"))
            db.add_exercise(1,Exercise("Pesa rusa","5 repeticiones x 15 levantamientos"))
            db.add_exercise(1,Exercise("Sentadillas","10 repeticiones x 10 sentadillas"))
        test_exercises()

        def test_routines():
            db.add_routine(1,Routine("Verano","Bici, Psea rusa"))
            db.add_routine(1,Routine("Zaragoza","Sentadillas, Pesa rusa"))
            db.add_routine(1,Routine("Findes","Bici, Sentadillas"))
        test_routines()

    def dispaly_all():
        def test_users():
            data:list = db.get_all_users()
            for u in data:
                u:User
                print (f'{u.object_id} - {u.username} - {u.mail} - {u.password}')
            print ("\n\n\n")
        test_users()

        def test_notes():
            data:list = db.get_all_notes()
            for u in data:
                u:Note
                print (f'{u.object_id} - {u.name} - {u.description}')
            print ("\n\n\n")
        test_notes()

        def test_reminders():
            data:list = db.get_all_reminders()
            for u in data:
                u:Reminder
                print (f'{u.object_id} - {u.name} - {u.date}')
            print ("\n\n\n")
        test_reminders()

        def test_birthdays():
            data:list = db.get_all_birthdays()
            for u in data:
                u:Birthday
                print (f'{u.object_id} - {u.name} - {u.date}')
            print ("\n\n\n")
        test_birthdays()

        def test_accountings():
            data:list = db.get_all_accountings()
            for u in data:
                u:Accounting
                print (f'{u.object_id} - {u.name} - {u.amount}')
            print ("\n\n\n")
        test_accountings()

        def test_movements():
            data:list = db.get_all_movements()
            for u in data:
                u:AccountMove
                print (f'{u.object_id} - {u.name} - {u.amount} - {u.date}')
            print ("\n\n\n")
        test_movements()

        def test_foods():
            data:list = db.get_all_foods()
            for u in data:
                u:Food
                print (f'{u.object_id} - {u.name} - {u.price} - {u.measure}')
            print ("\n\n\n")
        test_foods()

        def test_diets():
            data:list = db.get_all_diets()
            for u in data:
                u:Diet
                print (f'{u.object_id} - {u.name} - {u.price} - {u.monday_list} - {u.tuesday_list} - {u.wednesday_list} - {u.thursday_list} - {u.friday_list} - {u.saturday_list} - {u.sunday_list}')
            print ("\n\n\n")
        test_diets()

        def test_exercises():
            data:list = db.get_all_exercises()
            for u in data:
                u:Exercise
                print (f'{u.object_id} - {u.name} - {u.description}')
            print ("\n\n\n")
        test_exercises()

        def test_routines():
            data:list = db.get_all_routines()
            for u in data:
                u:Routine
                print (f'{u.object_id} - {u.name} - {u.description}')
            print ("\n\n\n")
        test_routines()

    db.close()