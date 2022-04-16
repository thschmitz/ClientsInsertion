import sqlite3
from sqlite3.dbapi2 import Cursor
import sys
import frmbanco
import frmplano
import frmedit
import frmexcluir
import resources_rc
from tkinter import *
from tkinter import ttk
from frmprincipal import *
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QDialog
from PyQt5.QtGui import QIcon
deletados = []




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
        frmBanco.ui.tableWidget.setColumnCount(4)
        for i in range(0, len(dados_lidos)):
            for j in range(0, 4):
                frmBanco.ui.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        banco.close()


class FrmMostraBanco(QDialog):
    def __init__(self, parent=None):
        super(FrmMostraBanco, self).__init__(parent)
        self.ui = frmbanco.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.btnProcurar.clicked.connect(self.consulta)
        self.ui.btnEditar.clicked.connect(self.onMostraEdit)
        self.ui.btnExcluir.clicked.connect(self.onMostraExcluir)
        self.ui.btnPlanos.clicked.connect(self.onMostraPlanos)
        self.ui.btnEditar.clicked.connect(self.bancoConsultaEdit)
        self.ui.btnExcluir.clicked.connect(self.bancoConsultaExcluir)
        self.ui.btnAtualizar.clicked.connect(self.atualizarBanco)
        self.ui.tableWidget_2.setEnabled(True)
        self.setWindowTitle("BancoClientes")
        self.setFixedSize(764, 551)

    def atualizarBanco(self):
        frmEdit.ui.tableWidget_3.clearContents()
        self.ui.linePesquisa.setText("")
        banco = sqlite3.connect("bancoclientes.db")
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM dadosclientes")
        dados_lidos = cursor.fetchall()
        frmBanco.ui.tableWidget.setRowCount(len(dados_lidos))
        frmBanco.ui.tableWidget.setColumnCount(4)
        for i in range(0, len(dados_lidos)):
            for j in range(0, 4):
                frmBanco.ui.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
                frmBanco.ui.tableWidget.setEnabled(True)
        banco.close()

    def bancoConsultaEdit(self):
        banco = sqlite3.connect("bancoclientes.db")
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM dadosclientes")
        dados_lidos = cursor.fetchall()
        frmEdit.ui.tableWidget_3.setRowCount(len(dados_lidos))
        frmEdit.ui.tableWidget_3.setColumnCount(4)
        for i in range(0, len(dados_lidos)):
            for j in range(0, 4):
                frmEdit.ui.tableWidget_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        banco.close()
    
    def bancoConsultaExcluir(self):
        banco = sqlite3.connect("bancoclientes.db")
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM dadosclientes")
        dados_lidos = cursor.fetchall()
        frmExcluir.ui.tableWidget_3.setRowCount(len(dados_lidos))
        frmExcluir.ui.tableWidget_3.setColumnCount(4)
        for i in range(0, len(dados_lidos)):
            for j in range(0, 4):
                frmExcluir.ui.tableWidget_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
        banco.close()

    def consulta(self):
        try:
            if self.ui.linePesquisa.text() != "":
                banco = sqlite3.connect("bancoclientes.db")
                cursor = banco.cursor()
                cursor.execute(f"SELECT * FROM dadosclientes WHERE Cliente LIKE '%{self.ui.linePesquisa.text()}%'")
                dados_lidos = cursor.fetchall()
                frmBanco.ui.tableWidget_2.setRowCount(len(dados_lidos))
                frmBanco.ui.tableWidget_2.setColumnCount(4)
                for i in range(0, len(dados_lidos)):
                    for j in range(0, 4):
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

    def onMostraExcluir(self):
        frmExcluir.show()

    def onMostraPlanos(self):
        fatias = [10, 15, 20]
        atividades = ["Universal", "Anual", "Mensal"]
        colunas = ["r", "m", "y"]
        plt.pie(fatias, labels = atividades, colors = colunas, startangle=90, shadow=True, explode=(0.1, 0, 0))
        plt.show()

    
class FrmMostraEdit(QDialog):
    def __init__(self, parent):
        super(FrmMostraEdit, self).__init__(parent)
        self.ui = frmedit.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("ConfigEdit")
        self.setFixedSize(680, 421)
        self.ui.btnProcurar.clicked.connect(self.bancoEdicao)
        self.ui.btnAplicar.clicked.connect(self.aplicar)
        self.ui.btnProcurar_2.clicked.connect(self.redefinir)
        self.ui.tableWidget_3.selectionModel().selectionChanged.connect(self.onSelecaoPressionada)

    def mensagemTela(self, mensagem):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(mensagem)
        msg.setWindowTitle("Erro edicao")
        msg.setStandardButtons(QMessageBox.Ok)

    def onSelecaoPressionada(self, selected):
        try:
            for i in selected.indexes():
                self.ui.lineColocar.setText(self.ui.tableWidget_3.item(i.row(), i.column()).text())
        except:
            pass

    def aplicar(self):
        try:
            i = self.ui.tableWidget_3.currentItem().row()
            j = self.ui.tableWidget_3.currentItem().column()
            print(i)
            Cliente = False
            Endereco = False
            Telefone = False

            if self.ui.lineColocar.text() == "":
                self.mensagemTela("Digite alguma informacao para a edicao do perfil do cliente")
            else:
                if j == 0:
                    self.mensagemTela("Nao pode editar o ID do cliente")
                elif j == 1:
                    Cliente = True
                elif j == 2:
                    Endereco = True
                elif j == 3:
                    Telefone = True
                banco = sqlite3.connect("bancoclientes.db")
                cursor = banco.cursor()
                cursor.execute("SELECT * FROM dadosclientes")
                dados_lidos = cursor.fetchall()
                id_pessoal = dados_lidos[i][0]
                print(id_pessoal)
                if Cliente:
                    cursor.execute(f"UPDATE dadosclientes SET Cliente= '{self.ui.lineColocar.text()}' WHERE ID= {id_pessoal}")
                    print("Registro atualizado")
                elif Endereco:
                    cursor.execute(f"UPDATE dadosclientes SET Endereco= '{self.ui.lineColocar.text()}' WHERE ID={id_pessoal}")
                    print("Registro atualizado")
                elif Telefone:
                    cursor.execute(f"UPDATE dadosclientes SET Telefone= '{self.ui.lineColocar.text()}' WHERE ID={id_pessoal}")
                    print("Registro atualizado")
                else:
                    print("SAIU")
                banco.commit()
                cursor.close()
                banco.close()
        except sqlite3.Error as erro:
            print(f"ERRO: {erro}")
            pass
        
    def bancoEdicao(self):
        try:
            if self.ui.linePesquisa_2.text() != "":
                banco = sqlite3.connect("bancoclientes.db")
                cursor = banco.cursor()
                cursor.execute(f"SELECT * FROM dadosclientes WHERE Cliente LIKE '%{self.ui.linePesquisa_2.text()}%'")
                dados_lidos = cursor.fetchall()
                frmEdit.ui.tableWidget_3.setRowCount(len(dados_lidos))
                frmEdit.ui.tableWidget_3.setColumnCount(4)
                for i in range(0, len(dados_lidos)):
                    for j in range(0, 4):
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
        frmEdit.ui.tableWidget_3.setColumnCount(4)
        for i in range(0, len(dados_lidos)):
            for j in range(0, 4):
                frmEdit.ui.tableWidget_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
                frmEdit.ui.tableWidget_3.setEnabled(True)
        banco.close()

