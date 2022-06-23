import socket
import threading
import pickle
import hashlib
# created modules
# decrypt(): rsa decryption, getCiphertext(): returns ciphertext as string, rsa: RSA class
from rsa import decrypt, rsa
# decryption(): aes decryption returns plaintext, keyGeneration(): aes key generation returns dict, formString(): string manipulation
from decryption import decryption, keyGeneration, formString


# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
def skukr():
    while True:
        serverKey = {}
        print('Enter valid server key generation parameters:\n ')
        serverKey['p'] = int(input('p: '))
        serverKey['q'] = int(input('q: '))
        serverKey['e'] = int(input('e: '))
        ServerRSA = rsa(serverKey['p'], serverKey['q'], serverKey['e'])
        if ServerRSA.f == 0:
            break
    return ServerRSA

serverRSA = skukr()

server.listen()
# Lists For Clients and Their Nicknames
clients = []
nicknames = []
# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            ciphterText = client.recv(1024).decode()
            encryptedSecretkey = pickle.loads(client.recv(1024))
            SecretKey = decrypt(encryptedSecretkey, serverRSA.n, serverRSA.prKey)
            SecretKeystr = formString(SecretKey)
            # aes decryption computation and key generation
            keys = keyGeneration(SecretKey)
            message = decryption(ciphterText, keys)
            print(message)
            clientKey = {}
            clientKey['n'] = int(client.recv().decode())
            clientKey['e'] = int(client.recv().decode())

            signature = pickle.loads(client.recv())
            digest = hashlib.sha256(message.encode()).hexdigest()

            verificationCode = decrypt(signature, clientKey['n'], clientKey['e'])

            # verifying signature
            if verificationCode == digest:
                broadcast(message.encode('ascii'))
            else:
                message = "Sorry message is tempered"
                broadcast(message.encode('ascii'))
            break
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast("{} joined!".format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(serverRSA.n)
        client.send(str(serverRSA.n).encode())
        client.send(str(serverRSA.pubKey).encode())
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()