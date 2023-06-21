import sys
import UI_Connect
import UI_Login
import UI_Client
import UI_Error_Connection
import UI_Error_Login
from CNLAB2_v2 import FTP
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
import os

IPADDRESS = "10.131.229.220"  # FTP服务器地址；如需测试，需要在自己的机器上使用Windows FTP Service架设服务器，并换成本机IP
PORT = 21
USER = "FTPUser"
PWD = "ftp"


class MainWindowClient(QMainWindow):             ##我们必须在这里拿到前面的ip
    def __init__(self, a_client):
        super().__init__()
        self.ui = UI_Client.Ui_MainWindow_Client()
        self.ui.setupUi(self)
        self.client = a_client
        self.fileName=''
        self.fileType=''
        # 加载控件逻辑
        self.ui.action_quit.triggered.connect(self.onquittriggered)
        self.ui.action_exit.triggered.connect(self.onexittriggered)
        # 文件操作开始 (ZYY)
        self.ui.action_upload.triggered.connect(self.onuploadtriggered)  # 上传操作逻辑(待完成)
        self.ui.action_download.triggered.connect(self.ondownloadtriggered)  # 下载操作逻辑(待完成)
        self.ui.action_delete.triggered.connect(self.ondeletetriggered)  # 删除操作逻辑(待完成)
        self.ui.lineEdit_cmd.returnPressed.connect(self.oncmdentered)
        return

    def onquittriggered(self):
        self.client.ftpserv.controlT.QUIT()
        self.close()
        self.client.widgetconnect.show()
        return

    def onexittriggered(self):
        self.client.ftpserv.controlT.QUIT()
        self.close()
        return

    def onuploadtriggered(self):  # 文件上传
        self.fileName,self.fileType = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(), "All Files(*);;Text Files(*.txt)")
        (name,suffix)=os.path.split(self.fileName)
        self.client.ftpserv.upload(self.client.ftpserv.ip,name+'\\',suffix)
        self.ui.lineEdit_path.setText(self.fileName)
        self.ui.listWidget_files.addItem(suffix)
        return

    def ondownloadtriggered(self):  # 文件下载
        temp=self.ui.listWidget_files.selectedItems()[0]
        item=temp.text()
        path=QtWidgets.QFileDialog.getExistingDirectory(self,"选取文件夹","C:/")
        self.client.ftpserv.download(self.client.ftpserv.ip,item,path)
        return

    def ondeletetriggered(self):  # 文件删除
        temp=self.ui.listWidget_files.selectedItems()[0]
        item=temp.text()
        self.client.ftpserv.controlT.delete(item)
        index=self.ui.listWidget_files.currentItem()
        self.ui.listWidget_files.takeItem(self.ui.listWidget_files.row(index))

    def oncmdentered(self):  # 控制台逻辑，目前只能原封不动地显示键盘输入
        flag=0
        cmd = self.ui.lineEdit_cmd.text().split()
        if len(cmd)==1:
            if cmd[0]=='PWD':
                self.client.ftpserv.controlT.PWD()
            elif cmd[0]=='QUIT':
                self.client.ftpserv.controlT.QUIT()
            elif cmd[0]=='ABOR':
                self.client.ftpserv.controlT.ABOR()
            else:self.ui.textBrowser_history.append('Invalid operation')
        elif len(cmd)==2:
            if cmd[0]=='CWD':
                self.client.ftpserv.controlT.CWD(cmd[1])
            elif cmd[0]=='SIZE':
                self.client.ftpserv.controlT.SIZE(cmd[1])
            elif cmd[0]=='RETR':
                self.client.ftpserv.controlT.RETR(cmd[1])
            elif cmd[0]=='STOR':
                self.client.ftpserv.controlT.STOR(cmd[1])
            else:self.ui.textBrowser_history.append('Invalid operation')
        elif len(cmd)==3:
            if cmd[0]=='NLST':
                self.client.ftpserv.controlT.NLST(cmd[1],cmd[2])
            elif cmd[0]=='LIST':
                self.client.ftpserv.controlT.LIST(cmd[1],cmd[2])
            else:self.ui.textBrowser_history.append('Invalid operation')
        else:self.ui.textBrowser_history.append('Invalid operation')
        return

    def showEvent(self, a_event):
        # 清除旧信息
        self.ui.lineEdit_path.clear()
        self.ui.listWidget_files.clear()
        self.ui.textBrowser_history.clear()  # 如需debug观察多次登录记录则注释掉
        self.ui.lineEdit_cmd.clear()
        # 显示新信息
        # 显示窗口
        a_event.accept()
        return


