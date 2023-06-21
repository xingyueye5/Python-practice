from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from prettytable import PrettyTable

from main_ui import Ui_MainWindow
from C_LL1 import *
from lex_analyse import Token
import sys,os

class MainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.codes=[]
        self.setupUi(self)
        self.actionupload_2.triggered.connect(self.upload)
        self.actionupload_yours.triggered.connect(self.uploadtax)
        self.pushButton_2.clicked.connect(self.lex)
        self.pushButton_3.clicked.connect(self.ll1)
        self.path='./ctax.txt'
        self.codestr=[]

    ##词法分析
    def lex(self):
        self.textBrowser.clear()
        token=Token()
        for code in self.codes:
            token.run(code, True)
            token.lineno += 1
        for line in token.results:
            self.textBrowser.append(line)
        for c in token.short_res:
            if c[1]=='void':
                self.codestr.append('void')
                self.codestr.append(' ')
            elif c[0]=='id':
                self.codestr.append('id')
            elif c[0]=='num':
                self.codestr.append('num')
            else:
                self.codestr.append(c[1])
        print(self.codestr)
        return

    ##文法分析
    def ll1(self):
        self.textBrowser.clear()
        Code, Vt, Vn, First, Follow, table1, table=C_LL1(self.codestr,self.path)

        self.printf('消除回溯递归后文法：')
        for line in Code:
            self.printf(line)
        for line in table:
            self.printf(str(line))
        self.printf('分析成功！！')


    def upload(self):
        fileName,fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(), "All Files(*);;Text Files(*.txt)")
        f = open(fileName, 'r', encoding='utf-8')
        self.textBrowser.clear()
        self.codes=[]
        for line in f:
            lines = line.strip()  # 读取每一行
            self.codes.append(lines.replace(" ", ""))
            self.textBrowser.append(lines)
        return

    def uploadtax(self):
        fileName,fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(), "All Files(*);;Text Files(*.txt)")
        self.path=fileName
        self.textBrowser.clear()
        f = open(fileName, 'r', encoding='utf-8')
        for line in f:
            self.textBrowser.append(line)
        self.textBrowser.append('\n自定义文法添加成功，请开始分析!')

    def printf(self, mes):
        self.textBrowser.append(mes)  # 在指定的区域显示提示信息
        self.cursot = self.textBrowser.textCursor()
        self.textBrowser.moveCursor(self.cursot.End)


if __name__=='__main__':

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())