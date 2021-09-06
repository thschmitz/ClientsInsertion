import sqlite3
import sys
import frmbanco
import frmedit
import resources_rc
from tkinter import *
from tkinter import ttk
from frmprincipal import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QDialog
from PyQt5.QtGui import QIcon

Nome = False
Endereco = False
Telefone = False

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent= None):
        super().__init__(parent)
        super().setupUi(self)
        self.setFixedSize(551, 514)
        self.btnEnviar.clicked.connect(self.envioBanco)
        self.btnConsultar.clicked.connect(self.onMostraBanco)
        self.btnEnviar.setIcon(QIcon(':/icon/save.png'))
        self.btnConsultar.setIcon(QIcon(':/icon/open.png'))
        self.setWindowTitle("InsercaoClientes")
        self.RdMensal.setChecked(True)

    def checagem(self):
        self.checado = False
        if self.leCliente.text() != "" and self.leEndereco.text() != "" and self.leTelefone.text() != "":
            self.checado = True

    def envioBanco(self):
        self.checagem()
        if self.checado:
            try:
                conexao = sqlite3.connect("bancoclientes.db")
                cursor = conexao.cursor()
                cursor.execute("INSERT INTO dadosclientes(Cliente, Endereco, Telefone) VALUES (:Cliente, :Endereco, :Telefone)",
                {"Cliente": self.leCliente.text(), "Endereco": self.leEndereco.text(), "Telefone": self.leTelefone.text()})
                conexao.commit()
                conexao.close()
                print("Dados inseridos com sucesso")
                self.limpar()
            except sqlite3.Error as erro:
                print("Erro ao inserir os dados:", erro)
                self.errorbox(f"Erro na insercao de clientes: {erro}")
        else:
            self.errorbox(f"Complete todas as informacoes!")

    def errorbox(self, mensagem):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(mensagem)
        msgBox.setWindowTitle("Erro")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()
    
    def limpar(self):
        self.leCliente.setText("")
        self.leEndereco.setText("")
        self.leTelefone.setText("")
        self.RdAnual.setChecked(False)
        self.RdMensal.setChecked(False)

    def onMostraBanco(self):
        frmBanco.show()
        banco = sqlite3.connect("bancoclientes.db")
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM dadosclientes")
        dados_lidos = cursor.fetchall()
        frmBanco.ui.tableWidget.setRowCount(len(dados_lidos))
        frmBanco.ui.tableWidget.setColumnCount(3)
        for i in range(0, len(dados_lidos)):
            for j in range(0, 3):
                frmBanco.ui.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        banco.close()


class FrmMostraBanco(QDialog):
    def __init__(self, parent=None):
        super(FrmMostraBanco, self).__init__(parent)
        self.ui = frmbanco.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.btnProcurar.clicked.connect(self.consulta)
        self.ui.btnEditar.clicked.connect(self.onMostraEdit)
        self.ui.btnEditar.clicked.connect(self.bancoConsulta)
        self.ui.tableWidget_2.setEnabled(True)
        self.setWindowTitle("BancoClientes")
        self.setFixedSize(594, 553)

    def bancoConsulta(self):
        banco = sqlite3.connect("bancoclientes.db")
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM dadosclientes")
        dados_lidos = cursor.fetchall()
        frmEdit.ui.tableWidget_3.setRowCount(len(dados_lidos))
        frmEdit.ui.tableWidget_3.setColumnCount(3)
        for i in range(0, len(dados_lidos)):
            for j in range(0, 3):
                frmEdit.ui.tableWidget_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        banco.close()

    def consulta(self):
        try:
            if self.ui.linePesquisa.text() != "":
                banco = sqlite3.connect("bancoclientes.db")
                cursor = banco.cursor()
                cursor.execute(f"SELECT * FROM dadosclientes WHERE Cliente LIKE '%{self.ui.linePesquisa.text()}%'")
                dados_lidos = cursor.fetchall()
                frmBanco.ui.tableWidget_2.setRowCount(len(dados_lidos))
                frmBanco.ui.tableWidget_2.setColumnCount(3)
                for i in range(0, len(dados_lidos)):
                    for j in range(0, 3):
                        frmBanco.ui.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
                        frmBanco.ui.tableWidget_2.setEnabled(True)
                banco.close()
            else:
                frmBanco.ui.tableWidget_2.clearContents()

        except sqlite3.Error as erro:
            print("Erro na pesquisa dos dados:", erro)
            self.errorbox(f"Erro na pesquisa de clientes: {erro}")

    def onMostraEdit(self):
        frmEdit.show()

