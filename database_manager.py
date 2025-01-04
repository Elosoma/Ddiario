import sqlite3



class Routine:
    def __init__(self,
                 user_id,
                 name,
                 description,
                 date,
                 is_recurring,
                 routine_id=None):
        '''Clase modelo para la creación de objetos rutina'''

        self.id = routine_id
        self.user = user_id
        self.name = name
        self.description = description
        self.date = date
        self.is_recurring = is_recurring

class User:
    def __init__(self,
                 username,
                 mail,
                 password,
                 user_id = None):
        '''Clase modelo para la creación de objetos usuario'''

        self.id = user_id
        self.username = username
        self.mail = mail
        self.password = password



class DatabaseManager:
    def __init__(self, db_name="res/ddiario.db"):
        '''Inicia la conexión con la base de datos y crea las tablas'''
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        '''Crea las tablas de la db si estas no existen'''

        # Inicia el cursor con la conexión a la db
        cursor = self.connection.cursor()
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                mail TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        # Tabla de rutinas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS routines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                is_recurring BOOLEAN NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')


        # Commit
        self.connection.commit()

    '''
    -------------------
    
    Metodos de rutinas
    
    -------------------
    '''

    def add_routine(self, routine=Routine):
        '''Añade una rutina a la db'''

        # Inicia el cursor con la conexión a la db
        cursor = self.connection.cursor()
        # Ejecuta el comando sql de insercción de datos en rutinas
        cursor.execute('''
            INSERT INTO routines (user_id, name, description, date, is_recurring) 
            VALUES (?, ?, ?, ?, ?)
        ''', (routine.user, routine.name, routine.description, routine.date, routine.is_recurring))
    
        # Commit
        self.connection.commit()

    def get_all_routines(self):
        '''Obtiene una lista con todas las rutinas de la db'''

        # Inicia el cursor con la conexión a la db
        cursor = self.connection.cursor()
        # Select * (all) de rutinas
        cursor.execute('''SELECT * FROM routines''')

        # Convierte el resultado de la consulta en una lista y la devuelve
        rows = cursor.fetchall()
        return [Routine(row[1], row[2], row[3], row[4], bool(row[5]), row[0]) for row in rows]

    def get_user_routines(self, user_id):
        '''Obtiene una lista con todas las rutinas del usuario de la db indicado'''

        # Inicia el cursor con la conexión a la db
        cursor = self.connection.cursor()
        # Select * (all) de rutinas
        cursor.execute('''SELECT * FROM routines WHERE user_id = ?''', (user_id))

        # Convierte el resultado de la consulta en una lista y la devuelve
        rows = cursor.fetchall()
        return [Routine(row[1], row[2], row[3], row[4], bool(row[5]), row[0]) for row in rows]

    def delete_routine(self, routine_id):
        '''Borra una rutina mediante su id'''

        # Inicia el cursor con la conexión a la db
        cursor = self.connection.cursor()
        # Comando SQL para borrar por id
        cursor.execute('''DELETE FROM routines WHERE id = ?''', (routine_id,))

        # Commit
        self.connection.commit()

    def update_routine(self, routine=Routine):
        '''Actualiza los datos de una rutina ya existente'''

        # Inicia el cursor con la conexión a la db
        cursor = self.connection.cursor()
        # Comando SQL Update con los datos nuevos pasados como parametro
        cursor.execute('''
            UPDATE routines
            SET name = ?, description = ?, date = ?, is_recurring = ?
            WHERE id = ?
        ''', (routine.name, routine.description, routine.date, routine.is_recurring, routine.id))

        # Commit
        self.connection.commit()

    '''
    -------------------
    
    Metodos de usuarios
    
    -------------------
    '''

    def add_user(self, user=User):
        '''Registra un usuario en la db'''

        # Inicia el cursor con la conexión a la db
        cursor = self.connection.cursor()
        # Coamndo SQL Insert into Users
        cursor.execute('''
            INSERT INTO users (username, mail, password) 
            VALUES (?, ?, ?)
        ''', (user.username, user.mail, user.password))

        # Commit
        self.connection.commit()

    def get_all_users(self):
        '''Devuelve una lista con todos los usuarios de la db'''

        # Inicia el cursor con la conexión a la db
        cursor = self.connection.cursor()
        # Comando Select * (all) usuarios
        cursor.execute('''SELECT * FROM users''')

        # Los convierte y los devuelve como una lista de usuarios
        rows = cursor.fetchall()
        return [User(row[1], row[2], row[3], row[0]) for row in rows]
    
    def get_user(self, user_mail):
        '''Devuelve los datos del usuario solicitado por mail'''

        # Recorre la lista de usuarios en busqueda del mail
        for u in self.get_all_users():
            if u.mail == user_mail:
                return u
        
        # Si no lo encuentra devuelve None
        return None

    def delete_user(self, user_id):
        '''Borra el usuario por su id'''

        # Inicia el cursor con la conexión a la db
        cursor = self.connection.cursor()
        # Ejecuta el comando SQL delete según el id dado
        cursor.execute('''DELETE FROM users WHERE id = ?''', (user_id,))

        # Commit
        self.connection.commit()

    def update_user(self, user=User):
        '''Actualiza los datos del usuario dado'''

        # Inicia el cursor con la conexión a la db
        cursor = self.connection.cursor()
        # Ejecuta el comando SQL Update en el usuario solicitado
        cursor.execute('''
            UPDATE users
            SET username = ?, mail = ?, password = ?
            WHERE id = ?
        ''', (user.username, user.mail, user.password, user.id))

        # Commit
        self.connection.commit()

    '''
    -------------------
    
    Otros metodos
    
    -------------------
    '''

    def close(self):
        '''Cierra conexión con la db'''
        self.connection.close()





# DEBUG, Inicia la db y permite realizar acciones aisladas tales como añadir o eliminar datos de prueba
if __name__ == "__main__":
    db = DatabaseManager()

    '''user = User("healtyrunner","sportman@gmail.com","runsofaraway")
    db.add_user(user)
    user = User("businessman","criptofounder@hotmail.io","memillonaire")
    db.add_user(user)
    user = User("alumno","alumno@gmail.com","alumno")
    db.add_user(user)

    routine = Routine(1,"TFG","Defender el proyecto de fin de grado","2025-01-15 14:00",False)
    db.add_routine(routine)
    routine = Routine(1,"Clase de piano","","Lunes-Martes 17:30-19:00",True)
    db.add_routine(routine)
    routine = Routine(2,"Salir a correr","Recorrer las afueras del poligono","2025-01-17 08:15-10:30",False)
    db.add_routine(routine)'''
    
    users = db.get_all_users()
    routines = db.get_all_routines()
    for u in users:
        print (f'{u.id} - {u.mail} - {u.username} - {u.password}')
        for r in routines:
            if r.user == u.id:
                print (f'{r.id} - {r.name} - {r.description} - {r.date} - {r.is_recurring}')

        print ("\n\n\n")

    db.close()
