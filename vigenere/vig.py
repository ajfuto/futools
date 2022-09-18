#!/usr/bin/env python3

import math
import re
import functools

MIN_NGRAM_LENGTH = 3
MIN_DIFF_DISTANCE = 5

ENG_FREQ = {
    'a': .082, 'b': .015, 'c': .028, 'd': .043, 'e': .127, 'f': .022, 'g': .020, 
    'h': .061, 'i': .070, 'j': .002, 'k': .008, 'l': .040, 'm': .024, 'n': .067, 
    'o': .075, 'p': .019, 'q': .001, 'r': .060, 's': .063, 't': .091, 'u': .028, 
    'v': .010, 'w': .023, 'x': .001, 'y': .020, 'z': .001 
}

# finds ngrams of length MIN_NGRAM_LENGTH or more in text
# returns list of ngrams
# code adapted from cryptotool
def find_ngrams(text):
    ngrams = []
    for i in range(0, len(text) - MIN_NGRAM_LENGTH):
        for j in range(i+MIN_NGRAM_LENGTH, len(text) - MIN_NGRAM_LENGTH):
            subs = ""
            for k in range(0, len(text)-j):
                if text[i+k] != text[j+k]:
                    break
                subs = subs + text[i+k]

            if len(subs) >= MIN_NGRAM_LENGTH and subs not in ngrams:
                ngrams.append(subs)

    return ngrams

# takes input text and a list of its ngrams
# returns dict of {ngram: [idx1, idx2], ...}
# indices of where the ngram repeats
def ngrams_to_idx(text, ngrams):
    ret = {}
    for ng in ngrams:
        idxs_obj = re.finditer(pattern=ng, string=text)
        idxs = [idx.start() for idx in idxs_obj]
        ret[ng] = idxs
    return ret

# finds the differences of a dictionary of {ngram: [idx1, idx2], ...}
# returns dict of the diffs
def find_diffs(ngram_dict):
    diffs_dict = {}
    for k in ngram_dict.keys():
        nums = ngram_dict[k]
        for i in range(len(nums) - 1):
            diff = nums[i+1] - nums[i]
            if diff >= MIN_DIFF_DISTANCE:
                diffs_dict[k] = [diff] if k not in diffs_dict.keys() else diffs_dict[k] + [diff]
    return diffs_dict

# finds the gcd of a list of numbers
def gcd_list(list):
    return functools.reduce(math.gcd, list)

def all_gcds(list):
    gcds = []
    for i in range(len(list)):
        for j in range(len(list)):
            if i!=j:
                gcds.append(math.gcd(list[i], list[j]))
    gcds.sort()
    return gcds


def find_bins(text, num):
    bins = []
    for i in range(num):
        bins.append([])
    for i in range(len(text)):
        bins[i%num].append(text[i])
    return bins

def find_bins_freqs(bins):
    freqs_list = []
    for bin in bins:
        freq_dict = {}
        for i in range(26):
            freq_dict[chr(ord('a') + i)] = round((bin.count(chr(ord('a') + i))) / len(bin), 4)
        freqs_list.append(freq_dict)
    return freqs_list


def mic(f, g):
    m = sum(f[i] for i in range(26))
    n = sum(f[i] for i in range(26))
    return sum((f[i]*g[i])/(m*n) for i in range(26))

def mic_analysis(freqs):
    potential_key = []
    for fr in freqs:
        mics = []
        for i in range(26):
            shifted = list(fr.values())[i:] + list(fr.values())[:i]
            mics.append(mic(shifted, list(ENG_FREQ.values())))
        max_mic = max(mics)
        potential_key.append(chr(ord('a') + mics.index(max_mic)))
    return ''.join(str(c) for c in potential_key)

def vig_decrypt(cipher, key):
    plain = []
    for i in range(len(cipher)):
        c = ((ord(cipher[i])-ord('a')) - (ord(key[i%len(key)])-ord('a')))%26 + ord('a')
        plain.append(chr(c))
    return ''.join(c for c in plain)

cipher = input('enter cipher text (lowercase, no spaces, a-z): ')
print()

ngrams = find_ngrams(cipher)
print("ngrams:")
print(ngrams)
print()

ng_dict = ngrams_to_idx(cipher, ngrams)
print("ngram dict:")
print(ng_dict)
print()

diffs_dict = find_diffs(ng_dict)
print("diffs_dict:")
print(diffs_dict)
print()


diffs_nums = []
for a in diffs_dict.values():
    diffs_nums.extend(a)
print("diffs_nums:")
print(diffs_nums)
print()

poss_gcds = all_gcds(diffs_nums)
print('all possible GCDs:')
print(poss_gcds)
print()

keylen = gcd_list(diffs_nums)
print("calculated GCD:")
print(keylen)
keylen = int(input("make a better guess? "))
print()

repeated_idxs = {}
for k in diffs_dict.keys():
    repeated_idxs[k] = ng_dict[k]
print("repeated indicies")
print(repeated_idxs)
print()

bins = find_bins(cipher, keylen)
print("bins")
for b in bins: print(b)
print()

freqs = find_bins_freqs(bins)
print("bin frequencies")
for f in freqs: print(f)
print()

key_guess = mic_analysis(freqs)
print('key guess: ')
print(key_guess)
input = input('make a better guess? ')
key_guess = key_guess if input == '' else input
print()

plaintext = vig_decrypt(cipher, key_guess)
print('decrypted')
print(plaintext)