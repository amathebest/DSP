

class Node():
    id = 0
    xi = ""
    pi = 0

    def __init__(self, id, xi, pi):
        self.id = id
        self.xi = xi
        self.pi = pi
        pass

    def __str__(self):
        return "xi: " + self.xi + ", pi: " + str(self.pi)


class Edge():
    label = ""
    starting_node = 0
    ending_node = 0

    def __init__():
        pass


# function that creates the code with optimal lenght for a given alphabet X and probability distribution p
def encode():
    distribution_path = "input/distribution.txt"
    with open(distribution_path, 'r') as d_file:
        values = d_file.read().split('\n')

    values = values[:-1] # this strips away the last empty line

    nodes = []


    for idx, value in enumerate(values):
        curr_xi, curr_pi = value.split(" ")[0], value.split(" ")[1]
        new_node = Node(idx, curr_xi, curr_pi)
        nodes.append(new_node)



    for node in nodes:
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
