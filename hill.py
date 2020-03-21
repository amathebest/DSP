import math
import numpy as np
from random import randrange
from numpy import average as avg

# alphabet dimension
ALPHA_DIM = 26

# function that takes a plaintext, a key and returns the cyphertext.
# each letter of the cyphertext is obtained by linear combination with plaintext and key:
# ci = ki1*p1 + ... + kim*pm mod 26
def encrypt(plaintext, key):
    cyphertext = []
    result = np.matmul(plaintext, key)
    for i in range(len(result)):
        cyphertext.append(result[i] % ALPHA_DIM)
    return cyphertext

# function that takes a cyphertext, a key and returns the corresponding plaintext.
def decrypt(cyphertext, keyinv):
    plaintext = []
    result = np.matmul(cyphertext, keyinv)
    for i in range(len(result)):
        plaintext.append(result[i] % ALPHA_DIM)
    return plaintext

# function that returns a key that is invertible mod ALPHA_DIM
def createKey(length):
    found = False
    # checking if the matrix is invertible
    while not found:
        key = []
        for i in range(length):
            row = []
            for j in range(length):
                row.append(randrange(ALPHA_DIM))
            key.append(row)
        if math.gcd(int(round(np.linalg.det(key), 0)), ALPHA_DIM) == 1:
            found = True
    return np.array(key)

# function that computes the multiplicative inverse of a given number.
# Used in the matrix inversion mod ALPHA_DIM
def computeMultiplicativeInverse(number):
    multiplicativeinverse = 0
    for i in range(ALPHA_DIM):
        if (number * i) % ALPHA_DIM == 1:
            multiplicativeinverse = i
            break
    return multiplicativeinverse

# function that computes the inversion of the key.
def invertMatrix(inputMat):
    invertedMat = np.zeros(inputMat.shape, dtype = int)
    for i in range(inputMat.shape[0]):
        for j in range(inputMat.shape[1]):
            redMatrix = np.delete(np.delete(inputMat, i, 0), j, 1)
            bji = (-1)**(i+j+2) * int(round(np.linalg.det(redMatrix), 0)) * computeMultiplicativeInverse(int(round(np.linalg.det(inputMat), 0) % ALPHA_DIM))
            invertedMat[j,i] = bji % ALPHA_DIM
    return invertedMat


def main():
    # computation variables
    mode = "ed"

    if mode == "a":
        print("todo")
    else:
        plaintext = "fox"
        p = []
        for i in range(len(plaintext)):
            p.append(ord(plaintext[i]) - 97)

        key = createKey(len(p))

        # reading the plaintext and applying the block encryption
        c = encrypt(p, key)

        invertedKey = invertMatrix(key)

        dec = decrypt(c, invertedKey)



        print("Plain: " + plaintext)
        for row in p:
            print(row)

        cyphertext = ""
        for elem in c:
            cyphertext += chr(elem + 97)
        print("Cypher: " + cyphertext)
        for row in c:
            print(row)

        print("Key:")
        for row in key:
            print(row)

        print("Key inversa:")
        for row in invertedKey:
            print(row)

        print("Decypher text")
        for row in dec:
            print(row)

    '''
    # attacking the cypher
    key = attack(cyphertext)
    print(key)
    # decrypting the text
    decrypted = decrypt(cyphertext, key)
    print(decrypted)
    '''

if __name__ == "__main__":
    main()
