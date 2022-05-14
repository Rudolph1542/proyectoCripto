import socket


CHUNK_SIZE = 4096

soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
soc.connect(('127.0.0.1',65432))
print('Conectado')
username=input('Introduce tu nombre de usuario:')
password=input('introduce tu contraseña:')
usrInfo=username+'|'+password

soc.sendall(str(usrInfo).encode())

if(soc.recv(CHUNK_SIZE).decode()=='error'):
    print('Error en autenticación')
    soc.close()
else:
    file=open('tosend.txt','rb')
    data=file.read(CHUNK_SIZE)
    soc.sendall(data)
    print('Se envió archivo')
    soc.close()