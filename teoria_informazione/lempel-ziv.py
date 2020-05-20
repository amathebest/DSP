

def encode():
    code_path = "input/lz-input.txt"
    with open(code_path, 'r') as input_file:
        infile = input_file.read().replace("\n", "")
    print(infile)
    # this variable will contain the dictionary entries that will be produced as the input file is parsed block by block
    dict = {}

    # indexes that will read the string, end is always increased by one, when an undiscovered block is found start will be put to end
    start = 0
    end = 1

    while True:
        if not len(infile) > start+end-1:
            break

        block = infile[start:start+end]

        if block in dict:
            end += 1
        else:
            dict[block] = bin(len(dict))
            start += end
            end = 1

    print(dict)
    return



def decode():

    return









def main():
    # variable that allows the user to choose the mode of the program:
    # e = encode mode
    # d = decode mode
    mode = "e"

    if mode == "e":
        #encode()
        compressed = compress("AAAABBCDEABCDABCAAABCDEEEEEECBBBBBBDDAAE")
        print(compressed)

    else:
        decode()

    return

if __name__ == "__main__":
    main()
