import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from numpy import average as avg
from statistics import mean
from collections import Counter

# alphabet dimension
ALPHA_DIM = 26
p_vec = [0.0812, 0.0149, 0.0271, 0.0432, 0.1202, 0.023, 0.0203, 0.0592, 0.0731, 0.01, 0.069, 0.0398, 0.0261, 0.0695, 0.0768, 0.0182, 0.011, 0.0602, 0.0628, 0.091, 0.0288, 0.0111, 0.0209, 0.017, 0.0211, 0.007]

# function that reads an input from given path and trims every new line and space.
# it returns the trimmed string as plaintext
def readAndTrimBlanks(path):
    with open(path, 'r', encoding = "utf-8") as infile:
        message = infile.read().replace("\n", "").replace(" ", "")
    return message.lower()

# function that takes a single letter of the plaintext, the corresponding letter of the key and
# returns the shifted letter
def shiftSingleLetter(pi, ki):
    plainidx_number = ord(pi) - 97
    keyidx_number = ord(ki) - 97
    cypheridx_number = ((plainidx_number + keyidx_number) % ALPHA_DIM) + 97
    return chr(cypheridx_number)

# function that takes a plaintext, a key and returns the cyphertext.
# each element of the cyphertext is obtained by following this rule:
# ci = pi+ki mod len(k)
def encrypt(plaintext, key):
    cyphertext = []
    for i in range(len(plaintext)):
        cyphertext.append(shiftSingleLetter(plaintext[i], key[i % len(key)]))
    cyphertext = "".join(cyphertext)
    return cyphertext

# function that takes a cyphertext, a key and returns the corresponding plaintext.
def decrypt(cyphertext, key):
    plaintext = []
    for i in range(len(cyphertext)):
        plaintext.append(shiftSingleLetter(cyphertext[i], key[i % len(key)]))
    plaintext = "".join(plaintext)
    return plaintext

# function that executes the Kaziski's Estimation to determine the key's length.
# it returns a collection of distances for every trigram found
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

# function that returns the factors of a given number
def factorsOfNumb(num):
    factors = []
    for i in range(1, num+1):
        if num % i == 0:
            factors.append(i)
    return factors

# function that implements the indexes of coincidence to find the correct length of the unknown key
def findCorrectLength(cyphertext, distances):
    # gathering all possible candidates
    all_factors = []
    for elem in distances:
        all_factors += factorsOfNumb(elem)
    lengthCandidates = Counter()
    for elem in all_factors:
        lengthCandidates[elem] += 1
    best_candidate = 0
    best_average_coincidence_idx = sys.float_info.min
    best_col_matrix = []
    # looping on candidates: for each candidate we split the cyphertext by columns and compute the coincidence indexes to find the best candidate
    for candidate in lengthCandidates:
        if candidate != 1 and candidate < 30:
            column_matrix = []
            for i in range(candidate):
                row = []
                column_matrix.append(row)
            i = 0
            while i < len(cyphertext):
                column_matrix[i % candidate].append(cyphertext[i])
                i += 1
            indexes = []
            for row in column_matrix:
                letter_count = Counter()
                for letter in row:
                    letter_count[letter] += 1
                row_coincidence_idx = 0
                for elem in letter_count:
                    row_coincidence_idx += (letter_count[elem]/len(row))*((letter_count[elem]-1)/len(row))
                indexes.append(row_coincidence_idx)
            avg_idxs = avg(indexes)
            # updating best values
            if avg_idxs > best_average_coincidence_idx:
                best_average_coincidence_idx = avg_idxs
                best_candidate = candidate
                best_col_matrix = column_matrix
    return best_candidate, best_col_matrix

# function that given a cyphertext organized by columns and the length of the key, returns the actual key
def findKey(column_cypher, m):
    key = ""
    # looping on the rows of the column cypher
    for i in range(m):
        row = column_cypher[i]
        indexes = []
        # looping through every possible shift of the letters that are in a row
        for j in range(26):
            shifted_row = []
            for elem in row:
                shifted_row.append(shiftSingleLetter(elem, chr(j+97)))
            letter_count = Counter()
            for elem in shifted_row:
                letter_count[elem] += 1
            # calculating the indexes and taking the letter that corresponds to the shift that gives the maximum index
            row_coincidence_idx = 0
            for elem in letter_count:
                row_coincidence_idx += (letter_count[elem]/len(row))*p_vec[ord(elem)-97]
            indexes.append(row_coincidence_idx)
        letter = np.argmax(indexes)
        key += chr(letter+97)

    return key

# function that implements an attack to the Vigenère cypher.
# it's composed by two main phases:
# - it tries to found the length of the key by looking at the recurrent characters in the plaintext
# - it determines each single character of the key
def attack(cyphertext):
    distances = kaziskiEstimation(cyphertext)
    key_length, column_cypher = findCorrectLength(cyphertext, distances)
    key = findKey(column_cypher, key_length)
    return key

# function that plots each letter with its specific frequency in the text
def plotOutput(plaintext):
    letter_count = Counter()
    for letter in plaintext:
        letter_count[letter] += 1
    letter_freq = Counter({k:v/len(plaintext) for k,v in letter_count.items()})
    plt.bar(letter_freq.keys(), letter_freq.values())
    plt.show()
    return

def mgramsDistribution(plaintext):
    counters = []
    meanfreqs = {}
    # looping from 2 to 4 (both included) to find the 2-grams, 3-grams and 4-grams and count them
    for m in range(2, 5):
        count = Counter()
        # finding mgrams
        mgrams = []
        for i in range(len(plaintext)):
            if m == 2:
                if i < len(plaintext)-2:
                    new_mgram = plaintext[i]+plaintext[i+1]
                    mgrams.append(new_mgram)
            elif m == 3:
                if i < len(plaintext)-3:
                    new_mgram = plaintext[i]+plaintext[i+1]+plaintext[i+2]
                    mgrams.append(new_mgram)
            else:
                if i < len(plaintext)-4:
                    new_mgram = plaintext[i]+plaintext[i+1]+plaintext[i+2]+plaintext[i+3]
                    mgrams.append(new_mgram)
        # counting the m-grams
        for mgram in mgrams:
            count[mgram] += 1
        counters.append(count)
    # converting in average frequencies
    for idx, counter in enumerate(counters):
        letter_freq = Counter({k:v/len(plaintext) for k,v in counter.items()})
        meanfreqs[str(idx+2) + "-grams"] = mean(letter_freq.values())

    for elem in meanfreqs:
        print(elem, meanfreqs.get(elem))
    return

# function that executes analysis compelling the exercise 3.1 on the Set 1 of homeworks
def analysis(plaintext):
    plotOutput(plaintext)
    mgramsDistribution(plaintext)

    return

def main():
    # computation modes:
    # at = attack
    # an = analysis
    # ed = encryption/decryption by specifying a key

    mode = "an"
    input_path = "input/plaintext.txt"

    if mode == "at":
        input_path = "input/cypher.txt"
        cyphertext = readAndTrimBlanks(input_path)
    elif mode == "an":
        analysis(readAndTrimBlanks(input_path))
        return
    else:
        key = "thereisalwayshope"
        # reading the plaintext and applying the block encryption
        plaintext = readAndTrimBlanks(input_path)
        cyphertext = encrypt(plaintext, key)
        print("Cypher text:")
        print(cyphertext)
        # attacking the cypher
    key = attack(cyphertext)
    # decrypting the text
    decrypted = decrypt(cyphertext, key)
    print("Decrypted text: ")
    print(decrypted)

    return

if __name__ == "__main__":
    main()
