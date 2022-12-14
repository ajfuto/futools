'''
simple affine cipher encrypter/decrypter

python3 affine.py helloworld e        ->  all encryptions of helloworld
python3 affine.py zoffqcqbft d        ->  all decryptions of zoffqcqbft
python3 affine.py helloworld e 21 8   ->  encrypts helloworld with a=21, b=8
python3 affine.py zoffqcqbft d 21 8   ->  decrypts zoffqcqbft with a=21, b=8
'''

import sys

# 'a' must be relatively prime with the size of the alphabet (in this case, 26)
# all these numbers are relatively prime with 26
POSSIBLE_A = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

def main():
    text = sys.argv[1]

    # decrypt
    if sys.argv[2] == 'd':
        # not enough args, so do all possible
        if len(sys.argv) < 5:
            for a in POSSIBLE_A:
                for b in range(0, 26):
                    print('[a: {:2d}, b: {:2d}]: {:s}'.format(a, b, affine_decrypt(text, a, b)))
                    
        # else, we have enough args, so use the specified 'a' and 'b' values
        else:
            a = int(sys.argv[3])
            b = int(sys.argv[4])
            if a not in POSSIBLE_A:
                print('you chose a bad value for "a". please try again with one of the following:')
                print(POSSIBLE_A)
                exit()
            print('[a: {:2d}, b: {:2d}]: {:s}'.format(a, b, affine_decrypt(text, a, b)))

    # encrypt
    elif sys.argv[2] == 'e':
        # not enough args, so do all possible
        if len(sys.argv) < 5:
            for a in POSSIBLE_A:
                for b in range(0, 26):
                    print('[a: {:2d}, b: {:2d}]: {:s}'.format(a, b, affine_encrypt(text, a, b)))

        # else, we have enough args, so use the specified 'a' and 'b' values
        else:
            a = int(sys.argv[3])
            b = int(sys.argv[4])
            if a not in POSSIBLE_A:
                print('you chose a bad value for "a". please try again with one of the following:')
                print(POSSIBLE_A)
                exit()
            print('[a: {:2d}, b: {:2d}]: {:s}'.format(a, b, affine_encrypt(text, a, b)))

# modular inverse
def mod_inv(a, m):
    return pow(a, -1, m)

# encrypts plaintext with keys a and b
def affine_encrypt(plain, a, b):
    plain = plain.lower().replace(' ', '')
    
    # E(x) = (ax + b) % 26
    return ''.join([ chr(((a * (ord(c) - ord('a')) + b) % 26) + ord('a')) for c in plain])

# decrypts ciphertext with keys a and b
def affine_decrypt(cipher, a, b):
    cipher = cipher.lower()

    # D(x) = (a^-1 * (x - b)) % 26
    return ''.join([ chr(((mod_inv(a, 26) * (ord(c) - ord('a') - b)) % 26) + ord('a')) for c in cipher ]) 


if __name__ == "__main__":
    if len(sys.argv) not in [3, 5] and sys.argv[2] not in ['e', 'd']:
        print("please run with the following syntax:")
        print("\tpython3 affine.py <plaintext> <optional: e/d <optional: a> <optional: b> ")
        print("\te encrypts, d decrypts. default behavior is encrypts with all 26 possibilities")
        print("\tex: python3 affine.py helloworld e")
        print("\tex: python3 affine.py zoffqcqbft d")
        print("\tex: python3 affine.py helloworld e 21 8")
        print("\tex: python3 affine.py zoffqcqbft d 21 8")
        exit()
    main()