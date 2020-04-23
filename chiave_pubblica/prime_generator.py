import miller_rabin as mr
from random import randrange

# function that applies Miller-Rabin test 10 times on the given n
def isPrime(n):
    for i in range(10):
        result = mr.millerRabinTest(n)
        if result:
            return False
    return True

# function that generates a prime number in the chosen order of magnitude
def generate_prime(exp):
    while True:
        n = randrange(1, 10**exp, 2)
        # making sure the number is of the chosen order of magnitude
        while len(str(n)) == exp:
            if isPrime(n):
                return n
            else:
                break

def main():
    print("This script generates prime numbers using Miller-Rabin test.")
    exp = 100
    print(generate_prime(exp))

    return

if __name__ == "__main__":
    main()
