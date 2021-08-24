import sys
from FrmPrincipal import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QDialog
from PyQt5.QtGui import QIcon
import sqlite3
import FrmBanco
import resources_rc

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent= None):
        super().__init__(parent)
        super().setupUi(self)
        self.btnEnviar.clicked.connect(self.envioBanco)
        self.btnEnviar_2.clicked.connect(self.onMostraBanco)
        self.btnEnviar.setIcon(QIcon(':/icon/save.png'))
        self.btnEnviar_2.setIcon(QIcon(':/icon/open.png'))

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

    def onMostraBanco(self):
        FrmBanco.show()

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

class FrmMostraBanco(QDialog):
    def __init__(self, parent=None):
        super(FrmMostraBanco, self).__init__(parent)
        self.ui = FrmBanco.Ui_Dialog()
        self.ui.setupUi(self)

if __name__ == "__main__":
    qt = QApplication(sys.argv)
    qt.setWindowIcon(QIcon(':/icon/database-icon.png'))

    MW = MainWindow()
    MW.show()

    FrmBanco = FrmMostraBanco(MW)

    qt.exec_()