class FrmMostraEdit(QDialog):
    def __init__(self, parent):
        super(FrmMostraEdit, self).__init__(parent)
        self.ui = frmedit.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("ConfigEdit")
        self.setFixedSize(576, 421)
        self.ui.btnAplicar.clicked.connect(self.aplicar)
        self.ui.btnCancelar.clicked.connect(self.cancelar)
        self.ui.btnProcurar.clicked.connect(self.bancoEdicao)
        self.ui.tableWidget_3.selectionModel().selectionChanged.connect(self.onSelecaoPressionada)
        self.ui.btnProcurar_2.clicked.connect(self.redefinir)

    def onSelecaoPressionada(self, selected):
        try:
            for i in selected.indexes():
                print("Linha: {}; Coluna: {}".format(i.row(), i.column()))
                self.ui.lineColocar.setText(self.ui.tableWidget_3.item(i.row(), i.column()).text())
                coordenadasRow = i.row()
                coordenadasColumn = i.column()
            if i.column() == 0:
                Nome = True
            elif i.column() == 1:
                Endereco = True
            elif i.column() == 2:
                Telefone = True
            return coordenadasRow
        except:
            pass

    def cancelar(self):
        self.ui.lineColocar.setText("")

    def aplicar(self):
        banco = sqlite3.connect("bancoclientes.db")
        cursor = banco.cursor()
        if Nome:
            cursor.execute(f"UPDATE dadosclientes SET Cliente={self.ui.lineColocar} WHERE {self.coordenadasRow}") 
            cursor.commit()
        banco.close()

    def bancoEdicao(self):
        try:
            if self.ui.linePesquisa_2.text() != "":
                banco = sqlite3.connect("bancoclientes.db")
                cursor = banco.cursor()
                cursor.execute(f"SELECT * FROM dadosclientes WHERE Cliente LIKE '%{self.ui.linePesquisa_2.text()}%'")
                dados_lidos = cursor.fetchall()
                frmEdit.ui.tableWidget_3.setRowCount(len(dados_lidos))
                frmEdit.ui.tableWidget_3.setColumnCount(3)
                for i in range(0, len(dados_lidos)):
                    for j in range(0, 3):
                        frmEdit.ui.tableWidget_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
                        frmEdit.ui.tableWidget_3.setEnabled(True)
                banco.close()

            else:
                frmEdit.ui.tableWidget_3.clearContents()
        except sqlite3.Error as erro:
            print("Erro na pesquisa dos dados:", erro)
            self.errorbox(f"Erro na pesquisa de clientes: {erro}")

    def redefinir(self):
        frmEdit.ui.tableWidget_3.clearContents()
        self.ui.linePesquisa_2.setText("")
        banco = sqlite3.connect("bancoclientes.db")
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM dadosclientes")
        dados_lidos = cursor.fetchall()
        frmEdit.ui.tableWidget_3.setRowCount(len(dados_lidos))
        frmEdit.ui.tableWidget_3.setColumnCount(3)
        for i in range(0, len(dados_lidos)):
            for j in range(0, 3):
                frmEdit.ui.tableWidget_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
                frmEdit.ui.tableWidget_3.setEnabled(True)
        banco.close()

if __name__ == "__main__":
    qt = QApplication(sys.argv)
    qt.setWindowIcon(QIcon(':/icon/database-icon.png'))

    MW = MainWindow()
    MW.show()

    frmBanco = FrmMostraBanco(MW)
    frmEdit = FrmMostraEdit(frmBanco)
    qt.exec_()