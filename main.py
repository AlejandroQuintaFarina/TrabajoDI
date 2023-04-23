import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
import sqlite3

class PeluqueriaApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar ventana principal
        self.setWindowTitle('Registro de Citas y Productos')
        self.setGeometry(100, 100, 600, 400)

        # Crear widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Crear cajas de texto y botones
        self.nombre_edit = QLineEdit()
        self.servicio_edit = QLineEdit()
        self.producto_edit = QLineEdit()
        self.citas_table = QTableWidget()
        self.citas_table.setColumnCount(3)
        self.citas_table.setHorizontalHeaderLabels(['Nombre', 'Servicio', 'Producto'])
        self.registrar_button = QPushButton('Registrar Cita')
        self.registrar_button.clicked.connect(self.registrar_cita)

        # Crear diseño de la interfaz
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox1.addWidget(QLabel('Nombre:'))
        hbox1.addWidget(self.nombre_edit)
        hbox2.addWidget(QLabel('Servicio:'))
        hbox2.addWidget(self.servicio_edit)
        hbox3.addWidget(QLabel('Producto:'))
        hbox3.addWidget(self.producto_edit)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addWidget(self.registrar_button)
        vbox.addWidget(self.citas_table)
        central_widget.setLayout(vbox)

        # Conectar a la base de datos
        self.conexion = sqlite3.connect('peluqueria.db')
        self.cursor = self.conexion.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS citas (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, servicio TEXT, producto TEXT)''')
        self.conexion.commit()

    def registrar_cita(self):
        nombre = self.nombre_edit.text()
        servicio = self.servicio_edit.text()
        producto = self.producto_edit.text()
        if nombre and servicio and producto:
            self.cursor.execute('''INSERT INTO citas (nombre, servicio, producto) VALUES (?, ?, ?)''', (nombre, servicio, producto))
            self.conexion.commit()
            self.cargar_citas()

    def cargar_citas(self):
        self.citas_table.clearContents()
        self.citas_table.setRowCount(0)
        self.cursor.execute('''SELECT nombre, servicio, producto FROM citas''')
        citas = self.cursor.fetchall()
        for row, cita in enumerate(citas):
            self.citas_table.insertRow(row)
            for col, value in enumerate(cita):
                self.citas_table.setItem(row, col, QTableWidgetItem(str(value)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = PeluqueriaApp()