class WidgetLogin(QMainWindow):
    def __init__(self, a_client):
        super().__init__()
        self.ui = UI_Login.Ui_widget_login()
        self.ui.setupUi(self)
        self.client = a_client
        # 加载控件逻辑
        self.ui.lineEdit_user.returnPressed.connect(self.onloginclicked)
        self.ui.lineEdit_pwd.returnPressed.connect(self.onloginclicked)
        self.ui.pushButton_login.clicked.connect(self.onloginclicked)
        self.ui.pushButton_cancel.clicked.connect(self.oncancelclicked)
        return

    def onloginclicked(self):
        user = self.ui.lineEdit_user.text()
        pwd = self.ui.lineEdit_pwd.text()
        try:
            rescode = self.client.ftpserv.controlT.login(user, pwd)[0:3]
        except:  # 未连接至服务器就尝试登录
            self.setDisabled(True)
            self.client.widgeterrorlogin.error = 1
            self.client.widgeterrorlogin.show()
        else:
            if rescode == "230":  # 登录成功
                self.close()
                self.client.mainwindowclient.show()
            else:  # 登录失败
                self.setDisabled(True)
                self.client.widgeterrorlogin.error = 0
                self.client.widgeterrorlogin.show()
        return

    def oncancelclicked(self):
        self.client.ftpserv.controlT.QUIT()
        self.close()
        self.client.widgetconnect.show()
        return

    def showEvent(self, a_event):
        # 清除旧信息
        self.ui.lineEdit_user.clear()
        self.ui.lineEdit_pwd.clear()
        # 显示新信息
        self.ui.lineEdit_user.setText(str(USER))
        self.ui.lineEdit_pwd.setText(str(PWD))
        # 显示窗口
        a_event.accept()
        return


class WidgetConnect(QMainWindow):
    def __init__(self, a_client):
        super().__init__()
        self.ui = UI_Connect.Ui_widget_connect()
        self.ui.setupUi(self)
        self.client = a_client
        self.ipv4=''
        # 加载控件逻辑
        self.ui.lineEdit_ipv4.returnPressed.connect(self.onconnectclicked)
        self.ui.lineEdit_port.returnPressed.connect(self.onconnectclicked)
        self.ui.pushButton_connect.clicked.connect(self.onconnectclicked)
        self.ui.pushButton_exit.clicked.connect(self.onexitclicked)
        return

    def onconnectclicked(self):
        self.ipv4 = str(self.ui.lineEdit_ipv4.text())
        port = int(self.ui.lineEdit_port.text())
        self.client.ftpserv = FTP(self.ipv4, port, self.client.mainwindowclient)  # 创建实例
        try:
            self.client.ftpserv.controlT.connect(self.client.ftpserv.ip)
        except:
            self.setDisabled(True)
            self.client.widgeterrorconnection.show()
        else:
            self.close()
            self.client.widgetlogin.show()
        return

    def onexitclicked(self):
        self.close()
        return

    def showEvent(self, a_event):
        # 清除旧信息
        self.ui.lineEdit_ipv4.clear()
        self.ui.lineEdit_port.clear()
        # 显示新信息
        self.ui.lineEdit_ipv4.setText(str(IPADDRESS))
        self.ui.lineEdit_port.setText(str(PORT))
        # 显示窗口
        a_event.accept()
        return


class WidgetErrorConnection(QMainWindow):
    def __init__(self, a_client):
        super().__init__()
        self.ui = UI_Error_Connection.Ui_widget_errorconnection()
        self.ui.setupUi(self)
        self.client = a_client
        # 加载控件逻辑
        self.ui.pushButton_ok.clicked.connect(self.onokclicked)
        return

    def onokclicked(self):
        self.close()
        return

    def closeEvent(self, a_event):
        self.client.widgetconnect.setEnabled(True)
        a_event.accept()
        return


class WidgetErrorLogin(QMainWindow):
    def __init__(self, a_client):
        super().__init__()
        self.ui = UI_Error_Login.Ui_widget_errorlogin()
        self.ui.setupUi(self)
        self.client = a_client
        self.error = None
        # 加载控件逻辑
        self.ui.pushButton_ok.clicked.connect(self.onokclicked)
        return

    def onokclicked(self):
        self.close()
        return

    def showEvent(self, a_event):
        if self.error == 0:  # 登录失败
            self.ui.label_linefirst.setText("无法登录到服务器！")
            self.ui.label_linesecond.setText("请检查用户名或密码是否正确。")
        elif self.error == 1:  # 连接不存在
            self.ui.label_linefirst.setText("目的服务器不存在！")
            self.ui.label_linesecond.setText("请重新建立连接。")
        else:
            self.ui.label_linefirst.setText("登录失败！")
            self.ui.label_linesecond.setText("未定义的异常。")
        a_event.accept()
        return

    def closeEvent(self, a_event):
        self.client.widgetlogin.setEnabled(True)
        if self.error == 1:  # 连接不存在，回到连接界面
            self.client.widgetlogin.oncancelclicked()
        a_event.accept()
        return


class FTPClient(object):
    def __init__(self):
        self.ftpserv = None  # 由连接窗体创建
        self.widgetlogin = WidgetLogin(self)
        self.widgetconnect = WidgetConnect(self)
        self.mainwindowclient = MainWindowClient(self)
        self.widgeterrorconnection = WidgetErrorConnection(self)
        self.widgeterrorlogin = WidgetErrorLogin(self)
        self.widgetconnect.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = FTPClient()
    sys.exit(app.exec_())
