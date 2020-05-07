

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


    for node in og_nodes:
        print(node)

    return


# function that returns the decoded string given a prefix-free code and a binary string
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