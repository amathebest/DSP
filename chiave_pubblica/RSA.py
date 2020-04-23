import binascii
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

    # keys creation
    pubkey = (e, n)
    privkey = (d, n)

    # plaintext creation, convertion to integer, cypher, decypher and reconversion
    plaintext = "Hello, World!"
    print("Plain text:", plaintext)
    message = int(binascii.hexlify(plaintext.encode()), 16)

    cyphertext = encryption(pubkey, message)

    decryptedtext = decryption(privkey, cyphertext)

    convertedtext = binascii.unhexlify(hex(decryptedtext)[2:]).decode()
    
    print("Decrypted text :", convertedtext)
    return


if __name__ == "__main__":
    main()
