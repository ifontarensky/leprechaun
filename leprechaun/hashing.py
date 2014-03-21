#!/usr/bin/env python3

import hashlib

def hash_word(word, hash_object):
  """Hashes a given word using the specified "hash_object".

  Parameters:
    - word: The word to hash
    - hash_object: The hashing object used to hash the given word

  Returns:
    - Hexdigit representation of the hashed word

  """
  hash_object.update(word)
  return hash_object.hexdigest()
