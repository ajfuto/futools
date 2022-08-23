'''
simple shift cipher encrypter/decrypter
by default, encrypts with all 26 possibilities

can also specify encryption vs decryption (and an optional shift value)

python3 shift.py helloworld e    ->  all 26 encryptions of helloworld
python3 shift.py mjqqtbtwqi d    ->  all 26 decryptions of mjqqtbtwqi
python3 shift.py helloworld e 5  ->  encrypts helloworld with shift 5
python3 shift.py mjqqtbtwqi d 5  ->  decrypts mjqqtbtwqi with shift 5
'''

import string
import sys

def main():
    plaintext = sys.argv[1]
    coeff = 1

    if len(sys.argv) > 2:
        coeff = -1 if sys.argv[2] == 'd' else 1

    if len(sys.argv) > 3:
        shift = int(sys.argv[3])
        print(shift_cipher(plaintext, coeff * (shift%26)))
    else:
        for i in range(0, 26):
            print("{:2d}: {:s}".format(i, shift_cipher(plaintext, coeff * i))) 

def shift_cipher(plain, shift):
    plain = plain.lower()
    shifted = string.ascii_lowercase[shift:] + string.ascii_lowercase[:shift]
    mapping_table = str.maketrans(string.ascii_lowercase, shifted)
    return plain.translate(mapping_table)

if __name__ == "__main__":
    if len(sys.argv) not in [2, 3, 4]:
        print("please run with the following syntax:")
        print("\tpython3 shift.py <plaintext> <optional: e/d <optional: shift>> ")
        print("\te encrypts, d decrypts. default behavior is encrypts with all 26 possibilities")
        print("\tex: python3 shift.py helloworld e")
        print("\tex: python3 shift.py mjqqtbtwqi d")
        print("\tex: python3 shift.py mjqqtbtwqi d 5")
        exit()
    main()