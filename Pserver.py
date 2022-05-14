import socket

from datetime import datetime

import now as now
from Crypto.Cipher import ChaCha20
from nacl.signing import SigningKey, VerifyKey

CHUNK_SIZE = 4096

soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
soc.bind(('127.0.0.1',65432))
soc.listen(1)
x,ad=soc.accept()
print(f'{ad} Conectado')
print()

#Autenticacion
users={
    'rudo1234':'asdfgh',
    'martha1':'hellothere',
    'arturo23':'werts',
    'winston':'bigbrother'
}
info=x.recv(CHUNK_SIZE)
usrInfo=info.decode().split('|')
usr=usrInfo[0]
pss=usrInfo[1]
logi=open('logins.txt','a',encoding='utf-8')
if(usr not in users.keys()):
    t=datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    msg=f'Inicio de sesión fallido-Usuario: {usr} no existe-{t}\n'
    print(msg)
    logi.write(msg)
    x.sendall(str('error1').encode())
    soc.close()
elif(pss!=users[usr]):
    t = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    msg = f'Inicio de sesión fallido-Contraseña incorrecta de {usr}-{t}\n'
    print(msg)
    logi.write(msg)
    x.sendall(str('error2').encode())
    soc.close()
else:
    t = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    msg = f'Inicio de sesión exitoso-Usuario: {usr}-{t}\n'
    print(msg)
    print()
    logi.write(msg)
    x.sendall(str('Error').encode())

    file1=open('cipheredsigned.txt', "wb")
    file2=open('deciphered.txt', "wb")

    data = x.recv(CHUNK_SIZE)

    #Cifrado

    key = b"9" * 32
    c = ChaCha20.new(key=key)
    cipData = c.encrypt(data)
    nonce=c.nonce
    print(cipData)
    print('Se ha cifrado el contenido del archivo')
    print()

    #Firma

    Skey=SigningKey.generate()
    sigData=Skey.sign(cipData)
    file1.write(sigData)
    print(sigData)
    print('Se ha firmado el contenido cifrado del archivo')
    print()

    #Verificacion de firma

    Vkey= VerifyKey(Skey.verify_key.encode())
    woutsData=Vkey.verify(sigData)
    print(woutsData)
    print('Se ha verificado la firma del contenido cifrado del archivo')
    print()

    #Descifrado

    c=ChaCha20.new(key=key,nonce=nonce)
    decData=c.decrypt(woutsData)
    file2.write(decData)
    print(decData)
    print('Se ha descifrado el contenido del archivo')
    print()


    soc.close()

