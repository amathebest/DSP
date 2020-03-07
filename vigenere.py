import math
import pandas as pd
from collections import Counter

# alphabet dimension
ALPHA_DIM = 26

# function that reads an input from given path and trims every new line and space.
# it returns the trimmed string as plaintext
def readAndTrimBlanks(path):
    with open(path, 'r') as infile:
        message = infile.read().replace("\n", "").replace(" ", "")
    return message

# function that takes a single letter of the plaintext, the corresponding letter of the key and
# returns the shifted letter
def shiftSingleLetter(pi, ki, direction):
    plainidx_number = ord(pi) - 97
    keyidx_number = ord(ki) - 97
    if direction == "forward":
        cypheridx_number = ((plainidx_number + keyidx_number) % ALPHA_DIM) + 97
    else:
        cypheridx_number = ((plainidx_number - keyidx_number) % ALPHA_DIM) + 97
    return chr(cypheridx_number)

# function that takes a plaintext, a key and returns the cyphertext.
# each element of the cyphertext is obtained by following this rule:
# ci = pi+ki mod len(k)
def encrypt(plaintext, key):
    cyphertext = []
    for i in range(len(plaintext)):
        cyphertext.append(shiftSingleLetter(plaintext[i], key[i % len(key)], "forward"))
    cyphertext = "".join(cyphertext)
    return cyphertext

# function that takes a cyphertext, a key and returns the corresponding plaintext.
def decrypt(cyphertext, key):
    plaintext = []
    for i in range(len(cyphertext)):
        plaintext.append(shiftSingleLetter(cyphertext[i], key[i % len(key)], "backwards"))
    plaintext = "".join(plaintext)
    return plaintext

# function that executes the Kaziski's Estimation to determine the key's length.
# it returns a
def kaziskiEstimation(cyphertext):
    kaziskiDistances = []
    dist_matrix = []
    count = Counter()
    # finding trigrams
    trigrams = []
    for i in range(len(cyphertext)):
        if i < len(cyphertext)-2:
            new_trigram = cyphertext[i]+cyphertext[i+1]+cyphertext[i+2]
            trigrams.append(new_trigram)
    # counting each occurrence
    for trigram in trigrams:
        count[trigram] += 1
    # finding the distances
    for elem in count:
        if count[elem] > 1:
            row = []
            row.append(elem)
            for i in range(len(cyphertext)):
                if i < len(cyphertext)-2:
                    if elem == cyphertext[i:i+3]:
                        row.append(i)
            dist_matrix.append(row)
    # saving the distances in the return matrix
    for elem in dist_matrix:
        for i in range(len(elem)-2):
            dist = elem[i+2] - elem[i+1]
            kaziskiDistances.append(dist)
    return kaziskiDistances

# function that implements an attack to the Vigenère cypher.
# it's composed by two main phases:
# 1. it tries to found the length of the key by looking at the recurrent characters in the plaintext
# 2. it then determines the single characters of the key by
def attack(cyphertext):
    distances = kaziskiEstimation(cyphertext)
    mcd = math.gcd(distances)
    print(mcd)

    return

def main():
    # computation variables
    input_path = "input/message.txt"
    key = "ambroisethomas"

    # reading the plaintext and applying the block encryption
    plaintext = readAndTrimBlanks(input_path)
    cyphertext = encrypt(plaintext, key)

    # attacking the cypher
    attack(cyphertext)

    # decrypting the text
    decrypted = decrypt(cyphertext, key)


if __name__ == "__main__":
    main()
