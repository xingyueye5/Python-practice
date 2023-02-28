from unrar import rarfile
import zipfile
import os
import threading
import queue


CipherPath='D:/Desktop/Code Blog/github_project/Python-practice/cipherbook/cipher'
RarPath='D:/Desktop/b.rar'
destPath='D:/Desktop'


def decipher(key,path,destpath):
    try:
        fp=rarfile.RarFile(path,pwd=key)
        fp.extractall(path=destpath,pwd=key)
        print('Success! ====>' + key)
        fp.close()
        return
    except:
        return


if __name__=='__main__':
    cipherList = os.listdir(CipherPath)  ##os.listdir列出文件夹下所有文件
    #q = queue.Queue()
    for file in cipherList:
        f = open(os.path.join(CipherPath, file))

        for key in f:
            print(' ',end='')
            #q.put(key.rstrip())
            key=key.rstrip()
            th = threading.Thread(target=decipher, args=(key,RarPath,destPath))
            th.start()
            #decipher(key,RarPath,destPath)
        print("Here finished {} cipher book".format(file))
        f.close()