import prime_generator as pg
import extended_euclid as eu
import quick_exp as qe


def main():

    # generating p and q as big random primes
    exp = 100
    p = pg.generate_prime(exp)
    q = pg.generate_prime(exp)

    # n is equal to the product of p and q
    n = p * q
    phi_n = (p-1)*(q-1)

    # chosing e and calculating d = e^-1 mod phi_n
    e = 65537
    d = eu.EuclidGCD(e, phi_n)[1] + phi_n

    

    return


if __name__ == "__main__":
    main()
