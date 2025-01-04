import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QStackedLayout, QPushButton, QLabel, QLineEdit, QFormLayout, QHBoxLayout, QListWidget, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from database_manager import DatabaseManager, Routine

class WelcomeScreen(QWidget):
    def __init__(self, switch_screen):
        super().__init__()
        layout = QVBoxLayout()

        img = QLabel()
        img.setPixmap(QPixmap("res\\wellcome.png"))
        layout.addWidget(img)

        button = QPushButton("Ir al inicio de sesión")
        button.clicked.connect(lambda: switch_screen(1))
        layout.addWidget(button)

        self.setLayout(layout)

class LoginScreen(QWidget):
    def __init__(self, switch_screen, db, set_current_user):
        super().__init__()
        self.db = db
        self.set_current_user = set_current_user
        self.switch_screen = switch_screen
        self.current_user = None
        layout = QFormLayout()

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        layout.addRow("Usuario:", self.username_input)
        layout.addRow("Contraseña:", self.password_input)

        login_button = QPushButton("Iniciar sesión")
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)

        register_button = QPushButton("Registrar usuario")
        register_button.clicked.connect(lambda: switch_screen(2))
        layout.addWidget(register_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user = self.db.get_user(username)
        if user:
            if user.password == password:
                self.set_current_user(user)
                self.switch_screen(3)
            else:
                QMessageBox.warning(self, "Error", "Contraseña incorrecta")
        else:
            QMessageBox.warning(self, "Error", "Mail incorrecto")

class RegisterScreen(QWidget):
    def __init__(self, switch_screen, db):
        super().__init__()
        self.db = db
        self.switch_screen = switch_screen
        layout = QFormLayout()

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        layout.addRow("Usuario:", self.username_input)
        layout.addRow("Contraseña:", self.password_input)
        layout.addRow("Confirmar Contraseña:", self.confirm_password_input)

        register_button = QPushButton("Registrar")
        register_button.clicked.connect(self.handle_register)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
            return

        try:
            self.db.add_user(username, password)
            QMessageBox.information(self, "Éxito", "Usuario registrado correctamente")
            self.switch_screen(1)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

class MainScreen(QWidget):
    def __init__(self, switch_screen, db, get_current_user):
        super().__init__()
        self.db = db
        self.get_current_user = get_current_user
        self.switch_screen = switch_screen
        self.layout = QVBoxLayout()

        self.label = QLabel("Rutinas próximas")
        self.layout.addWidget(self.label)

        self.routine_list = QListWidget()
        self.layout.addWidget(self.routine_list)

        self.update_routines()

        create_button = QPushButton("Crear rutina")
        create_button.clicked.connect(lambda: switch_screen(4))
        self.layout.addWidget(create_button)

        edit_button = QPushButton("Editar rutinas")
        edit_button.clicked.connect(lambda: switch_screen(5))
        self.layout.addWidget(edit_button)

        self.setLayout(self.layout)

    def update_routines(self):
        self.routine_list.clear()
        current_user = self.get_current_user()
        routines = self.db.get_user_routines(current_user['id']) if current_user['id'] else []
        for routine in routines:
            self.routine_list.addItem(f"{routine.name} - {routine.date}")

class CreateRoutineScreen(QWidget):
    def __init__(self, switch_screen, db, get_current_user):
        super().__init__()
        self.db = db
        self.get_current_user = get_current_user
        self.switch_screen = switch_screen

        self.layout = QFormLayout()

        self.name_input = QLineEdit()
        self.date_input = QLineEdit()
        self.description_input = QLineEdit()
        self.recurring_selector = QComboBox()
        self.recurring_selector.addItems(["Única vez", "Diaria", "Semanal", "Mensual"])

        self.layout.addRow("Nombre:", self.name_input)
        self.layout.addRow("Fecha:", self.date_input)
        self.layout.addRow("Descripción:", self.description_input)
        self.layout.addRow("Repetir:", self.recurring_selector)

        save_button = QPushButton("Guardar rutina")
        save_button.clicked.connect(self.handle_save)
        self.layout.addWidget(save_button)

        self.setLayout(self.layout)

    def handle_save(self):
        name = self.name_input.text()
        date = self.date_input.text()
        description = self.description_input.text()
        is_recurring = self.recurring_selector.currentIndex() > 0

        if not name or not date:
            QMessageBox.warning(self, "Error", "El nombre y la fecha son obligatorios")
            return

        current_user = self.get_current_user()
        if not current_user:
            QMessageBox.warning(self, "Error", "No hay usuario autenticado")
            return

        print (f'{current_user["id"]} - {name} - {description} - {date} -- {is_recurring}')
        routine = Routine(current_user['id'], name, description, date, is_recurring)
        self.db.add_routine(routine)
        QMessageBox.information(self, "Éxito", "Rutina guardada correctamente")
        self.switch_screen(3)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)

    db = DatabaseManager()
    current_user = {'id': None, 'username': None}

    def get_current_user():
        return current_user

    def set_current_user(user):
        current_user['id'] = user.id
        current_user['username'] = user.username

    main_window = QWidget()
    main_window.setGeometry(100, 100, 350, 600)
    with open('res\\css.css', "r", encoding='utf-8') as file:
        main_window.setStyleSheet(file.read())

    layout = QStackedLayout()
    main_window.setLayout(layout)

    screens = {
        0: WelcomeScreen(lambda i: layout.setCurrentIndex(i)),
        1: LoginScreen(lambda i: layout.setCurrentIndex(i), db, set_current_user),
        2: RegisterScreen(lambda i: layout.setCurrentIndex(i), db),
        3: MainScreen(lambda i: layout.setCurrentIndex(i), db, get_current_user),
        4: CreateRoutineScreen(lambda i: layout.setCurrentIndex(i), db, get_current_user),
        5: EditRoutineScreen(lambda i: layout.setCurrentIndex(i), db, get_current_user),
    }

    for i, screen in screens.items():
        layout.addWidget(screen)

    layout.setCurrentIndex(0)

    main_window.show()
    sys.exit(app.exec_())
