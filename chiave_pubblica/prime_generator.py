import miller_rabin as mr
from random import randrange

# function that applies Miller-Rabin test 10 times on the given n
def isPrime(n):
    rval = str(n)
    for i in range(10):
        result = mr.millerRabinTest(n)
        if result:
            rval += " is composite."
            return rval
    rval += " is prime"
    return rval

print("This script generates prime numbers using Miller-Rabin test.")
answ = ""
while answ != "n":
    print("Wanna generate a new prime? [y/n]")
    answ = input()
    if answ == "n":
        break
    n = randrange(1, 10**100, 2)
    print(isPrime(n))
