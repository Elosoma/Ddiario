from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt,QDateTime,QDate
from PyQt5.QtWidgets import (
    QLayout,
    QWidget,
    QSizePolicy,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QHBoxLayout,
    QPushButton,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QTextEdit,
    QDoubleSpinBox,
    QDateEdit,
    QDateTimeEdit,
    QListWidgetItem,
    QComboBox,
    QStackedLayout,
    QApplication
)

import datetime, json, sys, re
from database_manager import (
    DatabaseManager,
    User,
    Note,
    Reminder,
    Birthday,
    Accounting,
    AccountMove,
    Food,
    Diet,
    Exercise,
    Routine
    )

def setLayoutBounds(
        layout:QLayout,
        margin = [0,0,0,0],
        padding = 0):
    layout.setContentsMargins(margin[0],margin[1],margin[2],margin[3])
    layout.setSpacing(padding)
    
def setLayoutWidget(
        layout:QLayout,
        objectName='self',
        fixedheight=False,
        fixedwidth=False,
        maximum=[False,None,None],
        minimum=[False,None,None]):
    widget = QWidget()
    widget.setLayout(layout)
    widget.setObjectName(objectName)

    widget.setSizePolicy(
        QSizePolicy.Expanding if fixedheight else QSizePolicy.Fixed,
        QSizePolicy.Expanding if fixedwidth else QSizePolicy.Fixed
    )

    if maximum[0]:
        if maximum[1]: widget.setMaximumHeight(maximum[1])
        if maximum[2]: widget.setMaximumWidth(maximum[2])
    if minimum[0]:
        if minimum[1]: widget.setMinimumHeight(minimum[1])
        if minimum[2]: widget.setMinimumWidth(minimum[2])
    return widget 

'''
 ##   ##    ##      ####    ##   ##            #####     ####   ######   #######  #######  ##   ##
 ### ###   ####      ##     ###  ##           ##   ##   ##  ##   ##  ##   ##   #   ##   #  ###  ##
 #######  ##  ##     ##     #### ##           #        ##        ##  ##   ## #     ## #    #### ##
 #######  ##  ##     ##     ## ####            #####   ##        #####    ####     ####    ## ####
 ## # ##  ######     ##     ##  ###                ##  ##        ## ##    ## #     ## #    ##  ###
 ##   ##  ##  ##     ##     ##   ##           ##   ##   ##  ##   ##  ##   ##   #   ##   #  ##   ##
 ##   ##  ##  ##    ####    ##   ##            #####     ####   #### ##  #######  #######  ##   ##
'''

class MainScreen(QWidget):
    def __init__(self, switch_screen, db:DatabaseManager, get_current_user):
        super().__init__()

        self.db = db
        self.switch_screen = switch_screen
        self.current_user = get_current_user()
        self.layout:QLayout = QVBoxLayout(self)

        # Mensaje de bienvenida con el username
        self.wellcoming = QLabel('BIENVENIDO user')
        self.wellcoming.setStyleSheet("font-size: 20px;")
        self.wellcoming.setWordWrap(True)
        self.layout.addWidget(self.wellcoming)

        # Label informativo
        self.label = QLabel("Recordatorios:")
        self.layout.addWidget(self.label)

        # Lista con las rutinas del usuario
        self.routine_list = QListWidget()
        self.layout.addWidget(self.routine_list)

        # Menú de navegación
        self.nav_menu()

    def nav_menu(self):
        # Primera fila de navegación
        first_widget = QWidget()
        first_row = QHBoxLayout(first_widget)
        setLayoutBounds(first_row,[0,0,0,0],5)

        # Botón pestaña de notas
        note_btn = QPushButton("NOTAS")
        note_btn.clicked.connect(lambda: self.switch_screen(8))
        first_row.addWidget(note_btn)

        # Botón pestaña de contabilidad
        account_btn = QPushButton("CONTABILIDAD")
        account_btn.clicked.connect(lambda: self.switch_screen(11))
        first_row.addWidget(account_btn)


        # Segunda fila de navegación
        second_widget = QWidget()
        second_row = QHBoxLayout(second_widget)
        setLayoutBounds(second_row,[0,0,0,0],5)

        # Botón pestaña de dietas
        diet_btn = QPushButton("DIETAS")
        diet_btn.clicked.connect(lambda: self.switch_screen(14))
        second_row.addWidget(diet_btn)

        # Botón pestaña de rutinas
        routine_btn = QPushButton("RUTINAS")
        routine_btn.clicked.connect(lambda: self.switch_screen(17))
        second_row.addWidget(routine_btn)


        # Cuerpo de navegación
        widget = QWidget()
        layout = QVBoxLayout(widget)
        setLayoutBounds(layout,[5,0,5,0],5)

        layout.addWidget(first_widget)
        layout.addWidget(second_widget)

        # Botón perfil
        profile_btn = QPushButton()
        profile_btn.setIcon(QIcon("res\\icon_2.png"))
        profile_btn.setText("Perfil")
        profile_btn.clicked.connect(lambda: self.switch_screen(4))
        layout.addWidget(profile_btn)

        self.layout.addWidget(widget)

    def update(self):
        # Limpia la lista y actualiza el mensaje de bienvenida
        self.routine_list.clear()
        self.wellcoming.setText(f'Bienvenido/a {self.current_user["username"]}')

        # Añade las rutinas del usuario activo
        routines = self.db.get_user_reminders(int(self.current_user['id'])) if self.current_user['id'] else []

        # Ordenar rutinas por proximidad a la fecha actual
        today = datetime.datetime.now()
        routines.sort(key=lambda routine: abs((datetime.datetime.strptime(routine.date,"%Y-%m-%d %H:%M") - today).days))

        for routine in routines:
            r_date = datetime.datetime.strptime(routine.date,"%Y-%m-%d %H:%M")
            if today <= r_date:
                self.routine_list.addItem(f"{routine.name}\n{routine.date}\n")

'''
 ##   ##  #######  ####     ####       ####    #####   ##   ##  #######            #####     ####   ######   #######  #######  ##   ##
 ##   ##   ##   #   ##       ##       ##  ##  ##   ##  ### ###   ##   #           ##   ##   ##  ##   ##  ##   ##   #   ##   #  ###  ##
 ##   ##   ## #     ##       ##      ##       ##   ##  #######   ## #             #        ##        ##  ##   ## #     ## #    #### ##
 ## # ##   ####     ##       ##      ##       ##   ##  #######   ####              #####   ##        #####    ####     ####    ## ####
 #######   ## #     ##   #   ##   #  ##       ##   ##  ## # ##   ## #                  ##  ##        ## ##    ## #     ## #    ##  ###
 ### ###   ##   #   ##  ##   ##  ##   ##  ##  ##   ##  ##   ##   ##   #           ##   ##   ##  ##   ##  ##   ##   #   ##   #  ##   ##
 ##   ##  #######  #######  #######    ####    #####   ##   ##  #######            #####     ####   #### ##  #######  #######  ##   ##
'''

