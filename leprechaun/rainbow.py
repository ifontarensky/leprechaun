#!/usr/bin/env python3

import sqlite3

from .db import DB

def _hash_wordlist(wordlist, hashing_algorithm):
  """Hashes each of the words in the wordlist and yields the digests for each
  word.

  Parameters:
    - wordlist: The wordlist which we'll be hashing.
    - hashing_obj: The hashlib hashing algorithm which we'll be passing to the
      appropriate function to actually hash the word.

  Yields:
    - Hexadecimal digest of the given word.

  """
  for word in wordlist:
    # Create a copy of the hashing algorithm so the digest doesn't become
    # corrupted.
    hashing_obj = hashing_algorithm.copy()
    hashing_obj.update(word.encode())

    return_string = hashing_obj.hexdigest() + ":" + word
    yield return_string

def split_wordlist(wordlist, split):
  """Splits a wordlist into multiple different files, depending on the "split"
  parameter.

  Parameters:
    - wordlist: The original wordlist which will be split up.
    - split: The amount of times to split up the wordlist.

  """
  if split < 2: # No sense in splitting a file into one part
    return
  else:
    file_name = wordlist.split(".")[0] # We'll need this for later
    
    with open(wordlist, encoding="utf-8") as f:
      # Create a list of pointers to all of the new "split files", for easy
      # access.
      files = [
        open(file_name + "_" + str(i) + ".txt", "w", encoding="utf-8") for i in
          range(split)
      ]

      index = 0 # This determines which "split file" we're writing the line to
      for line in f:
        line = line.strip()
        print(line, file=files[index])
        
        index = (index + 1) % split

      # Now to clean up the mess!
      for g in files:
        g.close()

def create_rainbow_table(
  wordlist, hashing_algorithm, output, use_database=False):
  """Creates the rainbow table from the given plaintext wordlist.

  Parameters:
    - wordlist: The plaintext wordlist to hash.
    - hashing_algorithm: The algorithm to use when hashing the wordlist.
    - output: The name of the output file.
    - db: Flag whether the output is an SQLite DB or not (default=False).

  """
  # Create the database, if necessary.
  if use_database:
    db_file = output + ".db"
    database = DB(db_file)
    database.create_table()
  else:
    # Otherwise, create the plaintext file.
    txt_file = open(output + ".txt", "a")

  # Now actually hash the words in the wordlist.
  try:
    with open(wordlist, "r", encoding="utf-8") as wl:
      for entry in _hash_wordlist(wl, hashing_algorithm):
        if use_database:
          entries = entry.split(":")
          database.save_pair(entries[0], entries[1])
        else:
          txt_file.write(entry)
      txt_file.close()
  except IOError as err:
    print("File error: " + str(err))
