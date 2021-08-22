import sys
from FrmBanco import *
from FrmPrincipal import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import sqlite3

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent= None):
        super(Consulta).__init__(parent)
        super().setupUi(self)
        self.btnEnviar.clicked.connect(self.envioBanco)
        self.btnEnviar_2.clicked.connect(Consulta)

    def envioBanco(self):
        try:
            conexao = sqlite3.connect("basededados.db")
            cursor = conexao.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS clientes ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "nome TEXT,"
            "endereco TEXT,"
            "telefone NUMBER"
            ")")
            cursor.execute("INSERT INTO clientes(nome, endereco, telefone) VALUES (:nome, :endereco, :telefone)",
            {"nome": self.leCliente.text(), "endereco": self.leEndereco.text(), "telefone": self.leTelefone.text()})
            conexao.commit()
            conexao.close()
            print("Dados inseridos com sucesso")
            self.limpar()
        except sqlite3.Error as erro:
            print("Erro ao inserir os dados:", erro)
            self.errorbox(erro)

    def errorbox(self, erro):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(f"Erro na insercao dos dados: {erro}")
        msgBox.setWindowTitle("Erro")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def limpar(self):
        self.leCliente.setText("")
        self.leEndereco.setText("")
        self.leTelefone.setText("")
        self.RdAnual.setChecked(False)
        self.RdMensal.setChecked(False)
        self.RdUniversal.setChecked(False)

class Consulta(QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)

    def mostrar(self):
        C.show()

if __name__ == "__main__":
    qt = QApplication(sys.argv)
    C = Consulta()
    MW = MainWindow()
    MW.show()
    qt.exec_()