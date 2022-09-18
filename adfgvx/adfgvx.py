# part of our key, 6x6 grid
grid = [
    ['E', 'U', 'R', 'I', 'P', '8'],
    ['O', 'H', 'W', 'D', 'K', 'G'],
    ['2', 'N', '5', '0', '6', 'V'],
    ['Z', 'T', 'A', 'X', 'M', 'F'],
    ['7', 'Y', 'Q', '9', 'J', '4'],
    ['B', 'L', '3', 'C', '1', 'S']
]

# change these
keyword = 'SPONGE'
plaintext = 'THEQUICKBROWNFOXJUMPEDOVERTHE345679INSECTSIN2018'

# important letters
letters = ['A', 'D', 'F', 'G', 'V', 'X']

# dict formatted {'RC': 'char', ...}
dict = {}
for r in range(len(letters)):
    for c in range(len(letters)):
        dict[f'{letters[r]}{letters[c]}'] = grid[r][c]

# inverse of previous dict, formatted {'char': 'RC'}
dict_inv = {y:x for x,y in dict.items()}

# intermediate encryption, not sorted into columns yet
intermediate = ''.join(dict_inv[a] for a in plaintext)

# separeted into columns/bins
bins = {}
for i in range(len(intermediate)):
    bins[keyword[i%len(keyword)]] = bins.get(keyword[i%len(keyword)], '') + intermediate[i]

# sorts by bin
tups = sorted([(x, y) for x, y in bins.items()], key=lambda tup: tup[0])

# combines each bin and prints result
final = ''
for i in tups:
    final += i[1]

print(final)