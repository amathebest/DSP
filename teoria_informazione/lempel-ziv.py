




def encode():
    input_str = 'AAAABBCDEABCDABCAAABCDEEEEEECBBBBBBDDAAE'
    dict = {}

    # indexes that will read the string, end is always increased by one, when an undiscovered block is found start will be put to end
    start = 0
    end = 1

    progress = 0

    while True:
        if not len(input_str) > start+end-1:
            break
        sub_str = input_str[start:start + end]
        print(sub_str, start, end)
        if sub_str in dict:
            end += 1
        else:
            dict[sub_str] = progress
            start += end
            end = 1
            progress += 1

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
        encode()

    else:
        decode()

    return

if __name__ == "__main__":
    main()
