import math
import numpy as np
from itertools import product
from scipy.special import binom
from random import randrange
from numpy import average as avg

# alphabet dimension
ALPHA_DIM = 26

# function that converts a string to an array of numbers (corresponding ASCII)
def convertStringToNumbers(input):
    convNumbers = []
    for i in range(len(input)):
        convNumbers.append(ord(input[i])-97)
    return convNumbers

# function that converts an array of numbers to a string (corresponding ASCII)
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

# function that executes a known-plaintext attack to the Hill cypher.
# it assumes the knowledge of some plaintext messages and the respective cyphertexts.
# it accepts as parameters a plaintext, a cyphertext and the key length and returns the key and an eventual error code
# if the attack couldn't be executed.
def attack(plaintext, cyphertext, keylen):
    p = convertStringToNumbers(plaintext)
    c = convertStringToNumbers(cyphertext)

    # splitting into chunks of keylen elements
    pchunks = [p[i:i+keylen] for i in range(0, len(p), keylen)]
    cchunks = [c[i:i+keylen] for i in range(0, len(c), keylen)]

    chosen_idx = -1

    # these two arrays will contain the combinations of the chunks, to try to find one that has the inverse
    pstar_mat = []
    cstar_mat = []

    for elem in list(product(pchunks, pchunks)):
        if elem[0] != elem[1]:
            pstar_mat.append(np.transpose(elem))

    for elem in list(product(cchunks, cchunks)):
        if elem[0] != elem[1]:
            cstar_mat.append(np.transpose(elem))
    for elem in pstar_mat:
        print(elem)
    for idx, elem in enumerate(pstar_mat):
        if math.gcd(int(round(np.linalg.det(elem), 0)), 26) == 1:
            chosen_idx = idx
            break

    if chosen_idx == -1:
        return 0 -1

    pstar = pstar_mat[chosen_idx]
    cstar = cstar_mat[chosen_idx]

    # inverting pstar
    pstar_inv = invertMatrix(pstar)

    # finding the key by computing the multiplication k = c* x p*^-1
    key = np.matmul(cstar, pstar_inv)
    modkey = np.zeros(key.shape, dtype = int)
    for i in range(len(key)):
        for j in range(len(key[i])):
            modkey[j][i] = key[j][i] % 26

    return modkey, 0

def main():
    # computation mode:
    # a = attack
    # ed = encryption/decryption
    mode = "a"

    if mode == "a":
        plaintext = "maybetomorrowok"
        cyphertext = "oggdusyuorqdaak"
        keylen = 3

        key, error = attack(plaintext, cyphertext, keylen)

        if error == -1:
            print("The attack couldn't be executed. No pstar inverse was found.")
        else:
            print("Key found: ")
            print(key)
    else:
        plaintext = "maybetomorrowok"
        keylen = 3 # len(p)

        p = convertStringToNumbers(plaintext)

        # splitting p in blocks
        pstar = []
        for i in range(int(len(p)/keylen)):
            row = []
            for j in range(keylen):
                row.append(p[i*keylen+j])
            pstar.append(row)

        key = createKey(keylen)
        c = encrypt(pstar, key)
        invertedKey = invertMatrix(key)
        decrypted = decrypt(c, invertedKey)

        # output section
        print("\nPlaintext:")
        print(plaintext)
        print("\nCyphertext:")
        cyphertext = ""
        for block in c:
            for numb in block:
                cyphertext += chr(numb + 97)
        print(cyphertext)
        print("\nDecrypted text:")
        decrypted_text = ""
        for block in decrypted:
            for numb in block:
                letter = chr(numb + 97)
                decrypted_text += letter
        print(decrypted_text)

    return

if __name__ == "__main__":
    main()
