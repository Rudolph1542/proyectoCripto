import os
import socket
from tkinter import filedialog

CHUNK_SIZE = 4096

soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
soc.connect(('127.0.0.1',65432))
print('Conectado')
username=input('Introduce tu nombre de usuario:')
password=input('introduce tu contraseña:')
usrInfo=username+'|'+password

soc.sendall(str(usrInfo).encode())
x=soc.recv(CHUNK_SIZE).decode()
if(x=='error1'):
    print('Error en autenticación-Usuario inexistente')
    soc.close()
elif(x=='error2'):
    print('Error en autenticación-Contraseña incorrecta')
    soc.close()
else:
    pathh=filedialog.askopenfilename(initialdir=os.getcwd())
    file=open(pathh,'rb')
    data=file.read(CHUNK_SIZE)
    soc.sendall(data)
    print('Se envió archivo')
    soc.close()