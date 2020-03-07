

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
    return plaintext

def main():
    # computation variables
    input_path = "input/message.txt"
    key = "ambroisethomas"

    plaintext = readAndTrimBlanks(input_path)
    cyphertext = encrypt(plaintext, key)
    print(cyphertext)

if __name__ == "__main__":
    main()
