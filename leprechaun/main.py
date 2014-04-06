#!/usr/bin/env python3

import argparse
import sqlite3

import db
import generator
import hashlib

# Create command line arguments
parser = argparse.ArgumentParser(prog="leprechaun")
parser.add_argument("-n", "--number", type=int, default=0,
  help="Number of integers to append to end of password string (default=0)")

group_wordlist = parser.add_argument_group("wordlist arguments")
group_wordlist.add_argument("-w", "--wordlist", default="data/wordlist.txt",
  help="The list of words to hash (default=included list)")
group_wordlist.add_argument("-g", "--generate-wordlist", action="store_true",
  help="Generate a wordlist dynamically instead of using a prebuilt one")
group_wordlist.add_argument("-l", "--word-length", type=int, default=8,
  help="Maximum word length for generated wordlist")

group_output = parser.add_argument_group("output arguments")
group_output.add_argument("-o", "--output", default="rainbow",
  help="The name of the output file (default=rainbow)")
group_output.add_argument("-t", "--use-textfile", action="store_true",
  help="Save output to a plaintext file instead of sqlite database")

group_hashing = parser.add_argument_group("hashing arguments")
group_hashing.add_argument("-m", "--md5", action="store_true",
  help="Generate MD5 hashes of given passwords (default)")
group_hashing.add_argument("-s", "--sha1", action="store_true",
  help="Generate SHA1 hashes of given passwords")
group_hashing.add_argument("-s2", "--sha256", action="store_true",
  help="Generate SHA256 hashes of given passwords")
group_hashing.add_argument("-s5", "--sha512", action="store_true",
  help="Generate SHA512 hashes of given passwords")

def hash_wordlist(wordlist, hashing_algorithm):
  """Hashes each of the words in the wordlist and yields the digests for each
  word.

  Parameters:
    - wordlist: The wordlist which we'll be hashing.
    - hashing_obj: The hashlib hashing algorithm which we'll be passing to the
      appropriate function to actually hash the word.

  """
  for word in wordlist:
    word = word.encode("utf-8")
    hashing_obj = hashing_algorithm.copy()
    hashing_obj.update(word)
    
    return_string = hashing_obj.hexdigest() + ":" + str(word)
    yield return_string

def create_rainbow_table(wordlist, hashing_algorithm, output, use_database=True):
  """Creates the rainbow table from the given plaintext wordlist.

  Parameters:
    - wordlist: The plaintext wordlist to hash.
    - hashing_algorithm: The algorithm to use when hashing the wordlist.
    - output: The name of the output file.
    - db: Flag whether the output is an SQLite DB or not (default=True).

  """
  # Create the database, if necessary
  if use_database:
    db_file = output + ".db"
    db_connection = sqlite3.connect(db_file)
    db.create_table(db_connection)

  # Now actually hash the words in the wordlist
  try:
    with open(wordlist, "r", encoding="utf-8") as wl:
      for entry in hash_wordlist(wordlist, hashing_algorithm):
        if use_database:
          entries = entry.split(":")
          db.save_pair(db_connection, entries[0], entries[1])
        else:
          # TODO: Save entry into text file
          pass
  except IOError as err:
    print("File error: " + str(err))
    
def main():
  args = parser.parse_args()
  wordlist = args.wordlist or ""

  # Figure out the user's choice in hashing algorithms and create the
  # appropriate hashlib object for the job.
  if args.sha1:
    hashing_algorithm = hashlib.sha1()
  elif args.sha256:
    hashing_algorithm = hashlib.sha256()
  elif args.sha512:
    hashing_algorithm = hashlib.sha512()
  else:
    hashing_algorithm = hashlib.md5()

  
  if args.generate_wordlist:
    # TODO: Implement wordlist generation
    pass
  
  if args.use_textfile:
    # Save as a textfile instead of a database
    create_rainbow_table(wordlist, hashing_algorithm, args.output, use_database=False)
  else:
    create_rainbow_table(wordlist, hashing_algorithm, args.output)

if __name__ == "__main__":
  main()
