import math
import numpy as np
from random import randrange
from numpy import average as avg

# alphabet dimension
ALPHA_DIM = 26

def convertStringToNumbers(input):
    convNumbers = []
    for i in range(len(input)):
        convNumbers.append(ord(input[i])-97)
    return convNumbers

def convertNumbersToString(input):
    convString = ""
    for i in range(len(input)):
        convString += chr(input[i]+97)
    return convString

# function that takes a plaintext, a key and returns the cyphertext.
# each letter of the cyphertext is obtained by linear combination with plaintext and key:
# ci = ki1*p1 + ... + kim*pm mod 26
def encrypt(plaintext, key):
    cyphertext = []
    for block in plaintext:
        cypherblock = []
        result = np.matmul(block, key)
        for i in range(len(result)):
            cypherblock.append(result[i] % ALPHA_DIM)
        cyphertext.append(cypherblock)
    return cyphertext

# function that takes a cyphertext, a key and returns the corresponding plaintext.
def decrypt(cyphertext, keyinv):
    plaintext = []
    for block in cyphertext:
        plainblock = []
        result = np.matmul(block, keyinv)
        for i in range(len(result)):
            plainblock.append(result[i] % ALPHA_DIM)
        plaintext.append(plainblock)
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
    # computation mode:
    # a = attack
    # ed = encryption/decryption
    mode = "a"

    if mode == "a":

        plaintext = "friday"
        cyphertext = "obxjlp"
        m = 3
        # key [3]:
        # 11 21 3
        # 21 0 8
        # 25 0 23

        p = convertStringToNumbers(plaintext)
        c = convertStringToNumbers(cyphertext)

        pstar = []

        for i in range(m):
            row = []


    else:
        plaintext = "friday"
        keylen = 3 # len(p)

        p = convertStringToNumbers(plaintext)
        for i in range(int(len(p)/keylen)):
            row = []
            for j in range(keylen):
                row.append(p[i*keylen+j])
            p.append(row)

        key = createKey(keylen)

        c = encrypt(p, key)

        invertedKey = invertMatrix(key)

        decrypted = decrypt(c, invertedKey)



        print("Plain: " + plaintext)
        for row in p:
            print(row)

        cyphertext = ""
        for block in c:
            for numb in block:
                cyphertext += chr(numb + 97)
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
        for row in decrypted:
            print(row)

        pdec = ""
        for block in decrypted:
            for numb in block:
                letter = chr(numb + 97)
                pdec += letter
        print(pdec)

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
