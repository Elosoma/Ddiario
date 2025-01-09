import json, sys, re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QStackedLayout, QPushButton, QLabel, QLineEdit, QFormLayout, QHBoxLayout, QListWidget, QMessageBox, QComboBox, QDateEdit, QTimeEdit
)
from PyQt5.QtCore import Qt, QTime, QDate
from PyQt5.QtGui import QPixmap, QIcon
from datetime import datetime, date
from database_manager import DatabaseManager, Routine



class WelcomeScreen(QWidget):
    def __init__(self, switch_screen):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(self.wellcome())

        button = QPushButton("Ir al inicio de sesión")
        button.clicked.connect(lambda: switch_screen(1))
        layout.addWidget(button)

    def wellcome(self):
        '''Centra la imagen'''
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        img = QLabel()
        img.setPixmap(QPixmap("res\\frame_wellcome.png"))
        layout.addWidget(img)
        return widget

'''
------------------------------------------------------------------------------------------
'''

class LoginScreen(QWidget):
    def __init__(self, switch_screen, db, set_current_user):
        super().__init__()
        # Variables
        self.db = db
        self.switch_screen = switch_screen
        self.set_current_user = set_current_user
    
        layout = QFormLayout(self)
        # Formulario de email y de contrasseña censurada
        self.mail_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        # Añade las filas con los nombres de los campos
        layout.addRow("Correo: ", self.mail_input)
        layout.addRow("Contraseña: ", self.password_input)

        # Botón de inicio de sesión (Comprueba los datos)
        login_button = QPushButton("Iniciar sesión")
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)

        # Botón registro de usuario (Cambia de pestaña)
        register_button = QPushButton("Registrar usuario")
        register_button.clicked.connect(lambda: switch_screen(2))
        layout.addWidget(register_button)    

    def handle_login(self):
        '''Gestiona el inicio de sesión y comprueba los datos con la db'''

        # Extrae los datos del formulario
        mail = self.mail_input.text()
        password = self.password_input.text()

        # Comprueba los diferentes datos
        if is_mail(mail):
            user = self.db.get_user(mail)
            if user:
                if user.password == password:
                    # Cambiamos el usuario actual y redirige a las pestaña principal
                    self.set_current_user(user)
                    self.switch_screen(3)
                else:
                    QMessageBox.warning(self, "Datos Incorrectos", "Revise que los datos introducidos sean correctos.")
            else:
                QMessageBox.warning(self, "Datos Incorrectos", "Correo no vinculado a una cuenta existente.")
        else:
            QMessageBox.warning(self, "Datos Incorrectos", "Campo correo inválido.")

'''
------------------------------------------------------------------------------------------
'''

class RegisterScreen(QWidget):
    def __init__(self, switch_screen, db, set_current_user):
        super().__init__()
        # Variables
        self.db = db
        self.switch_screen = switch_screen
        self.set_current_user = set_current_user

        layout = QFormLayout(self)
        # Elementos del formulario
        self.mail_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        # Añade las filas con los nombres de los campos
        layout.addRow("Correo:", self.mail_input)
        layout.addRow("Usuario:", self.username_input)
        layout.addRow("Contraseña:", self.password_input)
        layout.addRow("Confirmar Contraseña:", self.confirm_password_input)

        # Botón de registro
        register_button = QPushButton("Registrar")
        register_button.clicked.connect(self.handle_register)
        layout.addWidget(register_button)

    def handle_register(self):
        '''Gestiona la creación de nuevos usuarios'''

        # Extrae los datos del formulario
        mail = self.mail_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        # Comprueba que los campos tengan contenido
        if not mail or not username or not password or not confirm_password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return

        # Comprueba que sea un mail válido
        if not is_mail(mail):
            QMessageBox.warning(self, "Datos Incorrectos", "Campo correo inválido.")
            return

        # Comprueba que el mail introducido no este ya registrado
        if self.db.get_user(mail):
            QMessageBox.warning(self, "Error", "El siguiente correo ya se encuentra registrado")
            return

        # Comprueba que la contraseña y su confirmación sean iguales
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
            return

        try:
            # Intenta crear el usuario y redirige a la pestaña principal
            self.db.add_user(username, mail, password)
            QMessageBox.information(self, "Éxito", "Usuario registrado correctamente")
            user = self.db.get_user(mail)
            self.set_current_user(user)
            self.switch_screen(3)
        except Exception as e:
            # Error no esperado de la db
            QMessageBox.warning(self, "Error", str(e))
            return

