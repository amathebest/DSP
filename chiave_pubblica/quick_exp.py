import math
import datetime as dt
import numpy as np
#from decimal import Decimal

# function that computes the quick exponentiation of a**m mod n
def exp(a, m, n, time_analysis):
    d = 1
    c = 0
    binary_exp = np.binary_repr(m)

    # start of processing
    initial_dt = dt.datetime.now()

    # algorithm that computes the quick exponentiation
    for i in range(len(binary_exp)):
        d = (d*d) % n
        c = 2*c
        if int(binary_exp[i]) == 1:
            d = (d*a) % n
            c += 1

    ending_dt = dt.datetime.now()
    time = ending_dt - initial_dt
    if time_analysis:
        print("The computation took", time.microseconds, "us.")

    return d

def main():
    # input and setup
    print("Insert a: ")
    a = int(input())
    print("Insert m: ")
    m = int(input())
    print("Insert n: ")
    n = int(input())

    # put true if time elapsed is wanted as output
    time = False

    # computation
    d = exp(a, m, n, time)

    # output
    print(str(a) + "^" + str(m) + " mod " + str(n) + " = " + str(d))

    return

if __name__ == "__main__":
    main()