class WelcomeScreen(QWidget):
    def __init__(self, switch_screen):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(self.wellcome())

        button = QPushButton("INICIO DE SESIÓN")
        button.setStyleSheet("font-size: 20px;")
        button.clicked.connect(lambda: switch_screen(2))
        layout.addWidget(button)

    def wellcome(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        img = QLabel()
        img.setPixmap(QPixmap("res\\frame_wellcome.png"))
        layout.addWidget(img)
        return widget

'''
 ####      #####     ####             ####    ##   ##
  ##      ##   ##   ##  ##             ##     ###  ##
  ##      ##   ##  ##                  ##     #### ##
  ##      ##   ##  ##                  ##     ## ####
  ##   #  ##   ##  ##  ###             ##     ##  ###
  ##  ##  ##   ##   ##  ##             ##     ##   ##
 #######   #####     #####            ####    ##   ##
'''

class LogInScreen(QWidget):
    def __init__(self,
                 switch_screen,
                 db:DatabaseManager,
                 set_current_user):
        super().__init__()

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
        mail = self.mail_input.text()
        password = self.password_input.text()

        # Comprueba los diferentes datos
        if is_mail(mail):
            user = self.db.get_user_mail(mail)
            if user:
                if user.password == password:
                    # Cambiamos el usuario actual y redirige a las pestaña principal
                    self.set_current_user(user)
                    self.switch_screen(0)
                else:
                    QMessageBox.warning(self, "Datos Incorrectos", "Revise que los datos introducidos sean correctos.")
            else:
                QMessageBox.warning(self, "Datos Incorrectos", "Correo no vinculado a una cuenta existente.")
        else:
            QMessageBox.warning(self, "Datos Incorrectos", "Campo correo inválido.")

'''
  #####    ####    ##   ##    ####            ##   ##  ######
 ##   ##    ##     ###  ##   ##  ##           ##   ##   ##  ##
 #          ##     #### ##  ##                ##   ##   ##  ##
  #####     ##     ## ####  ##                ##   ##   #####
      ##    ##     ##  ###  ##  ###           ##   ##   ##
 ##   ##    ##     ##   ##   ##  ##           ##   ##   ##
  #####    ####    ##   ##    #####            #####   ####
'''

class SingUpScreen(QWidget):
    def __init__(self,
                 switch_screen,
                 db:DatabaseManager,
                 set_current_user):
        super().__init__()

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

        # Botón de regreso
        back_button = QPushButton("Iniciar sesión")
        back_button.clicked.connect(lambda: switch_screen(2))
        layout.addWidget(back_button)

    def handle_register(self):
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
        if not self.db.get_user_mail(mail):
            QMessageBox.warning(self, "Error", "El siguiente correo ya se encuentra registrado")
            return

        # Comprueba que la contraseña y su confirmación sean iguales
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
            return

        try:
            # Intenta crear el usuario y redirige a la pestaña principal
            user = User(username,mail,password)
            self.db.add_user(user)
            QMessageBox.information(self, "Éxito", "Usuario registrado correctamente")
            
            self.set_current_user(user)
            self.switch_screen(0)
        except Exception as e:
            # Error no esperado de la db
            QMessageBox.warning(self, "Error", str(e))
            return

'''
 ######   ######    #####   #######   ####    ####     #######            #####     ####   ######   #######  #######  ##   ##
  ##  ##   ##  ##  ##   ##   ##   #    ##      ##       ##   #           ##   ##   ##  ##   ##  ##   ##   #   ##   #  ###  ##
  ##  ##   ##  ##  ##   ##   ## #      ##      ##       ## #             #        ##        ##  ##   ## #     ## #    #### ##
  #####    #####   ##   ##   ####      ##      ##       ####              #####   ##        #####    ####     ####    ## ####
  ##       ## ##   ##   ##   ## #      ##      ##   #   ## #                  ##  ##        ## ##    ## #     ## #    ##  ###
  ##       ##  ##  ##   ##   ##        ##      ##  ##   ##   #           ##   ##   ##  ##   ##  ##   ##   #   ##   #  ##   ##
 ####     #### ##   #####   ####      ####    #######  #######            #####     ####   #### ##  #######  #######  ##   ##
'''

class ProfileScreen(QWidget):
    def __init__(self,
                 switch_screen,
                 db:DatabaseManager,
                 get_current_user,
                 set_current_user):
        super().__init__()

        self.db = db
        self.switch_screen = switch_screen
        self.get_current_user = get_current_user
        self.set_current_user = set_current_user

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.porfile_icon())
        
        self.info_widget = self.user_info()
        layout.addWidget(self.info_widget)

        self.edit_widget = self.edit_info()
        layout.addWidget(self.edit_widget)
        self.edit_widget.hide()
        layout.addStretch()

        # Botón volver
        btn_back = QPushButton('Volver')
        btn_back.clicked.connect(lambda: switch_screen(0))
        layout.addWidget(btn_back)

        # Botón editar
        btn_edit = QPushButton('Editar')
        btn_edit.clicked.connect(self.handle_edit)
        layout.addWidget(btn_edit)

        # Botón cerrar sesión
        btn_log_out = QPushButton("Cerrar sesión")
        btn_log_out.clicked.connect(self.handle_log_out)
        layout.addWidget(btn_log_out)
    
    def update(self):
        current_user = self.get_current_user()
        user = self.db.get_user(int(current_user['id']))
        self.lbl_info.setText(f"Usuario: {current_user['username']}\nCorreo: {user.mail if user else ''}")

    def user_info(self):
        widget = QWidget()
        widget.setContentsMargins(0,0,0,0)
        layout = QHBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        self.lbl_info = QLabel('username')
        layout.addWidget(self.lbl_info)
        return widget
    
    def edit_info(self):
        widget = QWidget()
        widget.setContentsMargins(0,0,0,0)
        layout = QFormLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        # Añade las filas con los nombres de los campos
        layout.addRow("Usuario:", self.username_input)
        layout.addRow("Contraseña:", self.password_input)
        layout.addRow("Confirmar Contraseña:", self.confirm_password_input)

        # Botón cerrar sesión
        save_btn = QPushButton("Confirmar")
        save_btn.clicked.connect(self.handle_save)
        layout.addWidget(save_btn)

        # Botón cerrar sesión
        cancel_btn = QPushButton("Volver")
        cancel_btn.clicked.connect(self.handle_edit)
        layout.addWidget(cancel_btn)
        return widget

    def porfile_icon(self):
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
        with open("res\\user.json", "w", encoding='utf-8') as file:
            file.write(f'{json.dumps({"id": "None", "username": "None"})}')
        self.switch_screen(1) 

    def handle_edit(self):
        if self.edit_widget.isVisible():
            self.edit_widget.hide()
            self.username_input.setText('')
            self.password_input.setText('')
            self.confirm_password_input.setText('')
            self.info_widget.show()
        else:
            self.edit_widget.show()
            self.info_widget.hide()

    def handle_save(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        # Comprueba que los campos tengan contenido
        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return

        # Comprueba que la contraseña y su confirmación sean iguales
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
            return

        try:
            # Intenta crear el usuario y redirige a la pestaña principal
            current_user = self.get_current_user()
            user = self.db.get_user(int(current_user['id']))
            self.db.update_user(User(username,user.mail,password))
            QMessageBox.information(self, "Éxito", "Usuario actualizado correctamente")
            
            self.set_current_user(user)
            self.handle_edit()
            self.update()
        except Exception as e:
            # Error no esperado de la db
            QMessageBox.warning(self, "Error", str(e))
            print ("save")
            return

'''
 ##   ##   #####   ######   #######
 ###  ##  ##   ##  # ## #    ##   #
 #### ##  ##   ##    ##      ## #
 ## ####  ##   ##    ##      ####
 ##  ###  ##   ##    ##      ## #
 ##   ##  ##   ##    ##      ##   #
 ##   ##   #####    ####    #######
'''

class CreateEditNote(QWidget):
    def __init__(self,
                switch_screen,
                db:DatabaseManager,
                get_current_user,
                note:Note=Note('','')):
        
        super().__init__()
        self.db = db
        self.note=note
        self.object_id = None
        self.switch_screen = switch_screen
        self.current_user = get_current_user()
        self.layout:QLayout = QVBoxLayout(self)

        # Titulo de la pestaña
        title_lbl = QLabel("NOTA")
        title_lbl.setObjectName("header")
        self.layout.addWidget(title_lbl)

        # Formulario
        self.layout.addWidget(self.form_layout())
        self.layout.addStretch()

        # Botón para volver
        back_button = QPushButton("VOLVER")
        back_button.clicked.connect(lambda : self.switch_screen(8))
        self.layout.addWidget(back_button)

        # Botón para guardar rutina
        save_button = QPushButton("GUARDAR")
        save_button.clicked.connect(lambda : self.handle_save())
        self.layout.addWidget(save_button)

    def form_layout(self):
        layout = QFormLayout()

        # Editor de nombre
        self.name_input = QLineEdit()
        layout.addRow("NOMBRE:", self.name_input)

        # Editor de texto
        self.description_input = QTextEdit()
        layout.addRow("DESCRIPCIÓN:", self.description_input)

        widget = QWidget()
        widget.setLayout(layout)
        return widget
    
    def update(self):
        self.object_id = self.note.object_id
        self.name_input.setText(self.note.name)
        self.description_input.setText(self.note.description)

    def handle_save(self):
        if self.object_id:
            self.db.update_note(Note(self.name_input.text(),self.description_input.toPlainText(),self.object_id))
        else:
            self.db.add_note(int(self.current_user['id']), Note(self.name_input.text(),self.description_input.toPlainText()))
        self.note = Note('','')
        self.update()
        self.switch_screen(8)

'''
 ######   #######  ##   ##   ####    ##   ##  #####    #######  ######
  ##  ##   ##   #  ### ###    ##     ###  ##   ## ##    ##   #   ##  ##
  ##  ##   ## #    #######    ##     #### ##   ##  ##   ## #     ##  ##
  #####    ####    #######    ##     ## ####   ##  ##   ####     #####
  ## ##    ## #    ## # ##    ##     ##  ###   ##  ##   ## #     ## ##
  ##  ##   ##   #  ##   ##    ##     ##   ##   ## ##    ##   #   ##  ##
 #### ##  #######  ##   ##   ####    ##   ##  #####    #######  #### ##

'''

class CreateEditReminder(QWidget):
    def __init__(self,
                switch_screen,
                db:DatabaseManager,
                get_current_user,
                reminder:Reminder=Reminder('')):
        
        super().__init__()
        self.db = db
        self.object_id = None
        self.reminder = reminder
        self.switch_screen = switch_screen
        self.current_user = get_current_user()
        self.layout:QLayout = QVBoxLayout(self)

        # Titulo de la pestaña
        title_lbl = QLabel("RECORDATORIO")
        title_lbl.setObjectName("header")
        self.layout.addWidget(title_lbl)

        # Formulario
        self.layout.addWidget(self.form_layout())
        self.layout.addStretch()

        # Botón para volver
        back_button = QPushButton("VOLVER")
        back_button.clicked.connect(lambda : self.switch_screen(8))
        self.layout.addWidget(back_button)

        # Botón para guardar rutina
        save_button = QPushButton("GUARDAR")
        save_button.clicked.connect(lambda : self.handle_save())
        self.layout.addWidget(save_button)

    def form_layout(self):
        layout = QFormLayout()

        # Editor de nombre
        self.name_input = QLineEdit()
        layout.addRow("NOMBRE:", self.name_input)

        # Selector de fecha
        self.date_input = QDateTimeEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setMinimumDate(QDate.currentDate())
        layout.addRow("FECHA:", self.date_input)

        widget = QWidget()
        widget.setLayout(layout)
        return widget
    
    def update(self):
        self.object_id = self.reminder.object_id
        self.name_input.setText(self.reminder.name)
        self.date_input.setDateTime(
            QDateTime.currentDateTime()
            if self.reminder.name=='' else
            QDateTime.fromString(self.reminder.date,"yyyy-MM-dd HH:mm") 
        )

    def handle_save(self):
        if self.object_id:
            self.db.update_reminder(Reminder(self.name_input.text(),self.date_input.dateTime().toString("yyyy-MM-dd HH:mm"),self.object_id))
        else:
            self.db.add_reminder(int(self.current_user['id']), Reminder(self.name_input.text(),self.date_input.dateTime().toString("yyyy-MM-dd HH:mm")))
        self.reminder=Reminder('')
        self.update()
        self.switch_screen(8)

'''
 ######    ####    ######   ######   ##   ##  #####      ##     ##  ##
  ##  ##    ##      ##  ##  # ## #   ##   ##   ## ##    ####    ##  ##
  ##  ##    ##      ##  ##    ##     ##   ##   ##  ##  ##  ##   ##  ##
  #####     ##      #####     ##     #######   ##  ##  ##  ##    ####
  ##  ##    ##      ## ##     ##     ##   ##   ##  ##  ######     ##
  ##  ##    ##      ##  ##    ##     ##   ##   ## ##   ##  ##     ##
 ######    ####    #### ##   ####    ##   ##  #####    ##  ##    ####
'''

class CreateEditBirthday(QWidget):
    def __init__(self,
                switch_screen,
                db:DatabaseManager,
                get_current_user,
                birthday:Birthday=Birthday('')):
        
        super().__init__()
        self.db = db
        self.object_id = None
        self.birthday=birthday
        self.switch_screen = switch_screen
        self.current_user = get_current_user()
        self.layout:QLayout = QVBoxLayout(self)

        # Titulo de la pestaña
        title_lbl = QLabel("CUMPLEAÑOS")
        title_lbl.setObjectName("header")
        self.layout.addWidget(title_lbl)

        # Formulario
        self.layout.addWidget(self.form_layout())
        self.layout.addStretch()

        # Botón para volver
        back_button = QPushButton("VOLVER")
        back_button.clicked.connect(lambda : self.switch_screen(8))
        self.layout.addWidget(back_button)

        # Botón para guardar rutina
        save_button = QPushButton("GUARDAR")
        save_button.clicked.connect(lambda : self.handle_save())
        self.layout.addWidget(save_button)

    def form_layout(self):
        layout = QFormLayout()

        # Editor de nombre
        self.name_input = QLineEdit()
        layout.addRow("NOMBRE:", self.name_input)

        # Selector de fecha
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setMinimumDate(QDate.currentDate())
        layout.addRow("FECHA:", self.date_input)

        widget = QWidget()
        widget.setLayout(layout)
        return widget
    
    def update(self):
        self.object_id = self.birthday.object_id
        self.name_input.setText(self.birthday.name)
        self.date_input.setDate(
            QDate.currentDate()
            if self.birthday.name=='' else 
            QDate.fromString(self.birthday.date,"yyyy-MM-dd")
        )

    def handle_save(self):
        if self.object_id:
            self.db.update_reminder(Birthday(self.name_input.text(),self.date_input.date().toString("yyyy-MM-dd"),self.object_id))
        else:
            self.db.add_reminder(int(self.current_user['id']), Birthday(self.name_input.text(),self.date_input.date().toString("yyyy-MM-dd")))
        self.birthday = Birthday('')
        self.update()
        self.switch_screen(8)

'''
 ##   ##   #####   ######   #######            #####     ####   ######   #######  #######  ##   ##
 ###  ##  ##   ##  # ## #    ##   #           ##   ##   ##  ##   ##  ##   ##   #   ##   #  ###  ##
 #### ##  ##   ##    ##      ## #             #        ##        ##  ##   ## #     ## #    #### ##
 ## ####  ##   ##    ##      ####              #####   ##        #####    ####     ####    ## ####
 ##  ###  ##   ##    ##      ## #                  ##  ##        ## ##    ## #     ## #    ##  ###
 ##   ##  ##   ##    ##      ##   #           ##   ##   ##  ##   ##  ##   ##   #   ##   #  ##   ##
 ##   ##   #####    ####    #######            #####     ####   #### ##  #######  #######  ##   ##
'''

class NoteScreen(QWidget):
    def __init__(self,
                 switch_screen,
                 db:DatabaseManager,
                 get_current_user,
                 wdg_Note:CreateEditNote,
                 wdg_Reminder:CreateEditReminder,
                 wdg_Birthday:CreateEditBirthday):
        super().__init__()
        self.db = db
        self.switch_screen = switch_screen
        self.wdg_Note = wdg_Note
        self.wdg_Reminder = wdg_Reminder
        self.wdg_Birthday = wdg_Birthday
        self.current_user = get_current_user()
        self.get_current_user = get_current_user
        self.layout:QLayout = QVBoxLayout()

        self.label = QLabel("NOTAS Y RECORDATORIOS")
        self.layout.addWidget(self.label)

        self.routine_list = QListWidget()
        self.layout.addWidget(self.routine_list)

        self.update()

        delete_button = QPushButton("Añadir rutina")
        delete_button.clicked.connect(self.add_routine)
        self.layout.addWidget(delete_button)

        back_button = QPushButton("Volver")
        back_button.clicked.connect(lambda: self.switch_screen(0))
        self.layout.addWidget(back_button)

        self.setLayout(self.layout)
    
    def add_routine(self):
        def select_action():
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Nuevo recordatorio")
            msg_box.setText("¿Que tipo de nota quieres crear?")

            # Agregar botones personalizados
            btn_note = msg_box.addButton("Nota", QMessageBox.YesRole)
            btn_reminder = msg_box.addButton("Recordatorio", QMessageBox.YesRole)
            btn_birthday = msg_box.addButton("Cumpleaños", QMessageBox.YesRole)
            msg_box.addButton("Cancelar", QMessageBox.NoRole)

            msg_box.exec_()  # Mostrar el mensaje

            # Devolver qué botón fue presionado
            if msg_box.clickedButton() == btn_note:return 5
            elif msg_box.clickedButton() == btn_reminder:return 6
            elif msg_box.clickedButton() == btn_birthday:return 7
            else:return 8
        self.switch_screen(select_action())

    def update(self):
        self.routine_list.clear()
    
        notes = self.db.get_user_notes(int(self.current_user['id'])) if self.current_user['id'] else []
        for note in notes:
            class CustomNote(QWidget):
                def __init__(self, note:Note, parent):
                    super().__init__()
                    self.note = note
                    self.parent:NoteScreen = parent
                    self.layout:QLayout = QVBoxLayout(self)

                    show_btn = QPushButton(f'{self.note.name}\n\n')
                    show_btn.clicked.connect(self.show_details)
                    self.layout.addWidget(show_btn)

                def show_details(self):
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle(self.note.name)
                    msg_box.setText(self.note.description)

                    # Agregar botones personalizados
                    btn_edit = msg_box.addButton("Editar", QMessageBox.YesRole)
                    btn_delete = msg_box.addButton("Eliminar", QMessageBox.YesRole)
                    msg_box.addButton("Volver", QMessageBox.NoRole)

                    msg_box.exec_()  # Mostrar el mensaje
                    if msg_box.clickedButton() == btn_edit:
                        self.parent.wdg_Note.note = self.note
                        self.parent.switch_screen(5)
                    elif msg_box.clickedButton() == btn_delete:
                        if self.parent.confirm_action() == 1:
                            QMessageBox.information(self, "Éxito", "Nota eliminada correctamente") 
                            self.parent.db.delete_note(int(self.note.object_id))
                            self.parent.update()

            item = QListWidgetItem(self.routine_list)
            widget_personalizado = CustomNote(note, self)
            item.setSizeHint(widget_personalizado.sizeHint())
            self.routine_list.addItem(item)
            self.routine_list.setItemWidget(item, widget_personalizado)

        reminders = self.db.get_user_reminders(int(self.current_user['id'])) if self.current_user['id'] else []
        for reminder in reminders:
            class CustomReminder(QWidget):
                def __init__(self, reminder:Reminder, parent):
                    super().__init__()
                    self.reminder = reminder
                    self.parent:NoteScreen = parent
                    self.layout:QLayout = QVBoxLayout(self)
                    
                    show_btn = QPushButton(f'{self.reminder.name}\n{self.reminder.date}\n')
                    show_btn.clicked.connect(self.show_details)
                    self.layout.addWidget(show_btn)

                def show_details(self):
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle(self.reminder.name)
                    msg_box.setText(f'Fecha: {self.reminder.date}')

                    # Agregar botones personalizados
                    btn_edit = msg_box.addButton("Editar", QMessageBox.YesRole)
                    btn_delete = msg_box.addButton("Eliminar", QMessageBox.YesRole)
                    msg_box.addButton("Volver", QMessageBox.NoRole)

                    msg_box.exec_()  # Mostrar el mensaje
                    if msg_box.clickedButton() == btn_edit:
                        self.parent.wdg_Reminder.reminder = self.reminder
                        self.parent.switch_screen(6)
                    elif msg_box.clickedButton() == btn_delete:
                        if self.parent.confirm_action() == 1:
                            QMessageBox.information(self, "Éxito", "Nota eliminada correctamente") 
                            self.parent.db.delete_reminder(int(self.reminder.object_id))
                            self.parent.update()

            item = QListWidgetItem(self.routine_list)
            widget_personalizado = CustomReminder(reminder, self)
            item.setSizeHint(widget_personalizado.sizeHint())
            self.routine_list.addItem(item)
            self.routine_list.setItemWidget(item, widget_personalizado)

        
        birthdays = self.db.get_user_birthdays(int(self.current_user['id'])) if self.current_user['id'] else []
        for birthday in birthdays:
            class CustomBirthday(QWidget):
                def __init__(self, birthday:Birthday, parent):
                    super().__init__()
                    self.birthday = birthday
                    self.parent:NoteScreen = parent
                    self.layout:QLayout = QVBoxLayout(self)
                    
                    show_btn = QPushButton(f'{self.birthday.name}\n{self.birthday.date}\n')
                    show_btn.clicked.connect(self.show_details)
                    self.layout.addWidget(show_btn)

                def show_details(self):
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle(self.birthday.name)
                    msg_box.setText(f'Fecha: {self.birthday.date}')

                    # Agregar botones personalizados
                    btn_edit = msg_box.addButton("Editar", QMessageBox.YesRole)
                    btn_delete = msg_box.addButton("Eliminar", QMessageBox.YesRole)
                    msg_box.addButton("Volver", QMessageBox.NoRole)

                    msg_box.exec_()  # Mostrar el mensaje
                    if msg_box.clickedButton() == btn_edit:
                        self.parent.wdg_Birthday.birthday = self.birthday
                        self.parent.switch_screen(7)
                    elif msg_box.clickedButton() == btn_delete:
                        if self.parent.confirm_action() == 1:
                            QMessageBox.information(self, "Éxito", "Nota eliminada correctamente") 
                            self.parent.db.delete_birthday(int(self.birthday.object_id))
                            self.parent.update()

            item = QListWidgetItem(self.routine_list)
            widget_personalizado = CustomBirthday(birthday, self)
            item.setSizeHint(widget_personalizado.sizeHint())
            self.routine_list.addItem(item)
            self.routine_list.setItemWidget(item, widget_personalizado)

    def confirm_action(self):
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Confirmación")
            msg_box.setText("¿Quieres continuar con la acción?")

            # Agregar botones personalizados
            btn_si = msg_box.addButton("Sí", QMessageBox.YesRole)
            btn_no = msg_box.addButton("No", QMessageBox.NoRole)

            msg_box.exec_()  # Mostrar el mensaje

            # Devolver qué botón fue presionado
            if msg_box.clickedButton() == btn_si:
                return 1
            elif msg_box.clickedButton() == btn_no:
                return 0         

'''
   ##       ####     ####    #####   ##   ##  ##   ##  ######    ####    ##   ##    ####
  ####     ##  ##   ##  ##  ##   ##  ##   ##  ###  ##  # ## #     ##     ###  ##   ##  ##
 ##  ##   ##       ##       ##   ##  ##   ##  #### ##    ##       ##     #### ##  ##
 ##  ##   ##       ##       ##   ##  ##   ##  ## ####    ##       ##     ## ####  ##
 ######   ##       ##       ##   ##  ##   ##  ##  ###    ##       ##     ##  ###  ##  ###
 ##  ##    ##  ##   ##  ##  ##   ##  ##   ##  ##   ##    ##       ##     ##   ##   ##  ##
 ##  ##     ####     ####    #####    #####   ##   ##   ####     ####    ##   ##    #####
'''

class CreateEditAccounting(QWidget):
    def __init__(self,
                 switch_screen,
                 db:DatabaseManager,
                 getCurrentUser,
                 accounting:Accounting=Accounting('',0.0)):
        
        super().__init__()
        self.db = db
        self.object_id = None
        self.accounting = accounting
        self.current_user = getCurrentUser()
        self.switch_screen = switch_screen
        self.layout:QLayout = QVBoxLayout(self)

        # Titulo de la pestaña
        title_lbl = QLabel("CONTABILIDAD")
        title_lbl.setObjectName("header")
        self.layout.addWidget(title_lbl)

        # Formulario
        self.layout.addWidget(self.form_layout())
        self.layout.addStretch()

        # Botón para volver
        back_button = QPushButton("VOLVER")
        back_button.clicked.connect(lambda : self.switch_screen(11))
        self.layout.addWidget(back_button)

        # Botón para guardar rutina
        save_button = QPushButton("GUARDAR")
        save_button.clicked.connect(lambda : self.handle_save())
        self.layout.addWidget(save_button)

    def form_layout(self):
        layout = QFormLayout()

        # Editor de nombre
        self.name_input = QLineEdit()
        layout.addRow("NOMBRE:", self.name_input)

        # Selector de valor
        self.value_input = QDoubleSpinBox()
        self.value_input.setRange(-100000000.0, 100000000.0)
        self.value_input.setDecimals(2)
        layout.addRow("DINERO:", self.value_input)

        widget = QWidget()
        widget.setLayout(layout)
        return widget
    
    def update(self):
        self.object_id = self.accounting.object_id
        self.name_input.setText(self.accounting.name)
        try:
            self.value_input.setValue(float(self.accounting.amount))
        except:
            self.value_input.setValue(float(self.accounting.amount.replace(",", ".")))
    
    def handle_save(self):
        if self.object_id:
            self.db.update_accounting(Accounting(self.name_input.text(),self.value_input.value(),self.object_id))
        else:
            self.db.add_accounting(int(self.current_user['id']), Accounting(self.name_input.text(),self.value_input.value()))
        self.accounting = Accounting('',0.0)
        self.update()
        self.switch_screen(11)

'''
 ##   ##   #####   ##   ##  #######  ##   ##  #######  ##   ##  ######
 ### ###  ##   ##  ##   ##   ##   #  ### ###   ##   #  ###  ##  # ## #
 #######  ##   ##   ## ##    ## #    #######   ## #    #### ##    ##
 #######  ##   ##   ## ##    ####    #######   ####    ## ####    ##
 ## # ##  ##   ##    ###     ## #    ## # ##   ## #    ##  ###    ##
 ##   ##  ##   ##    ###     ##   #  ##   ##   ##   #  ##   ##    ##
 ##   ##   #####      #     #######  ##   ##  #######  ##   ##   ####
'''

class CreateEditMovement(QWidget):
    def __init__(self,
                 switch_screen,
                 db:DatabaseManager,
                 current_account:Accounting,
                 acount_move:AccountMove=AccountMove('',0.0)):
        
        super().__init__()
        self.db = db
        self.object_id = None
        self.acount_move = acount_move
        self.current_accounting = current_account
        self.switch_screen = switch_screen
        self.layout:QLayout = QVBoxLayout(self)

        # Titulo de la pestaña
        title_lbl = QLabel("MOVIMIENTO")
        title_lbl.setObjectName("header")
        self.layout.addWidget(title_lbl)

        # Formulario
        self.layout.addWidget(self.form_layout())
        self.layout.addStretch()

        # Botón para volver
        back_button = QPushButton("VOLVER")
        back_button.clicked.connect(lambda : self.switch_screen(11))
        self.layout.addWidget(back_button)

        # Botón para guardar rutina
        save_button = QPushButton("GUARDAR")
        save_button.clicked.connect(lambda : self.handle_save())
        self.layout.addWidget(save_button)

    def form_layout(self):
        layout = QFormLayout()

        # Editor de nombre
        self.name_input = QLineEdit()
        layout.addRow("NOMBRE:", self.name_input)

        # Selector de valor
        self.value_input = QDoubleSpinBox()
        self.value_input.setRange(-100000000.0, 100000000.0)
        self.value_input.setDecimals(2)
        layout.addRow("CONTIDAD:", self.value_input)

        # Selector de fecha
        self.date_input = QDateTimeEdit()
        self.date_input.setCalendarPopup(True)
        layout.addRow("FECHA:", self.date_input)

        widget = QWidget()
        widget.setLayout(layout)
        return widget
    
    def update(self):
        self.object_id = self.acount_move.object_id

        self.name_input.setText(self.acount_move.name)
        try:
            self.value_input.setValue(float(self.acount_move.amount))
        except:
            self.value_input.setValue(float(self.acount_move.amount.replace(",", ".")))
        
        self.date_input.setDateTime(
            QDateTime.currentDateTime()
            if self.acount_move.name=='' else
            QDateTime.fromString(self.acount_move.date,"yyyy-MM-dd HH:mm") 
        )
            
    def handle_save(self):
        if self.object_id:
            self.db.update_movement(AccountMove(self.name_input.text(),self.value_input.value(), self.date_input.dateTime().toString("yyyy-MM-dd HH:mm"),self.object_id))
        else:
            self.db.add_movement(int(self.current_accounting.object_id), AccountMove(self.name_input.text(),self.value_input.value()))
        self.acount_move = AccountMove('',0.0)
        self.update()
        self.switch_screen(11)

'''
   ##       ####     ####    #####   ##   ##  ##   ##  ######    ####    ##   ##    ####             #####     ####   ######   #######  #######  ##   ##
  ####     ##  ##   ##  ##  ##   ##  ##   ##  ###  ##  # ## #     ##     ###  ##   ##  ##           ##   ##   ##  ##   ##  ##   ##   #   ##   #  ###  ##
 ##  ##   ##       ##       ##   ##  ##   ##  #### ##    ##       ##     #### ##  ##                #        ##        ##  ##   ## #     ## #    #### ##
 ##  ##   ##       ##       ##   ##  ##   ##  ## ####    ##       ##     ## ####  ##                 #####   ##        #####    ####     ####    ## ####
 ######   ##       ##       ##   ##  ##   ##  ##  ###    ##       ##     ##  ###  ##  ###                ##  ##        ## ##    ## #     ## #    ##  ###
 ##  ##    ##  ##   ##  ##  ##   ##  ##   ##  ##   ##    ##       ##     ##   ##   ##  ##           ##   ##   ##  ##   ##  ##   ##   #   ##   #  ##   ##
 ##  ##     ####     ####    #####    #####   ##   ##   ####     ####    ##   ##    #####            #####     ####   #### ##  #######  #######  ##   ##
'''

class AccountingScreen(QWidget):
    def __init__(self,
                 switch_screen,
                 db:DatabaseManager,
                 get_current_user,
                 wdg_Accounting:CreateEditAccounting,
                 wdg_Movement:CreateEditMovement):
        super().__init__()
        self.db = db
        self.switch_screen = switch_screen
        self.wdg_Accounting = wdg_Accounting
        self.wdg_Movement = wdg_Movement
        self.current_user = get_current_user()
        self.get_current_user = get_current_user
        self.layout:QLayout = QVBoxLayout()

        self.label = QLabel("CONTABILIDAD")
        self.layout.addWidget(self.label)

        self.routine_list = QListWidget()
        self.layout.addWidget(self.routine_list)

        self.update()

        delete_button = QPushButton("Añadir contabilidad")
        delete_button.clicked.connect(lambda: self.switch_screen(9))
        self.layout.addWidget(delete_button)

        back_button = QPushButton("Volver")
        back_button.clicked.connect(lambda: self.switch_screen(0))
        self.layout.addWidget(back_button)

        self.setLayout(self.layout)

    def update(self):
        self.routine_list.clear()
    
        accountings = self.db.get_user_accountings(int(self.current_user['id'])) if self.current_user['id'] else []
        for accounting in accountings:
            class CustomAccounting(QWidget):
                def __init__(self, accounting:Accounting, parent):
                    super().__init__()
                    self.accounting = accounting
                    self.parent:AccountingScreen = parent
                    self.layout:QLayout = QVBoxLayout(self)

                    show_btn = QPushButton(f'{self.accounting.name}\nDinero: {self.accounting.amount}\n')
                    show_btn.clicked.connect(self.show_details)
                    self.layout.addWidget(show_btn)

                def show_details(self):
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle(self.accounting.name)
                    msg_box.setText(f'{self.accounting.amount}')

                    # Agregar botones personalizados
                    btn_edit = msg_box.addButton("Editar", QMessageBox.YesRole)
                    btn_delete = msg_box.addButton("Eliminar", QMessageBox.YesRole)
                    msg_box.addButton("Volver", QMessageBox.NoRole)

                    msg_box.exec_()  # Mostrar el mensaje
                    if msg_box.clickedButton() == btn_edit:
                        self.parent.wdg_Accounting.accounting = self.accounting
                        self.parent.switch_screen(9)
                    elif msg_box.clickedButton() == btn_delete:
                        if self.parent.confirm_action() == 1:
                            QMessageBox.information(self, "Éxito", "Nota eliminada correctamente") 
                            self.parent.db.delete_note(int(self.accounting.object_id))
                            self.parent.update()

            item = QListWidgetItem(self.routine_list)
            widget_personalizado = CustomAccounting(accounting, self)
            item.setSizeHint(widget_personalizado.sizeHint())
            self.routine_list.addItem(item)
            self.routine_list.setItemWidget(item, widget_personalizado)

    def confirm_action(self):
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Confirmación")
            msg_box.setText("¿Quieres continuar con la acción?")

            # Agregar botones personalizados
            btn_si = msg_box.addButton("Sí", QMessageBox.YesRole)
            btn_no = msg_box.addButton("No", QMessageBox.NoRole)

            msg_box.exec_()  # Mostrar el mensaje

            # Devolver qué botón fue presionado
            if msg_box.clickedButton() == btn_si:
                return 1
            elif msg_box.clickedButton() == btn_no:
                return 0

'''
 #######   #####    #####   #####
  ##   #  ##   ##  ##   ##   ## ##
  ## #    ##   ##  ##   ##   ##  ##
  ####    ##   ##  ##   ##   ##  ##
  ## #    ##   ##  ##   ##   ##  ##
  ##      ##   ##  ##   ##   ## ##
 ####      #####    #####   #####
'''

class CreateEditFood(QWidget):
    def __init__(self,
                switch_screen,
                db:DatabaseManager,
                get_current_user,
                food:Food=Food('',0.0,0)):
        
        super().__init__()
        self.db = db
        self.food=food
        self.object_id = None
        self.switch_screen = switch_screen
        self.current_user = get_current_user()
        self.layout:QLayout = QVBoxLayout(self)

        # Titulo de la pestaña
        title_lbl = QLabel("ALIMENTO")
        title_lbl.setObjectName("header")
        self.layout.addWidget(title_lbl)

        # Formulario
        self.layout.addWidget(self.form_layout())
        self.layout.addStretch()

        # Botón para volver
        back_button = QPushButton("VOLVER")
        back_button.clicked.connect(lambda : self.switch_screen(14))
        self.layout.addWidget(back_button)

        # Botón para guardar rutina
        save_button = QPushButton("GUARDAR")
        save_button.clicked.connect(lambda : self.handle_save())
        self.layout.addWidget(save_button)

    def form_layout(self):
        layout = QFormLayout()

        # Editor de nombre
        self.name_input = QLineEdit()
        layout.addRow("NOMBRE:", self.name_input)

        # Selector de valor
        self.value_input = QDoubleSpinBox()
        self.value_input.setRange(0, 100000000.0)
        self.value_input.setDecimals(2)
        layout.addRow("PRCIO:", self.value_input)

        # Selector de valor
        self.selection_input = QComboBox()
        self.selection_input.addItems(["Undiades","Litros","Gramos"])
        layout.addRow("MEDIDA:", self.selection_input)

        widget = QWidget()
        widget.setLayout(layout)
        return widget
    
    def update(self):
        self.object_id = self.food.object_id
        self.name_input.setText(self.food.name)
        self.value_input.setValue(self.food.price)
        self.selection_input.setCurrentIndex(self.food.measure)

    def handle_save(self):
        if self.object_id:
            self.db.update_note(Food(self.name_input.text(),self.value_input.value(),self.object_id))
        else:
            self.db.add_note(int(self.current_user['id']), Food(self.name_input.text(),self.value_input.value()))
        self.food = Food('',0.0,0)
        self.update()
        self.switch_screen(14)

'''
 #####     ####    #######  ######
  ## ##     ##      ##   #  # ## #
  ##  ##    ##      ## #      ##
  ##  ##    ##      ####      ##
  ##  ##    ##      ## #      ##
  ## ##     ##      ##   #    ##
 #####     ####    #######   ####
'''

class CreateEditDiet(QWidget):
    def __init__(self,
                switch_screen,
                db:DatabaseManager,
                get_current_user,
                diet:Diet=Diet('',0.0,"","","","","","","")):
        
        super().__init__()
        self.db = db
        self.diet=diet
        self.object_id = None
        self.switch_screen = switch_screen
        self.current_user = get_current_user()
        self.layout:QLayout = QVBoxLayout(self)

        # Titulo de la pestaña
        title_lbl = QLabel("DIETA")
        title_lbl.setObjectName("header")
        self.layout.addWidget(title_lbl)

        # Formulario
        self.layout.addWidget(self.form_layout())
        self.layout.addStretch()

        # Botón para volver
        back_button = QPushButton("VOLVER")
        back_button.clicked.connect(lambda : self.switch_screen(14))
        self.layout.addWidget(back_button)

        # Botón para guardar rutina
        save_button = QPushButton("GUARDAR")
        save_button.clicked.connect(lambda : self.handle_save())
        self.layout.addWidget(save_button)

    def form_layout(self):
        layout = QFormLayout()

        # Editor de nombre
        self.name_input = QLineEdit()
        layout.addRow("NOMBRE:", self.name_input)

        # Selector de valor
        self.value_input = QDoubleSpinBox()
        self.value_input.setRange(0, 100000000.0)
        self.value_input.setDecimals(2)
        layout.addRow("PRCIO:", self.value_input)

        # Editor de texto
        self.description_input = QTextEdit()
        layout.addRow("DESCRIPCIÓN:", self.description_input)

        widget = QWidget()
        widget.setLayout(layout)
        return widget
    
    def update(self):
        self.object_id = self.diet.object_id
        self.name_input.setText(self.diet.name)
        self.value_input.setValue(self.diet.price)
        self.description_input.setText(self.diet.monday_list)

    def handle_save(self):
        if self.object_id:
            self.db.update_note(Diet(self.name_input.text(), self.value_input.value(),self.description_input.toPlainText(),"","","","","","",self.object_id))
        else:
            self.db.add_note(int(self.current_user['id']), Diet(self.name_input.text(),self.value_input.value(),self.description_input.toPlainText(),"","","","","",""))
        self.diet = Diet('',0.0,"","","","","","","")
        self.update()
        self.switch_screen(14)

'''
 #####     ####    #######  ######             #####     ####   ######   #######  #######  ##   ##
  ## ##     ##      ##   #  # ## #            ##   ##   ##  ##   ##  ##   ##   #   ##   #  ###  ##
  ##  ##    ##      ## #      ##              #        ##        ##  ##   ## #     ## #    #### ##
  ##  ##    ##      ####      ##               #####   ##        #####    ####     ####    ## ####
  ##  ##    ##      ## #      ##                   ##  ##        ## ##    ## #     ## #    ##  ###
  ## ##     ##      ##   #    ##              ##   ##   ##  ##   ##  ##   ##   #   ##   #  ##   ##
 #####     ####    #######   ####              #####     ####   #### ##  #######  #######  ##   ##
'''

class DietScreen(QWidget):
    def __init__(self,
                 switch_screen,
                 db:DatabaseManager,
                 get_current_user,
                 wdg_Food:CreateEditFood,
                 wdg_Diet:CreateEditDiet):
        super().__init__()
        self.db = db
        self.switch_screen = switch_screen
        self.wdg_Food = wdg_Food
        self.wdg_Diet = wdg_Diet
        self.current_user = get_current_user()
        self.get_current_user = get_current_user
        self.layout:QLayout = QVBoxLayout()

        self.label = QLabel("DIETAS Y ALIMENTOS")
        self.layout.addWidget(self.label)

        self.routine_list = QListWidget()
        self.layout.addWidget(self.routine_list)

        self.update()

        delete_button = QPushButton("Añadir dieta")
        delete_button.clicked.connect(self.add_routine)
        self.layout.addWidget(delete_button)

        back_button = QPushButton("Volver")
        back_button.clicked.connect(lambda: self.switch_screen(0))
        self.layout.addWidget(back_button)

        self.setLayout(self.layout)
    
    def add_routine(self):
        def select_action():
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Nueva dieta")
            msg_box.setText("¿Que tipo de dieta quieres crear?")

            # Agregar botones personalizados
            btn_food = msg_box.addButton("Alimento", QMessageBox.YesRole)
            btn_diet = msg_box.addButton("Dieta", QMessageBox.YesRole)
            msg_box.addButton("Cancelar", QMessageBox.NoRole)

            msg_box.exec_()  # Mostrar el mensaje

            # Devolver qué botón fue presionado
            if msg_box.clickedButton() == btn_food:return 12
            elif msg_box.clickedButton() == btn_diet:return 13
            else:return 14
        self.switch_screen(select_action())

    def update(self):
        self.routine_list.clear()
    
        foods = self.db.get_user_foods(int(self.current_user['id'])) if self.current_user['id'] else []
        for food in foods:
            class CustomFood(QWidget):
                def __init__(self, food:Food, parent):
                    super().__init__()
                    self.food = food
                    self.parent:DietScreen = parent
                    self.layout:QLayout = QVBoxLayout(self)

                    show_btn = QPushButton(f'{self.food.name}\n\n')
                    show_btn.clicked.connect(self.show_details)
                    self.layout.addWidget(show_btn)

                def show_details(self):
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle(self.food.name)
                    measure = ["Ud","l","g"]
                    msg_box.setText(f'Precio: {self.food.price}/{measure[self.food.measure]}')

                    # Agregar botones personalizados
                    btn_edit = msg_box.addButton("Editar", QMessageBox.YesRole)
                    btn_delete = msg_box.addButton("Eliminar", QMessageBox.YesRole)
                    msg_box.addButton("Volver", QMessageBox.NoRole)

                    msg_box.exec_()  # Mostrar el mensaje
                    if msg_box.clickedButton() == btn_edit:
                        self.parent.wdg_Food.food = self.food
                        self.parent.switch_screen(12)
                    elif msg_box.clickedButton() == btn_delete:
                        if self.parent.confirm_action() == 1:
                            QMessageBox.information(self, "Éxito", "Comida eliminada correctamente") 
                            self.parent.db.delete_food(int(self.food.object_id))
                            self.parent.update()

            item = QListWidgetItem(self.routine_list)
            widget_personalizado = CustomFood(food, self)
            item.setSizeHint(widget_personalizado.sizeHint())
            self.routine_list.addItem(item)
            self.routine_list.setItemWidget(item, widget_personalizado)

        diets = self.db.get_user_diets(int(self.current_user['id'])) if self.current_user['id'] else []
        for diet in diets:
            class CustomReminder(QWidget):
                def __init__(self, diet:Diet, parent):
                    super().__init__()
                    self.diet = diet
                    self.parent:DietScreen = parent
                    self.layout:QLayout = QVBoxLayout(self)
                    
                    show_btn = QPushButton(f'{self.diet.name}\n\n')
                    show_btn.clicked.connect(self.show_details)
                    self.layout.addWidget(show_btn)

                def show_details(self):
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle(self.diet.name)
                    msg_box.setText(f'Precio: {self.diet.price}\n{self.diet.monday_list}')

                    # Agregar botones personalizados
                    btn_edit = msg_box.addButton("Editar", QMessageBox.YesRole)
                    btn_delete = msg_box.addButton("Eliminar", QMessageBox.YesRole)
                    msg_box.addButton("Volver", QMessageBox.NoRole)

                    msg_box.exec_()  # Mostrar el mensaje
                    if msg_box.clickedButton() == btn_edit:
                        self.parent.wdg_Diet.diet = self.diet
                        self.parent.switch_screen(13)
                    elif msg_box.clickedButton() == btn_delete:
                        if self.parent.confirm_action() == 1:
                            QMessageBox.information(self, "Éxito", "Dieta eliminada correctamente") 
                            self.parent.db.delete_diet(int(self.diet.object_id))
                            self.parent.update()

            item = QListWidgetItem(self.routine_list)
            widget_personalizado = CustomReminder(diet, self)
            item.setSizeHint(widget_personalizado.sizeHint())
            self.routine_list.addItem(item)
            self.routine_list.setItemWidget(item, widget_personalizado)

    def confirm_action(self):
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Confirmación")
            msg_box.setText("¿Quieres continuar con la acción?")

            # Agregar botones personalizados
            btn_si = msg_box.addButton("Sí", QMessageBox.YesRole)
            btn_no = msg_box.addButton("No", QMessageBox.NoRole)

            msg_box.exec_()  # Mostrar el mensaje

            # Devolver qué botón fue presionado
            if msg_box.clickedButton() == btn_si:
                return 1
            elif msg_box.clickedButton() == btn_no:
                return 0

'''
 #######  ##  ##   #######  ######     ####    ####     #####   #######
  ##   #  ##  ##    ##   #   ##  ##   ##  ##    ##     ##   ##   ##   #
  ## #     ####     ## #     ##  ##  ##         ##     #         ## #
  ####      ##      ####     #####   ##         ##      #####    ####
  ## #     ####     ## #     ## ##   ##         ##          ##   ## #
  ##   #  ##  ##    ##   #   ##  ##   ##  ##    ##     ##   ##   ##   #
 #######  ##  ##   #######  #### ##    ####    ####     #####   #######
'''

class CreateEditExercise(QWidget):
    def __init__(self,
                switch_screen,
                db:DatabaseManager,
                get_current_user,
                exercise:Exercise=Exercise('','')):
        
        super().__init__()
        self.db = db
        self.exercise=exercise
        self.object_id = None
        self.switch_screen = switch_screen
        self.current_user = get_current_user()
        self.layout:QLayout = QVBoxLayout(self)

        # Titulo de la pestaña
        title_lbl = QLabel("EJERCICIO")
        title_lbl.setObjectName("header")
        self.layout.addWidget(title_lbl)

        # Formulario
        self.layout.addWidget(self.form_layout())
        self.layout.addStretch()

        # Botón para volver
        back_button = QPushButton("VOLVER")
        back_button.clicked.connect(lambda : self.switch_screen(17))
        self.layout.addWidget(back_button)

        # Botón para guardar rutina
        save_button = QPushButton("GUARDAR")
        save_button.clicked.connect(lambda : self.handle_save())
        self.layout.addWidget(save_button)

    def form_layout(self):
        layout = QFormLayout()

        # Editor de nombre
        self.name_input = QLineEdit()
        layout.addRow("NOMBRE:", self.name_input)

        # Editor de texto
        self.description_input = QTextEdit()
        layout.addRow("DESCRIPCIÓN:", self.description_input)

        widget = QWidget()
        widget.setLayout(layout)
        return widget
    
    def update(self):
        self.object_id = self.exercise.object_id
        self.name_input.setText(self.exercise.name)
        self.description_input.setText(self.exercise.description)

    def handle_save(self):
        if self.object_id:
            self.db.update_note(Exercise(self.name_input.text(),self.description_input.toPlainText(),self.object_id))
        else:
            self.db.add_note(int(self.current_user['id']), Exercise(self.name_input.text(),self.description_input.toPlainText()))
        self.exercise = Exercise('','')
        self.update()
        self.switch_screen(17)

'''
 ######    #####   ##   ##  ######    ####    ##   ##  #######
  ##  ##  ##   ##  ##   ##  # ## #     ##     ###  ##   ##   #
  ##  ##  ##   ##  ##   ##    ##       ##     #### ##   ## #
  #####   ##   ##  ##   ##    ##       ##     ## ####   ####
  ## ##   ##   ##  ##   ##    ##       ##     ##  ###   ## #
  ##  ##  ##   ##  ##   ##    ##       ##     ##   ##   ##   #
 #### ##   #####    #####    ####     ####    ##   ##  #######
'''

class CreateEditRoutine(QWidget):
    def __init__(self,
                switch_screen,
                db:DatabaseManager,
                get_current_user,
                routine:Routine=Routine('','')):
        
        super().__init__()
        self.db = db
        self.routine=routine
        self.object_id = None
        self.switch_screen = switch_screen
        self.current_user = get_current_user()
        self.layout:QLayout = QVBoxLayout(self)

        # Titulo de la pestaña
        title_lbl = QLabel("RUTINA")
        title_lbl.setObjectName("header")
        self.layout.addWidget(title_lbl)

        # Formulario
        self.layout.addWidget(self.form_layout())
        self.layout.addStretch()

        # Botón para volver
        back_button = QPushButton("VOLVER")
        back_button.clicked.connect(lambda : self.switch_screen(17))
        self.layout.addWidget(back_button)

        # Botón para guardar rutina
        save_button = QPushButton("GUARDAR")
        save_button.clicked.connect(lambda : self.handle_save())
        self.layout.addWidget(save_button)

    def form_layout(self):
        layout = QFormLayout()

        # Editor de nombre
        self.name_input = QLineEdit()
        layout.addRow("NOMBRE:", self.name_input)

        # Editor de texto
        self.description_input = QTextEdit()
        layout.addRow("DESCRIPCIÓN:", self.description_input)

        widget = QWidget()
        widget.setLayout(layout)
        return widget
    
    def update(self):
        self.object_id = self.routine.object_id
        self.name_input.setText(self.routine.name)
        self.description_input.setText(self.routine.description)

    def handle_save(self):
        if self.object_id:
            self.db.update_routine(Routine(self.name_input.text(),self.description_input.toPlainText(),self.object_id))
        else:
            self.db.add_routine(int(self.current_user['id']), Routine(self.name_input.text(),self.description_input.toPlainText()))
        self.routine = Routine('','')
        self.update()
        self.switch_screen(17)

'''
 ######    #####   ##   ##  ######    ####    ##   ##  #######            #####     ####   ######   #######  #######  ##   ##
  ##  ##  ##   ##  ##   ##  # ## #     ##     ###  ##   ##   #           ##   ##   ##  ##   ##  ##   ##   #   ##   #  ###  ##
  ##  ##  ##   ##  ##   ##    ##       ##     #### ##   ## #             #        ##        ##  ##   ## #     ## #    #### ##
  #####   ##   ##  ##   ##    ##       ##     ## ####   ####              #####   ##        #####    ####     ####    ## ####
  ## ##   ##   ##  ##   ##    ##       ##     ##  ###   ## #                  ##  ##        ## ##    ## #     ## #    ##  ###
  ##  ##  ##   ##  ##   ##    ##       ##     ##   ##   ##   #           ##   ##   ##  ##   ##  ##   ##   #   ##   #  ##   ##
 #### ##   #####    #####    ####     ####    ##   ##  #######            #####     ####   #### ##  #######  #######  ##   ##
'''

class RoutineScreen(QWidget):
    def __init__(self,
                 switch_screen,
                 db:DatabaseManager,
                 get_current_user,
                 wdg_Exercise:CreateEditExercise,
                 wdg_Routine:CreateEditRoutine):
        super().__init__()
        self.db = db
        self.switch_screen = switch_screen
        self.wdg_Exercise = wdg_Exercise
        self.wdg_Routine = wdg_Routine
        
        self.current_user = get_current_user()
        self.get_current_user = get_current_user
        self.layout:QLayout = QVBoxLayout()

        self.label = QLabel("RUTINAS Y EJERCICIOS")
        self.layout.addWidget(self.label)

        self.routine_list = QListWidget()
        self.layout.addWidget(self.routine_list)

        self.update()

        delete_button = QPushButton("Añadir rutina")
        delete_button.clicked.connect(self.add_routine)
        self.layout.addWidget(delete_button)

        back_button = QPushButton("Volver")
        back_button.clicked.connect(lambda: self.switch_screen(0))
        self.layout.addWidget(back_button)

        self.setLayout(self.layout)
    
    def add_routine(self):
        def select_action():
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Nueva rutina")
            msg_box.setText("¿Que tipo quieres crear?")

            # Agregar botones personalizados
            btn_routine = msg_box.addButton("Rutina", QMessageBox.YesRole)
            btn_exercise = msg_box.addButton("Ejercicio", QMessageBox.YesRole)
            msg_box.addButton("Cancelar", QMessageBox.NoRole)

            msg_box.exec_()  # Mostrar el mensaje

            # Devolver qué botón fue presionado
            if msg_box.clickedButton() == btn_routine:return 15
            elif msg_box.clickedButton() == btn_exercise:return 16
            else:return 17
        self.switch_screen(select_action())

    def update(self):
        self.routine_list.clear()
    
        exercises = self.db.get_user_exercises(int(self.current_user['id'])) if self.current_user['id'] else []
        for exercise in exercises:
            class CustomExercise(QWidget):
                def __init__(self, exercise:Exercise, parent):
                    super().__init__()
                    self.exercise = exercise
                    self.parent:RoutineScreen = parent
                    self.layout:QLayout = QVBoxLayout(self)

                    show_btn = QPushButton(f'{self.exercise.name}\n\n')
                    show_btn.clicked.connect(self.show_details)
                    self.layout.addWidget(show_btn)

                def show_details(self):
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle(self.exercise.name)
                    msg_box.setText(self.exercise.description)

                    # Agregar botones personalizados
                    btn_edit = msg_box.addButton("Editar", QMessageBox.YesRole)
                    btn_delete = msg_box.addButton("Eliminar", QMessageBox.YesRole)
                    msg_box.addButton("Volver", QMessageBox.NoRole)

                    msg_box.exec_()  # Mostrar el mensaje
                    if msg_box.clickedButton() == btn_edit:
                        self.parent.wdg_Exercise.exercise = self.exercise
                        self.parent.switch_screen(15)
                    elif msg_box.clickedButton() == btn_delete:
                        if self.parent.confirm_action() == 1:
                            QMessageBox.information(self, "Éxito", "Rutina eliminada correctamente") 
                            self.parent.db.delete_note(int(self.exercise.object_id))
                            self.parent.update()

            item = QListWidgetItem(self.routine_list)
            widget_personalizado = CustomExercise(exercise, self)
            item.setSizeHint(widget_personalizado.sizeHint())
            self.routine_list.addItem(item)
            self.routine_list.setItemWidget(item, widget_personalizado)

        routines = self.db.get_user_routines(int(self.current_user['id'])) if self.current_user['id'] else []
        for routine in routines:
            class CustomRoutine(QWidget):
                def __init__(self, routine:Routine, parent):
                    super().__init__()
                    self.routine = routine
                    self.parent:RoutineScreen = parent
                    self.layout:QLayout = QVBoxLayout(self)
                    
                    show_btn = QPushButton(f'{self.routine.name}\n\n')
                    show_btn.clicked.connect(self.show_details)
                    self.layout.addWidget(show_btn)

                def show_details(self):
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle(self.routine.name)
                    msg_box.setText(f'{self.routine.description}')

                    # Agregar botones personalizados
                    btn_edit = msg_box.addButton("Editar", QMessageBox.YesRole)
                    btn_delete = msg_box.addButton("Eliminar", QMessageBox.YesRole)
                    msg_box.addButton("Volver", QMessageBox.NoRole)

                    msg_box.exec_()  # Mostrar el mensaje
                    if msg_box.clickedButton() == btn_edit:
                        self.parent.wdg_Routine.routine = self.routine
                        self.parent.switch_screen(16)
                    elif msg_box.clickedButton() == btn_delete:
                        if self.parent.confirm_action() == 1:
                            QMessageBox.information(self, "Éxito", "Nota eliminada correctamente") 
                            self.parent.db.delete_reminder(int(self.routine.object_id))
                            self.parent.update()

            item = QListWidgetItem(self.routine_list)
            widget_personalizado = CustomRoutine(routine, self)
            item.setSizeHint(widget_personalizado.sizeHint())
            self.routine_list.addItem(item)
            self.routine_list.setItemWidget(item, widget_personalizado)

    def confirm_action(self):
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Confirmación")
            msg_box.setText("¿Quieres continuar con la acción?")

            # Agregar botones personalizados
            btn_si = msg_box.addButton("Sí", QMessageBox.YesRole)
            btn_no = msg_box.addButton("No", QMessageBox.NoRole)

            msg_box.exec_()  # Mostrar el mensaje

            # Devolver qué botón fue presionado
            if msg_box.clickedButton() == btn_si:
                return 1
            elif msg_box.clickedButton() == btn_no:
                return 0 

'''
 #####    #######  ######   ##   ##    ####
  ## ##    ##   #   ##  ##  ##   ##   ##  ##
  ##  ##   ## #     ##  ##  ##   ##  ##
  ##  ##   ####     #####   ##   ##  ##
  ##  ##   ## #     ##  ##  ##   ##  ##  ###
  ## ##    ##   #   ##  ##  ##   ##   ##  ##
 #####    #######  ######    #####     #####
'''

def is_mail(mail):
    """Comprueba si el texto dado tiene el formato de un correo electrónico válido."""
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, mail) is not None

