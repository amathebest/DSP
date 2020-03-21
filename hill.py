import sys
import math
import numpy as np
from random import randrange
from numpy import average as avg

# alphabet dimension
ALPHA_DIM = 26

# function that takes a single letter of the plaintext, the corresponding letter of the key and
# returns the shifted letter
def shiftSingleLetter(pi, ki):
    plainidx_number = ord(pi) - 97
    keyidx_number = ord(ki) - 97
    cypheridx_number = ((plainidx_number + keyidx_number) % ALPHA_DIM) + 97
    return chr(cypheridx_number)


# function that takes a plaintext, a key and returns the cyphertext.
# each letter of the cyphertext is obtained by linear combination with plaintext and key:
# ci = ki1*p1 + ... + kim*pm mod 26
def encrypt(plaintext, key):
    cyphertext = []
    for i in range(len(plaintext)):
        acc = 0
        for elem in key[i]:
            acc += elem*plaintext[i]
        cyphertext.append(acc % ALPHA_DIM)
    return cyphertext

# function that takes a cyphertext, a key and returns the corresponding plaintext.
def decrypt(cyphertext, key):
    plaintext = []
    for i in range(len(cyphertext)):
        plaintext.append(shiftSingleLetter(cyphertext[i], key[i % len(key)]))
    plaintext = "".join(plaintext)
    return plaintext


def main():
    # computation variables
    mode = "ed"

    if mode == "a":
        print("todo")
    else:
        plaintext = "four"
        p = []
        for i in range(len(plaintext)):
            p.append(ord(plaintext[i]) - 97)
        found = False

        # checking if the matrix is invertible
        while not found:
            key = []
            for i in range(len(plaintext)):
                row = []
                for j in range(len(plaintext)):
                    row.append(randrange(ALPHA_DIM))
                key.append(row)
            if np.linalg.det(key) != 0:
                found = True

        # reading the plaintext and applying the block encryption
        c = encrypt(p, key)





        print("Plain: " + plaintext)
        for row in p:
            print(row)
        print("\n")

        cyphertext = ""
        for elem in c:
            cyphertext += chr(elem + 97)
        print("Cypher: " + cyphertext)
        for row in c:
            print(row)
        print("\n")

        for row in key:
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
