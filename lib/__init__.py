#!/usr/bin/env python3

import hashlib
from itertools import product
from string import ascii_letters, digits

def letter_generator(limit):
  chars = tuple(ascii_letters + digits)
  for length in range(1, limit+1):
    for letters in product(chars, repeat=length):
      yield ''.join(letters)

if __name__ == '__main__':
  try:
    with open('md5.txt', 'w') as output:
      for combination in letter_generator(12):
        hashed_combination = \
          hashlib.md5(combination.encode('utf-8')).hexdigest()
        print(combination + ': ' + hashed_combination, file=output)
  except IOError as err:
    print('File error: ' + str(err))