'''
------------------------------------------------------------------------------------------
'''

class MainScreen(QWidget):
    def __init__(self, switch_screen, db, get_current_user):
        super().__init__()
        # Variables
        self.db = db
        self.switch_screen = switch_screen
        self.get_current_user = get_current_user
        
        # Layout
        self.layout = QVBoxLayout(self)

        # Mensaje de bienvenida con el username
        self.wellcoming = QLabel('Bienvenido/a user')
        self.wellcoming.setStyleSheet("font-size: 20px;")
        self.wellcoming.setWordWrap(True)
        self.layout.addWidget(self.wellcoming)

        # Label informativo
        self.label = QLabel("Rutinas próximas:")
        self.layout.addWidget(self.label)

        # Lista con las rutinas del usuario
        self.routine_list = QListWidget()
        self.layout.addWidget(self.routine_list)
        self.update_routines()

        # Menú de navegación
        self.layout.addWidget(self.nav_menu())

    def nav_menu(self):
        '''Elementos de navegación'''
        # Estructura layout
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # Botón añadir rutina
        add_btn = QPushButton()
        add_btn.setIcon(QIcon("res\\icon_0.png"))
        add_btn.clicked.connect(lambda: self.switch_screen(4))
        layout.addWidget(add_btn)

        # Botón listado de rutinas
        list_btn = QPushButton()
        list_btn.setIcon(QIcon("res\\icon_1.png"))
        list_btn.clicked.connect(lambda: self.switch_screen(5))
        layout.addWidget(list_btn)

        # Botón perfil de usuario
        porfile_btn = QPushButton()
        porfile_btn.setIcon(QIcon("res\\icon_2.png"))
        porfile_btn.clicked.connect(lambda: self.switch_screen(6))
        layout.addWidget(porfile_btn)
        return widget

    

    def update_routines(self):
        '''Actualiza las rutinas y otras variables que dependen del usuario activo'''

        # Limpia la lista y actualiza el mensaje de bienvenida
        self.routine_list.clear()
        self.current_user = self.get_current_user()
        self.wellcoming.setText(f'Bienvenido/a {self.current_user["username"]}')

        # Añade las rutinas del usuario activo
        routines = self.db.get_user_routines(int(self.current_user['id'])) if self.current_user['id'] else []

        # Ordenar rutinas por proximidad a la fecha actual
        today = datetime.now()
        routines.sort(key=lambda r: abs((r.date - today).days))

        for routine in routines:
            lbl = QLabel()
            lbl.setStyleSheet("border: 2px solid #190f2a; background-color: white;")
            self.routine_list.addItem(f"{routine.name}\n{routine.date}\n{routine.description}\n")


'''
------------------------------------------------------------------------------------------
'''

