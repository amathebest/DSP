# recursive function that computes the extended Euclid algorithm
# it returns 2 important values:
# - the GCD between a and b;
# - the multiplicative inverse of a mod b.
def EuclidGCD(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        b_div_a, b_mod_a = divmod(b, a)
        gcd, x, y = EuclidGCD(b_mod_a, a)
        return (gcd, y - b_div_a * x, x)

def main():
    # input
    print("Insert a: ")
    a = int(input())
    print("Insert b: ")
    b = int(input())

    # computation
    gcd, x, y = EuclidGCD(a, b)

    # output
    print("MCD:", gcd, "x:", x, "y:", y)

    return

if __name__ == "__main__":
    main()