def run():
    # Variables
    app = QApplication(sys.argv)
    db = DatabaseManager()

    # Comprobación de sesión
    with open("res\\user.json", "r", encoding='utf-8') as file:
        user = json.load(file)
    current_user = {
        'id': None if user["id"] == 'None' else user["id"],
        'username': None if user["username"] == 'None' else user["username"]
    }

    def get_current_user():
        '''Devuelve la variable del usuario actual'''
        return current_user

    def set_current_user(user:User):
        '''Cambia el usuario actual'''
        current_user['id'] = user.object_id
        current_user['username'] = user.username
        with open("res\\user.json", "w", encoding='utf-8') as file:
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

    wdg_Note = CreateEditNote(lambda i: layout.setCurrentIndex(i),db,get_current_user)
    wdg_Reminder = CreateEditReminder(lambda i: layout.setCurrentIndex(i),db,get_current_user)
    wdg_Birthday = CreateEditBirthday(lambda i: layout.setCurrentIndex(i),db,get_current_user)

    wdg_Accounting = CreateEditAccounting(lambda i: layout.setCurrentIndex(i),db,get_current_user)
    wdg_Movements = CreateEditMovement(lambda i: layout.setCurrentIndex(i),db,get_current_user)

    wdg_Food = CreateEditFood(lambda i: layout.setCurrentIndex(i),db,get_current_user)
    wdg_Diet = CreateEditDiet(lambda i: layout.setCurrentIndex(i),db,get_current_user)

    wdg_Exercise = CreateEditExercise(lambda i: layout.setCurrentIndex(i),db,get_current_user)
    wdg_Routine = CreateEditRoutine(lambda i: layout.setCurrentIndex(i),db,get_current_user)

    screens = {
        0: MainScreen(lambda i: layout.setCurrentIndex(i),db,get_current_user),

        1: WelcomeScreen(lambda i: layout.setCurrentIndex(i)),
        2: LogInScreen(lambda i: layout.setCurrentIndex(i),db,set_current_user),
        3: SingUpScreen(lambda i: layout.setCurrentIndex(i),db,set_current_user),
        4: ProfileScreen(lambda i: layout.setCurrentIndex(i),db,get_current_user,set_current_user),

        5: wdg_Note,
        6: wdg_Reminder,
        7: wdg_Birthday,
        8: NoteScreen(lambda i: layout.setCurrentIndex(i),db,get_current_user,wdg_Note,wdg_Reminder,wdg_Birthday),
        
        9: wdg_Accounting,
        10: wdg_Movements,
        11: AccountingScreen(lambda i: layout.setCurrentIndex(i),db,get_current_user,wdg_Accounting,wdg_Movements),

        12: wdg_Food,
        13: wdg_Diet,
        14: DietScreen(lambda i: layout.setCurrentIndex(i),db,get_current_user,wdg_Food,wdg_Diet),

        15: wdg_Exercise,
        16: wdg_Routine,
        17: RoutineScreen(lambda i: layout.setCurrentIndex(i),db,get_current_user,wdg_Exercise,wdg_Routine)
    }

    def on_tab_changed(index):
        if index == 0:
            screens[0].update()
        elif index == 4:
            screens[4].update()
        elif index == 5:
            screens[5].update()
        elif index == 6:
            screens[6].update()
        elif index == 7:
            screens[7].update()
        elif index == 8:
            screens[8].update()
        elif index == 9:
            screens[9].update()
        elif index == 10:
            screens[10].update()
        elif index == 11:
            screens[11].update()
        elif index == 12:
            screens[12].update()
        elif index == 13:
            screens[13].update()
        elif index == 14:
            screens[14].update()
        elif index == 15:
            screens[15].update()
        elif index == 16:
            screens[16].update()
        elif index == 17:
            screens[17].update()
    layout.currentChanged.connect(on_tab_changed)

    # Añade las ventans al stacked
    for i, screen in screens.items():
        layout.addWidget(screen)

    # Si se ha iniciado sesión, la mantiene
    if user["id"] == 'None':
        layout.setCurrentIndex(1)
    else:
        layout.setCurrentIndex(0)

    # Muestra la ventanta y prepara el cierre de la app
    main_window.show()
    sys.exit(app.exec_())

# DEBUG, Inicia la interfaz gráfica
if __name__ == "__main__":
    run()