import sys

class Node():
    xi = ""
    pi = 0
    ci = ""

    def __init__(self, xi, pi):
        self.xi = xi
        self.pi = pi
        pass

    def __str__(self):
        return "xi: " + self.xi + ", pi: " + str(self.pi) + ", ci: " + self.ci

    def append_encoding(self, symbol):
        self.ci = symbol + self.ci
        pass

# function that verifies whether a given code is prefix-free
def verify_code(codes):
    for key in codes:
        for key_to_check in codes:
            if key in key_to_check[:len(key)] and key != key_to_check:
                return False
    return True

# function that creates the code with optimal lenght for a given alphabet X and probability distribution p
def encode():
    distribution_path = "input/distribution.txt"
    with open(distribution_path, 'r') as d_file:
        values = d_file.read().split('\n')

    values = values[:-1] # this strips away the last empty line

    nodes = []
    # creating the nodes with the values from file
    for value in values:
        curr_xi, curr_pi = value.split(" ")[0], float(value.split(" ")[1])
        new_node = Node(curr_xi, curr_pi)
        nodes.append(new_node)

    og_nodes = nodes.copy()

    # looping until there is a single node left. on each loop the two minimum pi are selected and a
    # father node is created. meanwhile the code for each original node gets updated by appending a 0 or a 1
    while len(nodes) >= 2:
        # processing first node with minimum pi
        node_1 = min(nodes, key = lambda x: x.pi)
        if len(node_1.xi) > 1:
            for elem in node_1.xi:
                node_to_edit = [x for x in og_nodes if x.xi == elem][0]
                node_to_edit.append_encoding("0")
        node_1.append_encoding("0")
        nodes = [x for x in nodes if x.xi != node_1.xi]

        # processing second node with minimum pi
        node_2 = min(nodes, key = lambda x: x.pi)
        if len(node_2.xi) > 1:
            for elem in node_2.xi:
                node_to_edit = [x for x in og_nodes if x.xi == elem][0]
                node_to_edit.append_encoding("1")
        node_2.append_encoding("1")
        nodes = [x for x in nodes if x.xi != node_2.xi]

        new_node = Node(node_1.xi + node_2.xi, node_1.pi + node_2.pi)
        nodes.append(new_node)

    return og_nodes

# function that returns the decoded string given a prefix-free code and a binary string
def decode():
    code_path = "input/code.txt"
    with open(code_path, 'r') as c_file:
        values = c_file.read().split('\n')
    values = values[:-1] # this strips away the last empty line

    # storing the codes into a dictionary
    codes = {}
    for line in values:
        codes[line.split(" ")[1]] = line.split(" ")[0]

    # checking whether the given code is prefix-free. the code halts if the boolean returned is false
    is_prefix_free = verify_code(codes)
    if not is_prefix_free:
        print("The given coded is not prefix-free, so the string could not be decoded.")
        return -1

    if len(sys.argv) < 2:
        print("Usage: python huffman.py <insert_binary_string_to_decode_here>")
        return -1

    encoded_message = sys.argv[1] # input binary string
    decoded_message = ""
    i = 0
    j = 0

    # looping through the encoded message and parsing each encoded letter one at a time
    while i <= len(encoded_message):
        possible_chars = [value for key, value in codes.items() if encoded_message[j:i] in key[:i-j]]
        if len(possible_chars) == 1:
            decoded_message += possible_chars[0]
            j = i
        i += 1

    return decoded_message

def main():
    # variable that allows the user to choose the mode of the program:
    # e = encode mode
    # d = decode mode
    mode = "e"

    if mode == "e":
        nodes = encode()
        print("Letters given as input have been encoded:")
        for node in nodes:
            print(node)
    else:
        decoded_message = decode()
        if decoded_message != -1:
            print("The decoded message is: \n" + decoded_message)
        else:


    return

if __name__ == "__main__":
    main()
