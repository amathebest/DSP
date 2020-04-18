from random import randint

# function that accepts an int dim and returns a pseudo-random permutation of dim elements
def generate_permutation(dim):
    arr = []
    i = 0

    while i < dim:
        gen = randint(0, dim-1)
        if gen not in arr:
            arr.append(gen)
            i += 1

    return arr

def main():
    perm = generate_permutation(100)
    print(perm)

if __name__ == "__main__":
    main()
