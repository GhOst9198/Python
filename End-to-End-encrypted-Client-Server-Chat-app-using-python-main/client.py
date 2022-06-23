import socket
import threading
import string,random
import pickle
import hashlib

# created modules
# encrypt(): for encryption returns ciphertext, getCiphertext(): to get ciphertext string, rsa: RSA class
from rsa import encrypt, getCiphertext
from ckukr import cckukr
# encryption(): for aes encryption, keyGeneration(): for key generation
from encryption import encryption, keyGeneration

# Choosing Nickname
nickname = input("Choose your nickname: ")
clientRSA = cckukr()

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))
serverKey = {}
serverKey['n'] = int(client.recv(1024).decode())
serverKey['e'] = int(client.recv(1024).decode())
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        pt = input('')
        sk = ''
        sk += random.choice(string.ascii_letters)
        sk += random.choice(string.ascii_letters)
        keys = keyGeneration(sk)
        ciphterText = encryption(pt, keys)
        client.send(ciphterText.encode())
        encryptedSecretKey = encrypt(sk, serverKey['n'], serverKey['e'])
        data = pickle.dumps(encryptedSecretKey)
        client.send(data)

        digest = hashlib.sha256(pt.encode()).hexdigest()

        signature = encrypt(digest, clientRSA.n, clientRSA.prKey)
        n = int(clientRSA.n)
        e = int(clientRSA.pubKey)
        client.send(str(n).encode())
        client.send(str(e).encode())

        data = pickle.dumps(signature)
        client.send(data)
        break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
