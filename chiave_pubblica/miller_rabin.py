from random import randrange

# function that implements the Miller-Rabin test. It accepts
def millerRabinTest(n):
    # 2 and 3 are prime
    if n == 2 or n == 3:
        return False

    # even numbers are always composite
    if n % 2 == 0:
        return True

    # rewriting n-1=(2^r)*m
    m = n-1
    r = 0
    while m % 2 == 0:
        m //= 2
        r += 1
    x = randrange(2, n-1)

    # checking if the first element of the sequence is 1
    if pow(x, m, n) == 1:
        return False

    # checking if each subsequent element of the sequence is equal to -1 mod n
    for i in range(r):
        if pow(x, 2**i*m, n) == n-1:
            return False

    return True



def main():
    print("Insert a number n to test with Miller-Rabin:")
    n = int(input())

    result = millerRabinTest(n)

    if result:
        print(n, "is composite.")
    else:
        print(n, "is probably prime.")

if __name__ == "__main__":
    main()
