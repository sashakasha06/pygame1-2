import io
import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QStatusBar, QFormLayout, QPlainTextEdit, \
    QPushButton, QWidget
temp = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QWidget" name="verticalLayoutWidget">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>9</y>
      <width>770</width>
      <height>300</height>
     </rect>
    </property>
    <layout class="QVBoxLayout" name="verticalLayout">
     <item>
      <widget class="QPushButton" name="pushbut">
       <property name="text">
        <string>PushButton</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QTableWidget" name="tableWidget"/>
     </item>
     <item>
      <widget class="QPushButton" name="addbutton">
       <property name="text">
        <string>Добавить</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="editbutton">
       <property name="text">
        <string>Редактировать</string>
       </property>
      </widget>
     </item>
    </layout>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
     <height>18</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>'''


class coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(temp)
        uic.loadUi(f, self)

        self.pushbut.clicked.connect(self.butclicked)
        self.addbutton.clicked.connect(self.add_coffee)
        self.editbutton.clicked.connect(self.edit_coffee)
        self.pushbut.setText("Кофе!")
        self.tableWidget.setColumnCount(7)
        for i in range(7):
            self.tableWidget.setColumnWidth(i, 110)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "название сорта", "степень обжарки", "молотый/в зернах", "описание вкуса", "цена", "объем упаковки"])

    def butclicked(self):
        conn = sqlite3.connect('data/coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM coffee''')
        rows = cursor.fetchall()
        self.tableWidget.setRowCount(len(rows))
        for row_number, row_data in enumerate(rows):
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_coffee(self):
        self.add_coffee_widget = AddcoffeeWidget(self)
        self.add_coffee_widget.show()

    def edit_coffee(self):
        current_row = self.tableWidget.currentRow()
        if current_row == -1:
            return False
        coffee_id = int(self.tableWidget.item(current_row, 0).text())
        self.edit_coffee_widget = AddcoffeeWidget(self, coffee_id)
        self.edit_coffee_widget.show()

class AddcoffeeWidget(QMainWindow):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить/Редактировать кофе')
        self.con = sqlite3.connect('data/coffee.sqlite')
        self.coffee_id = coffee_id
        self.layout = QFormLayout()
        self.params = {}

        # Поля для ввода данных
        self.title = QPlainTextEdit()
        self.title.setMaximumHeight(40)
        self.objar_text = QPlainTextEdit()
        self.objar_text.setMaximumHeight(40)
        self.molzer_text = QPlainTextEdit()
        self.molzer_text.setMaximumHeight(40)
        self.opis_text = QPlainTextEdit()
        self.opis_text.setMaximumHeight(40)
        self.cena_text = QPlainTextEdit()
        self.cena_text.setMaximumHeight(40)
        self.obem_text = QPlainTextEdit()
        self.obem_text.setMaximumHeight(40)

        if self.coffee_id is not None:
            self.pushButton = QPushButton('Отредактировать')
            self.get_elem()
            self.pushButton.clicked.connect(self.get_editing_verdict)
        else:
            self.pushButton = QPushButton('Сохранить')
            self.pushButton.clicked.connect(self.get_adding_verdict)

        # Добавление виджетов на форму
        self.layout.addRow('Название', self.title)
        self.layout.addRow('Степень обжарки', self.objar_text)
        self.layout.addRow('Молотый/зерно', self.molzer_text)
        self.layout.addRow('Описание вкуса', self.opis_text)
        self.layout.addRow('Цена', self.cena_text)
        self.layout.addRow('Объём упаковки', self.obem_text)
        self.layout.addRow(self.pushButton)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def get_editing_verdict(self):
        return self.get_adding_verdict()

    def get_adding_verdict(self):
        self.title = self.title.toPlainText().strip()
        self.objar_text = self.objar_text.toPlainText().strip()
        self.molzer_text = self.molzer_text.toPlainText().strip()
        self.cena_text = self.cena_text.toPlainText().strip()
        self.opis_text = self.opis_text.toPlainText().strip()
        self.obem_text = self.obem_text.toPlainText().strip()


        if self.coffee_id is None:
            query = 'INSERT INTO coffee (name, roast_degree, ground_or_whole, flavor_description, price, package_size) VALUES (?, ?, ?, ?, ?, ?)'
            self.con.execute(query, (self.title, self.objar_text, self.molzer_text, self.cena_text, self.opis_text, self.obem_text))
        else:
            query = 'UPDATE coffee SET name = ?, roast_degree = ?, ground_or_whole = ?, flavor_description = ?, price = ?, package_size = ? WHERE id = ?'
            self.con.execute(query, (self.title, self.objar_text, self.molzer_text, self.cena_text, self.opis_text, self.obem_text, self.coffee_id))

        self.con.commit()
        self.parent().butclicked()
        self.close()
        return True

    def get_elem(self):
        query = 'SELECT name, roast_degree, ground_or_whole, flavor_description, price, package_size FROM coffee WHERE id = ?'
        res = self.con.execute(query, (self.coffee_id,)).fetchone()
        if res:
            self.title.setPlainText(res[0])
            self.objar_text.setPlainText(str(res[1]))
            self.molzer_text.setPlainText(str(res[2]))
            self.opis_text.setPlainText(res[3])
            self.cena_text.setPlainText(str(res[4]))
            self.obem_text.setPlainText(str(res[5]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = coffee()
    ex.show()
    sys.exit(app.exec())