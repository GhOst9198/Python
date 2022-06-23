from rsa import rsa
def cckukr():
    while True:
        clientKey = {}
        print('\nEnter valid client key generation parameters: \n')
        clientKey['p'] = int(input('p: '))
        clientKey['q'] = int(input('q: '))
        clientKey['e'] = int(input('e: '))
        ClientRSA = rsa(clientKey['p'], clientKey['q'], clientKey['e'])
        if (ClientRSA.f == 0):
            break
    return ClientRSA