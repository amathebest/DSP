import binascii
import numpy as np
import pandas as pd
import datetime as dt
from random import randrange, randint

# custom modules
import prime_generator as pg
import extended_euclid as eu
import quick_exp as qe


# function that executes the encryption on a message (expressed as integer)
# it accepts a tuple pubkey = (e, n) and a message m.
# it returns the encrypted message as m^e mod n.
def encryption(pubkey, m):
    return qe.exp(m, pubkey[0], pubkey[1], False)

# function that executes the decryption of a message (expressed as integer)
# it accepts a tuple privkey = (d, n) and a cyphertext c.
# it returns the decrypted message m as c^d mod n.
def decryption(privkey, c):
    return qe.exp(c, privkey[0], privkey[1], False)

# function that takes the job of generating p and q as big random numbers, compute phi of n,
# create e and d and returns the public key, the private key, n, p and q.
def setup(exp):
    # generating p and q as big random primes
    p = pg.generate_prime(exp)
    q = pg.generate_prime(exp)

    # n is equal to the product of p and q
    n = p * q
    phi_n = (p-1)*(q-1)

    # chosing e and calculating d = e^-1 mod phi_n
    e = 65537
    d = eu.EuclidGCD(e, phi_n)[1] + phi_n

    return (e, n), (d, n), n, p, q

# function that executes an attack by assuming the private exponent d is known to the attacker
# it accepts e, d and n and returns the non-trivial factor of n found by the procedure.
def decryptionexp(e, d, n, testing):
    counter = 0
    while True:
        counter += 1

        x = randrange(2, n-1)
        gcd = eu.EuclidGCD(x, n)[0]

        if gcd != 1:
            if testing:
                return gcd, counter
            else:
                return gcd

        # rewriting e*d - 1 as 2^r * m, with m odd
        m = e*d-1
        r = 0
        while m % 2 == 0:
            m //= 2
            r += 1

        seq = []

        if qe.exp(x, m, n, False) != 1:
            # checking if each subsequent element of the sequence is equal to -1 mod n
            for i in range(r):
                xi = qe.exp(x, 2**i*m, n, False)
                seq.append(xi)
                if xi == 1:
                    break

            if seq[-2] != 1 and seq[-2] != -1:
                if testing:
                    return eu.EuclidGCD(seq[-2]+1, n)[0], counter
                else:
                    return eu.EuclidGCD(seq[-2]+1, n)[0]
    return -1

# function that tests the attack on 100 different RSA modules and prints:
# - the average iteration taken by the algorithm to converge;
# - average time elapsed to converge;
# - variance of that time.
def testing(exp):
    stats = pd.DataFrame(columns = ['iterations', 'time'])
    print("Computing the attack 100 times...")

    for i in range(100):
        pubkey, privkey, n, p, q = setup(exp)

        initial_dt = dt.datetime.now()

        non_trivial_factor, iterations = decryptionexp(pubkey[0], privkey[0], n, True)

        ending_dt = dt.datetime.now()
        time = ending_dt - initial_dt

        row = {'iterations': iterations, 'time': time.microseconds}
        stats = stats.append(row, ignore_index = True)

    mean_iterations = np.mean(stats['iterations'])
    mean_time = np.mean(stats['time'])
    var_time = np.var(stats['time'])

    print("Statistic on the attack:")
    print("Mean iterations required to converge:", mean_iterations)
    print("Mean time required to converge:", mean_time, "[us]")
    print("Variance of the time required to converge:", var_time, "[us]")

    return

# function that tests 100 different random decryption using standard RSA decryption vs
# decryption by using CRT optimization.
# the function then prints the average time elapsed by the two approaches.
def testCRTOptimization(pubkey, privkey, p, q):
    print("Testing the decryption 100 times with and without CRT optimization...")
    # value arrays for cyphertexts, CRT values and time analysis
    n = p * q
    c_arr = []
    sp_arr = []
    sq_arr = []
    timesCRTNo = np.empty((0,1), int)
    timesCRTYes = np.array((0,1), int)


    # getting the multiplicative inverse of p mod q and q mod p
    invp = eu.EuclidGCD(p, q)[1]
    invq = eu.EuclidGCD(q, p)[1]

    # generating 100 random cyphertexts
    for i in range(100):
        c_arr.append(randint(1000, 9999))

    # first we precompute the values
    for i in range(100):
        sp_arr.append(qe.exp(c_arr[i], privkey[0], p, False))
        sq_arr.append(qe.exp(c_arr[i], privkey[0], q, False))

    # decryption
    for i in range(100):
        # no CRT
        initial_dt = dt.datetime.now()
        decyphertext = decryption(privkey, c_arr[i])
        ending_dt = dt.datetime.now()
        time = ending_dt - initial_dt
        timesCRTNo = np.append(timesCRTNo, time.microseconds)

        # with CRT
        initial_dt = dt.datetime.now()
        decyphertext = (sp_arr[i] * q * invq + sq_arr[i] * p * invp) % n
        ending_dt = dt.datetime.now()
        time = ending_dt - initial_dt
        timesCRTYes = np.append(timesCRTYes, time.microseconds)

    print("Average time elapsed without CRT optimization:", timesCRTNo.mean(),"[us]")
    print("Average time elapsed with CRT optimization:", timesCRTYes.mean(),"[us]")

    return

def main():
    mode = "t"
    exp = 100
    pubkey, privkey, n, p, q = setup(exp)

    if mode == "s":
        # standard mode
        plaintext = "Hello, World!"
        print("Plain text:", plaintext)
        message = int(binascii.hexlify(plaintext.encode()), 16)
        cyphertext = encryption(pubkey, message)
        decyphertext = decryption(privkey, cyphertext)
        convertedtext = binascii.unhexlify(hex(decyphertext)[2:]).decode()
        print("Decrypted text :", convertedtext)
    elif mode == "a":
        # attack mode
        non_trivial_factor = decryptionexp(pubkey[0], privkey[0], n, False)
        if non_trivial_factor == -1:
            print("Some error occurred.")
        else:
            print("n got factorized into", non_trivial_factor, "and", str(n/non_trivial_factor))
    elif mode == "t":
        # testing on 100 random RSA modules (esercizio 3.2)
        testing(exp)
    elif mode == "c":
        # decryption with or without CRT optimization
        testCRTOptimization(pubkey, privkey, p, q)

    return


if __name__ == "__main__":
    main()
