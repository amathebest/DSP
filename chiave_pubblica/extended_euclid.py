# recursive function that computes the extended Euclid algorithm
def EuclidGCD(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        b_div_a, b_mod_a = divmod(b, a)
        mcd, x, y = EuclidGCD(b_mod_a, a)
        return (mcd, y - b_div_a * x, x)

def main():
    # input
    print("Insert a: ")
    a = int(input())
    print("Insert b: ")
    b = int(input())

    # computation
    mcd, x, y = EuclidGCD(a, b)

    # output
    print("MCD:", mcd, "x:", x, "y:", y)

    return

if __name__ == "__main__":
    main()