class CreateRoutineScreen(QWidget):
    def __init__(self, switch_screen, db, get_current_user):
        super().__init__()
        # Variables
        self.db = db
        self.get_current_user = get_current_user
        self.switch_screen = switch_screen

        self.layout = QFormLayout(self)
        # Elementos del formulario
        self.name_input = QLineEdit()
        self.description_input = QLineEdit()
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setMinimumDate(QDate.currentDate())
        self.time_input = QTimeEdit()
        self.recurring_selector = QComboBox()
        self.recurring_selector.addItems(["Única vez", "Diaria", "Semanal", "Mensual"])

        # Filas con los nombres de los campos
        self.layout.addRow("Nombre:", self.name_input)
        self.layout.addRow("Descripción:", self.description_input)
        self.layout.addRow("Fecha:", self.date_input)
        self.layout.addRow("Hora:", self.time_input)
        self.layout.addRow("Repetir:", self.recurring_selector)

        # Botón para guardar rutina
        save_button = QPushButton("Volver")
        save_button.clicked.connect(lambda : self.switch_screen(3))
        self.layout.addWidget(save_button)

        # Botón para guardar rutina
        save_button = QPushButton("Guardar rutina")
        save_button.clicked.connect(self.handle_save)
        self.layout.addWidget(save_button)
    
    def update(self):
        '''Actualiza los campos cada vez que se accede a la pestaña'''
        self.name_input.setText("")
        self.description_input.setText("")
        self.date_input.setDate(QDate.currentDate())
        self.time_input.setTime(QTime.currentTime())
        self.recurring_selector.setCurrentIndex(0)

    def handle_save(self):
        '''Gestiona la creación de rutinas'''

        name = self.name_input.text()
        description = self.description_input.text()
        date = self.date_input.date().toPyDate()
        time = self.time_input.time().toPyTime()
        date_time = datetime.combine(date, time)
        formatted_date = date_time.strftime("%Y-%m-%d %H:%M")  # Sin microsegundos
        is_recurring = self.recurring_selector.currentIndex() > 0

        # Comprueba los campos obligatorios
        if not name:
            QMessageBox.warning(self, "Error", "El nombre es un campo obligatorio")
            return
        if not date or not time:
            QMessageBox.warning(self, "Error", "La fecha es un campo obligatorio")
            return
        
        # Comprueba que la feha no sea pasada:
        current_date = datetime.now()
        if date_time <= current_date:
            QMessageBox.warning(self, "Fecha/Hora Inválida", "Selecciona una fecha y hora futuras.")
            return

        # Comprueba que exista una sesión
        current_user = self.get_current_user()
        if not current_user:
            QMessageBox.warning(self, "Error", "No hay usuario autenticado")
            return

        # Crea la rutina y la añade al usuario con la sesión actual
        print (f"{current_user['id']}, {name}, {description}, {formatted_date}, {is_recurring}")
        routine = Routine(current_user['id'], name, description, formatted_date, is_recurring)
        self.db.add_routine(routine)

        # Informa y regresa a la pestaña principal
        QMessageBox.information(self, "Éxito", "Rutina guardada correctamente")
        self.switch_screen(3)

'''
------------------------------------------------------------------------------------------
'''

class EditRoutineScreen(QWidget):
    def __init__(self, switch_screen, db, get_current_user):
        super().__init__()
        self.db = db
        self.get_current_user = get_current_user
        self.switch_screen = switch_screen

        self.layout = QVBoxLayout()

        self.label = QLabel("Lista de rutinas")
        self.layout.addWidget(self.label)

        self.routine_list = QListWidget()
        self.layout.addWidget(self.routine_list)

        self.update_routines()

        delete_button = QPushButton("Eliminar rutina")
        delete_button.clicked.connect(self.delete_routine)
        self.layout.addWidget(delete_button)

        back_button = QPushButton("Volver")
        back_button.clicked.connect(lambda: switch_screen(3))
        self.layout.addWidget(back_button)

        self.setLayout(self.layout)

    def update_routines(self):
        self.routine_list.clear()
        current_user = self.get_current_user()
        routines = self.db.get_user_routines(current_user['id']) if current_user['id'] else []
        for routine in routines:
            self.routine_list.addItem(f"{routine.name} - {routine.date}")

    def delete_routine(self):
        selected_item = self.routine_list.currentItem()
        if selected_item:
            routine_name = selected_item.text().split(" - ")[0]
            current_user = self.get_current_user()
            routines = self.db.get_user_routines(current_user['id']) if current_user['id'] else []
            for routine in routines:
                if routine.name == routine_name:
                    self.db.delete_routine(routine.id)
                    QMessageBox.information(self, "Éxito", "Rutina eliminada correctamente")
                    self.update_routines()
                    return

'''
------------------------------------------------------------------------------------------
'''

