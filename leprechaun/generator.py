#!/usr/bin/env python3

import itertools
import string

def digit_generator(limit):
  """Generates a string of digits to be appened to another string.

  Parameters:
    - limit: The upper limit of the range of the length of digits to be
      generated.

  Yields:
    - A string of digits joined together.

  """
  digits = tuple(string.digits)
  for length in range(1, limit+1):
    for digit in itertools.product(digits, repeat=length):
      yield "".join(digit)

def word_generator(limit):
  """Generates a list of words up to length specified by 'limit'

  Parameters:
    - limit: The upper limit of the range of the word length.

  Yields:
    - A list of words up to length 'limit'

  """
  characters = tuple(string.printable[0:95])
  for length in range(1, limit+1):
    for char in itertools.product(characters, repeat=length):
      yield "".join(char)
