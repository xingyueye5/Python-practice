import os
import re
import socket
import time


IPADDRESS = "10.131.229.220"  # 默认FTP服务器地址，校园网环境下自机架设服务器的地址是动态的，每次连接校园网都会变更
PORT = 21
USER = 'ZYY'
PWD = '3046666'


class FTP(object):
    # ip = None  # 可省略

    def __init__(self, ip=IPADDRESS, port=PORT, mainwindowclient=None):  ##用自己的IPV4连接，然后后面的connect都是host的ip
        self.controlT = self.controlTube(port, mainwindowclient)
        self.ip = ip

    class controlTube(object):
        def __init__(self, port, mainwindowclient=None):
            self.control = socket.socket()  # 待添加参数
            self.port = port
            self.mainwindowclient = mainwindowclient  # 主窗体

        def response(self):
            data_buff = [self.control.recv(1024).decode()]
            self.control.setblocking(False)    # 非阻塞模式
            while True:
                try:
                    time.sleep(0.0001)
                    res = self.control.recv(1024).decode()
                    if res == '':
                        break
                    else:
                        data_buff.append(res)
                except BlockingIOError:
                    break
            self.control.setblocking(True)  # 阻塞模式
            for i in data_buff:
                print(i)
                if self.mainwindowclient is not None:  # 如果存在UI，则输出结果到UI控制台
                    self.mainwindowclient.ui.textBrowser_history.append(i)
            return data_buff[0]

        def connect(self, ip):
            self.control.connect((ip, self.port))
            return self.response()

        def delete(self,filename):
            self.control.send(("DELE "+filename+"\r\n").encode())
            return self.response()

        def login(self, user, pas):
            self.control.send(("USER " + user + "\r\n").encode("utf-8"))
            self.response()
            self.control.send(("PASS " + pas + "\r\n").encode("utf_8"))
            return self.response()  # 返回登录结果

        def PWD(self):  ##本质是调用已经写好的socket函数
            self.control.send("PWD\r\n".encode())
            return self.response()

        def CWD(self, path):
            self.control.send(("CWD " + path + "\r\n").encode())
            return self.response()

        def SIZE(self, filename):
            self.control.send(("SIZE " + filename + "\r\n").encode())
            size = self.response()
            size1 = int(re.findall("\d+", size)[1])
            return size1

        def RETR(self, filename):
            # 不可单独调用
            self.control.send(("RETR " + filename + "\r\n").encode())
            return self.response()

        def PASV1(self):   ##得到host发回的新端口号,然后client主动与host端口相连
            self.control.send("PASV\r\n".encode())
            res = self.response()
            res = re.findall("\d+", res)
            print(res)
            port_data = int(res[5]) * 256 + int(res[6])
            return port_data

        def PASV2(self):   ##只要response回复码就行
            self.control.send("PASV\r\n".encode())
            return self.response()

        def STOR(self, filename):
            self.control.send(("STOR " + filename + "\r\n").encode())
            return self.response()

        def QUIT(self):
            self.control.send(("QUIT\r\n").encode())
            return self.response()

        def REST(self, offset):
            self.control.send(("REST " + str(offset) + "\r\n").encode())
            return self.response()

        def ABOR(self):
            self.control.send(("ABOR\r\n").encode())
            return self.response()

        def NLST(self, ip, path):
            newport = self.PASV1()
            dataT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataT.connect((ip, newport))
            self.control.send(("NLST " + path + "\r\n").encode())
            res = dataT.recv(1024 * 5).decode()
            self.mainwindowclient.ui.textBrowser_history.append(res)
            print(res)
            dataT.close()
            self.PASV2()
            return res

        def LIST(self, ip, fileorpath):
            newport = self.PASV1()
            dataT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataT.connect((ip, newport))
            self.control.send(("LIST " + fileorpath + "\r\n").encode())
            self.response()
            res = dataT.recv(1024 * 5).decode()
            self.mainwindowclient.ui.textBrowser_history.append(res)
            print(res)
            return res

    def download(self, ip, filename, localpath):
        newport = self.controlT.PASV1()
        dataT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataT.connect((ip, newport))
        size = self.controlT.SIZE(filename)
        # Check whether files exist locally and size is less than download size
        if os.path.exists(localpath + r'\\' + filename) and os.path.getsize(localpath + r'\\' + filename) < size:
            # Breakpoint resume
            self.controlT.REST(os.path.getsize(localpath+ r'\\' + filename))
            self.controlT.RETR(filename)
            stream = open(localpath + r'\\' + filename, "ab")
            # Add content
            bitstream = b''
            while len(bitstream) < size - os.path.getsize(localpath + r'\\' + filename):
                bitstream += dataT.recv(size - os.path.getsize(localpath + r'\\' + filename) - len(bitstream))
            stream.write(bitstream)
            stream.close()
            dataT.close()
        else:
            # Normal download
            self.controlT.RETR(filename)
            # Create a new file
            stream = open(localpath + r'\\' + filename, 'wb+')
            # Write content
            bitstream = b''
            while len(bitstream) < size:
                bitstream += dataT.recv(size - len(bitstream))
            stream.write(bitstream)
            stream.close()
            dataT.close()
        self.controlT.PASV2()

    def upload(self, ip, path,filename):
        newport = self.controlT.PASV1()
        dataT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataT.connect((ip, newport))
        self.controlT.STOR(filename)
        stream = open(path+filename, "rb+")
        stats = os.stat(path+filename)
        size = stats.st_size
        sent_size = 0
        stream.seek(sent_size)
        while sent_size < size:
            dataslice = stream.read(512)
            dataT.sendall(dataslice)
            sent_size += len(dataslice)
        stream.close()
        dataT.close()
        self.controlT.PASV2()


if __name__ == '__main__':
    FTPCLIENT = FTP(IPADDRESS, PORT)
    FTPCLIENT.controlT.connect(FTPCLIENT.ip)
    FTPCLIENT.controlT.login(USER, PWD)
    FTPCLIENT.upload(FTPCLIENT.ip,'D:/Desktop/','RMA.txt')
    FTPCLIENT.download(FTPCLIENT.ip,'test.txt','D:/Desktop')
    FTPCLIENT.controlT.LIST(FTPCLIENT.ip, "/")
    #time.sleep(2)
    #FTPCLIENT.controlT.LIST(FTPCLIENT.ip, "/")