class PorfileScreen (QWidget):
    def __init__(self, switch_screen, db, get_current_user, set_current_user):
        super().__init__()
        # Variables
        self.db = db
        self.switch_screen = switch_screen
        self.get_current_user = get_current_user
        self.set_current_user = set_current_user

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.porfile_icon())
        layout.addWidget(self.user_info())
        layout.addStretch()

        # Botón volver
        btn_back = QPushButton('Volver')
        btn_back.clicked.connect(lambda: switch_screen(3))
        layout.addWidget(btn_back)

        # Botón cerrar sesión
        btn_log_out = QPushButton("Cerrar sesión")
        btn_log_out.clicked.connect(self.handle_log_out)
        layout.addWidget(btn_log_out)
    
    def update_info(self):
        '''Actualiza la información con la del usuario activo'''
        current_user = self.get_current_user()
        routines = self.db.get_user_routines(current_user['id']) if current_user['id'] else []
        self.lbl_info.setText(f"Usuario: {current_user['username']}\n\nNº de rutinas: {len(routines)}")

    def user_info(self):
        '''Centra la imagen y la re escala'''
        widget = QWidget()
        widget.setContentsMargins(0,0,0,0)
        layout = QHBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        self.lbl_info = QLabel('username')
        layout.addWidget(self.lbl_info)
        return widget

    def porfile_icon(self):
        '''Centra la imagen y la re escala'''
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        lbl_img = QLabel()
        lbl_img.resize(128,128)

        # Re-escalar la imagen
        pixmap = QPixmap('res\\icon_2.png')
        scaled_pixmap = pixmap.scaled(lbl_img.size())

        lbl_img.setPixmap(scaled_pixmap)
        layout.addWidget(lbl_img)
        return widget

    def handle_log_out(self):
        '''Borra la sesión y regresa al inicio'''
        with open("user.json", "w", encoding='utf-8') as file:
            file.write(f'{json.dumps({"id": "None", "username": "None"})}')
        self.switch_screen(0)    

'''
------------------------------------------------------------------------------------------
'''

def is_mail(mail):
    """Comprueba si el texto dado tiene el formato de un correo electrónico válido."""
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, mail) is not None

def run():
    '''Inicia el programa'''

    # Variables
    app = QApplication(sys.argv)
    db = DatabaseManager()

    with open("user.json", "r", encoding='utf-8') as file:
        user = json.load(file)
    current_user = {
        'id': None if user["id"] == 'None' else user["id"],
        'username': None if user["username"] == 'None' else user["username"]
    }

    def get_current_user():
        '''Devuelve la variable del usuario actual'''
        return current_user

    def set_current_user(user):
        '''Cambia el usuario actual'''
        current_user['id'] = user.id
        current_user['username'] = user.username
        with open("user.json", "w", encoding='utf-8') as file:
            file.write(f'{json.dumps(current_user)}')

    # Widget principal y sus propiedades
    main_window = QWidget()
    main_window.setWindowTitle('Ddiario')
    main_window.setGeometry(100, 100, 350, 600)
    main_window.setWindowIcon(QIcon('res\\icon_main.png'))
    with open('res\\css.css', "r", encoding='utf-8') as file:
        main_window.setStyleSheet(file.read())

    # Layout principal (StackedLayout)
    layout = QStackedLayout()
    main_window.setLayout(layout)
    screens = {
        0: WelcomeScreen(lambda i: layout.setCurrentIndex(i)),
        1: LoginScreen(lambda i: layout.setCurrentIndex(i), db, set_current_user),
        2: RegisterScreen(lambda i: layout.setCurrentIndex(i), db, set_current_user),
        3: MainScreen(lambda i: layout.setCurrentIndex(i), db, get_current_user),
        4: CreateRoutineScreen(lambda i: layout.setCurrentIndex(i), db, get_current_user),
        5: EditRoutineScreen(lambda i: layout.setCurrentIndex(i), db, get_current_user),
        6: PorfileScreen(lambda i: layout.setCurrentIndex(i), db, get_current_user, set_current_user),
    }

    def on_tab_changed(index):
        # Si el index cambia a estas ventanas, actualiza los datos de sus listas
        if index == 3:  # Pantalla principal
            screens[3].update_routines()
        elif index == 4:  # Pantalla de edición
            screens[4].update()
        elif index == 5:  # Pantalla de edición
            screens[5].update_routines()
        elif index == 6: # Pantalla perfil
            screens[6].update_info()
    layout.currentChanged.connect(on_tab_changed)

    # Añade las ventans al stacked
    for i, screen in screens.items():
        layout.addWidget(screen)

    # Si se ha iniciado sesión, la mantiene
    if user["id"] == 'None':
        layout.setCurrentIndex(0)
    else:
        layout.setCurrentIndex(3)

    # Muestra la ventanta y prepara el cierre de la app
    main_window.show()
    sys.exit(app.exec_())



# Solo se ejecuta si el programa es lanzado desde esta ventana
if __name__ == "__main__":
    run()