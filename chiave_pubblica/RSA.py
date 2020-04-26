import binascii
import pandas as pd
import datetime as dt
from random import randrange

# custom modules
import prime_generator as pg
import extended_euclid as eu
import quick_exp as qe


# function that executes the encryption on a message (expressed as integer)
# it accepts a tuple pubkey = (e, n) and a message m.
# it returns the encrypted message as m^e mod n
def encryption(pubkey, m):
    return qe.exp(m, pubkey[0], pubkey[1], False)

# function that executes the decryption of a message (expressed as integer)
# it accepts a tuple privkey = (d, n) and a cyphertext c.
# it returns the decrypted message m as c^d mod n
def decryption(privkey, c):
    return qe.exp(c, privkey[0], privkey[1], False)

# function that takes the job of generating p and q as big random numbers, compute phi of n,
# creation of e and d and returns n, the public key and the private key
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

    # keys creation
    pubkey = (e, n)
    privkey = (d, n)

    return n, pubkey, privkey

# function that executes an attack by assuming the private exponent d is known to the attacker
# it accepts e, d and n and returns the non-trivial factor of n found by the procedure
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
        # # checking if each subsequent element of the sequence is equal to -1 mod n
        for i in range(r):
            xi = qe.exp(x, 2**i*m, n, False)
            seq.append(xi)
            if xi == 1:
                break

        print(seq)
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

    for i in range(100):
        n, pubkey, privkey = setup(exp)


        initial_dt = dt.datetime.now()

        non_trivial_factor, iterations = decryptionexp(pubkey[0], privkey[0], n, True)

        ending_dt = dt.datetime.now()
        time = ending_dt - initial_dt

        row = {'iterations': iterations, 'time': time.microseconds}

        stats = stats.append(row, ignore_index = True)



    return

def main():
    exp = 100
    n, pubkey, privkey = setup(exp)

    # plaintext creation, convertion to integer, encryption, decryption and reconversion
    plaintext = "Hello, World!"
    print("Plain text:", plaintext)

    message = int(binascii.hexlify(plaintext.encode()), 16)

    cyphertext = encryption(pubkey, message)

    decyphertext = decryption(privkey, cyphertext)

    convertedtext = binascii.unhexlify(hex(decyphertext)[2:]).decode()

    print("Decrypted text :", convertedtext)

    # attack section
    non_trivial_factor = decryptionexp(pubkey[0], privkey[0], n, False)

    if non_trivial_factor == -1:
        print("Some error occurred.")
    else:
        print("n got factorized into", non_trivial_factor, "and", str(n/non_trivial_factor))

    # testing on 100 random RSA modules
    testing(exp)

    return


if __name__ == "__main__":
    main()