class FrmMostraExcluir(QDialog):
    def __init__(self, parent):
        super(FrmMostraExcluir, self).__init__(parent)
        self.ui = frmexcluir.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("ConfigExcluir")
        self.setFixedSize(544, 422)
        self.ui.btnAplicar.clicked.connect(self.aplicar)
        self.ui.btnProcurar.clicked.connect(self.procura)
        self.ui.btnRedefinir.clicked.connect(self.redefinir)
        self.ui.tableWidget_3.selectionModel().selectionChanged.connect(self.excluir)

    def excluir(self, selected):
        banco = sqlite3.connect("bancoclientes.db")
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM dadosclientes")
        dados_lidos = cursor.fetchall()
        try:
            for ix in selected.indexes():
                self.ui.tableWidget_3.removeRow(ix.row())
                deletados.append(dados_lidos[ix.row()])
            
        except sqlite3.Error as erro:
            print("Erro que eu ainda nao entendi: {}".format(erro)) 
            pass          

    def aplicar(self):
        ret = QMessageBox.question(self, "MessageBox", "Tem certeza que deseja deletar?", QMessageBox.Yes | QMessageBox.No)

        if ret == QMessageBox.Yes:
            banco = sqlite3.connect("bancoclientes.db")
            cursor = banco.cursor()
            for i in deletados:
                print(i[0])
                cursor.execute(f"DELETE FROM dadosclientes WHERE ID={i[0]}")
            cursor.close()
            banco.commit()
            banco.close()
            
        else:
            banco = sqlite3.connect("bancoclientes.db")
            cursor = banco.cursor()
            cursor.execute("SELECT * FROM dadosclientes")
            dados_lidos = cursor.fetchall()
            frmExcluir.ui.tableWidget_3.setRowCount(len(dados_lidos))
            frmExcluir.ui.tableWidget_3.setColumnCount(4)
            for i in range(0, len(dados_lidos)):
                for j in range(0, 4):
                    frmExcluir.ui.tableWidget_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    def procura(self):
        try:
            if self.ui.linePesquisa_3.text() != "":
                banco = sqlite3.connect("bancoclientes.db")
                cursor = banco.cursor()
                cursor.execute(f"SELECT * FROM dadosclientes WHERE Cliente LIKE '%{self.ui.linePesquisa_3.text()}%'")
                dados_lidos = cursor.fetchall()
                frmExcluir.ui.tableWidget_3.setRowCount(len(dados_lidos))
                frmExcluir.ui.tableWidget_3.setColumnCount(4)
                for i in range(0, len(dados_lidos)):
                    for j in range(0, 4):
                        frmExcluir.ui.tableWidget_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
                        frmExcluir.ui.tableWidget_3.setEnabled(True)
                banco.close()
            else:
                frmExcluir.ui.tableWidget_3.clearContents()
        except sqlite3.Error as erro:
            print("Erro na pesquisa dos dados:", erro)
            self.errorbox(f"Erro na pesquisa de clientes: {erro}")

    def redefinir(self):
        frmEdit.ui.tableWidget_3.clearContents()
        self.ui.linePesquisa_3.setText("")
        banco = sqlite3.connect("bancoclientes.db")
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM dadosclientes")
        dados_lidos = cursor.fetchall()
        frmExcluir.ui.tableWidget_3.setRowCount(len(dados_lidos))
        frmExcluir.ui.tableWidget_3.setColumnCount(4)
        for i in range(0, len(dados_lidos)):
            for j in range(0, 4):
                frmExcluir.ui.tableWidget_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
                frmExcluir.ui.tableWidget_3.setEnabled(True)
        banco.close()

if __name__ == "__main__":
    qt = QApplication(sys.argv)
    qt.setWindowIcon(QIcon(':/icon/database-icon.png'))

    MW = MainWindow()
    MW.show()

    frmBanco = FrmMostraBanco(MW)
    frmEdit = FrmMostraEdit(frmBanco)
    frmExcluir = FrmMostraExcluir(frmBanco)
    qt.exec_()