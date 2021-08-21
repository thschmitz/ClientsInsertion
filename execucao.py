# este eh o develop

import sys
from frm_cadastro import *
from InterfacePrincipal import *
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QMessageBox, QTableWidget, QTableWidgetItem, QWidget
import sqlite3
from tkinter import *

class FrmInterfaceSecundaria(QDialog):
    def __init__(self, *args, **argvs):
        super(FrmInterfaceSecundaria, self).__init__(*args, **argvs)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def chama_outra_tela(self):
        widget.show()
        banco = sqlite3.connect("clientes")
        cursor = banco.cursor()
        cursor.execute("select * from Clientes")
        dados_lidos = cursor.fetchall()
        self.ui.tableWidget.setRowCount(len(dados_lidos))
        self.ui.tableWidget.setColumnCount(3)

        for i in range(0, len(dados_lidos)):
            for j in range(0, 3):
                self.ui.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(dados_lidos[i][j]))
        
        banco.close()

class Login(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        self.btnEnviar.clicked.connect(self.inserir)
        self.btnEnviar_2.clicked.connect(FrmInterfaceSecundaria.chama_outra_tela)
        self.setWindowTitle("LoginClientes")

    def inserir(self):
        try:
            banco = sqlite3.connect("clientes")
            cursor = banco.cursor()
            cursor.execute("INSERT INTO clientes(nome, endereco, telefone) VALUES (:nome, :endereco, :telefone)",
            {"nome": self.leCliente.text(), "endereco": self.leEndereco.text(), "telefone": self.leTelefone.text()})
            banco.commit()
            banco.close()
            print("Dados inseridos com sucesso")
            self.limpar()

        except sqlite3.Error as erro:
            print("Erro ao inserir os dados:", erro)
            self.errorbox(erro)

    def limpar(self):
        self.leCliente.setText("")
        self.leEndereco.setText("")
        self.leTelefone.setText("")
        self.RdAnual.setChecked(False)
        self.RdMensal.setChecked(False)
        self.RdUniversal.setChecked(False)

    def errorbox(self, erro):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(f"Erro na insercao dos dados: {erro}")
        msgBox.setWindowTitle("Erro")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()
    
qt = QApplication(sys.argv)
Log = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(Log)
widget.setFixedHeight(514)
widget.setFixedWidth(551)
widget.show()
ST = FrmInterfaceSecundaria()
widget2 = QtWidgets.QStackedWidget()
widget2.addWidget(ST)
widget2.setFixedHeight(558)
widget2.setFixedWidth(848)
qt.exec_()