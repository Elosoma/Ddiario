

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QDateEdit, QTimeEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QDate, QTime, QDateTime
from datetime import datetime

class DateTimeSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selector de Fecha y Hora")
        self.resize(300, 200)

        layout = QVBoxLayout()

        self.date_label = QLabel("Selecciona una fecha futura:")
        layout.addWidget(self.date_label)

        # Selector de fechas con restricción de fechas pasadas
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())  # Fecha inicial: hoy
        self.date_edit.setMinimumDate(QDate.currentDate())  # Fecha mínima: hoy
        layout.addWidget(self.date_edit)

        self.time_label = QLabel("Selecciona una hora futura:")
        layout.addWidget(self.time_label)

        # Selector de horas
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())  # Hora inicial: ahora
        layout.addWidget(self.time_edit)

        # Botón para validar la selección
        self.validate_button = QPushButton("Validar Selección")
        self.validate_button.clicked.connect(self.validate_selection)
        layout.addWidget(self.validate_button)

        self.setLayout(layout)

    def validate_selection(self):
        selected_date = self.date_edit.date().toPyDate()
        selected_time = self.time_edit.time().toPyTime()
        selected_datetime = datetime.combine(selected_date, selected_time)

        current_datetime = datetime.now()

        if selected_datetime <= current_datetime:
            QMessageBox.warning(self, "Fecha/Hora Inválida", "Selecciona una fecha y hora futuras.")
        else:
            QMessageBox.information(self, "Fecha/Hora Válida", f"Seleccionaste: {selected_datetime}")

if __name__ == "__main__":
    app = QApplication([])
    window = DateTimeSelector()
    window.show()
    app.exec_()
