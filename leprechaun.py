#!/usr/bin/env python3

import argparse
import hashlib
import itertools
import string
import sqlite3

def getHash(args):
  """Returns a string representing the hash that the user wishes to use."""
  if args.sha1:
    return "sha1"
  elif args.sha256:
    return "sha256"
  elif args.sha512:
    return "sha512"
  else:
    return "md5"

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

# Create command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--wordlist", default="wordlist.txt",
  help="The wordlist to hash (default=wordlist.txt)")
parser.add_argument("-o", "--output", default="rainbow-table.txt",
  help="Name of the rainbow table file (default=rainbow-table.txt)")
parser.add_argument("-d", "--database", action="store_true",
  help="Save in sqlite-database instead of textfile")
parser.add_argument("--db-name", default="rainbow-table.db",
  help="Name of the rainbow table database file (default=rainbow-table.db)")
parser.add_argument("-n", "--number", type=int, default=0,
  help="Number of integers to append to end of password string (default=0)")
parser.add_argument("-m", "--md5", action="store_true",
  help="Generate MD5 hashes of given passwords (default)")
parser.add_argument("-s", "--sha1", action="store_true",
  help="Generate SHA1 hashes of given passwords")
parser.add_argument("-s2", "--sha256", action="store_true",
  help="Generate SHA256 hashes of given passwords")
parser.add_argument("-s5", "--sha512", action="store_true",
  help="Generate SHA512 hashes of given passwords")

if __name__ == "__main__":
  args = parser.parse_args()

  if args.database:
    con = sqlite3.connect(args.db_name)
    cur = con.cursor()
    cur.execute("""create table if not exists rainbow(id integer primary key
        autoincrement, hash text not null, word text not null)""")
    con.commit()
  
  # Figure out the user's choice in hashing algorithms and create the
  # appropriate hashlib object for the job.
  user_hash = getHash(args)
  if user_hash == "sha1":
    user_hash = hashlib.sha1()
  elif user_hash == "sha256":
    user_hash = hashlib.sha256()
  elif user_hash == "sha512":
    user_hash = hashlib.sha512()
  else:
    user_hash = hashlib.md5()
  
  try:
    with open(args.output, "w") as output:
      with open(args.wordlist, "r") as wordlist:
        for line in wordlist:
          line = line.strip()

          # Create an object to hash the line
          line_hash = user_hash.copy()
          line_hash.update(line.encode("utf-8"))
          print(line_hash.hexdigest() + ": " + line, file=output)
          if args.database:
            cur.execute("insert into rainbow (hash, word) values (?, ?)", 
              (str(line_hash.hexdigest()), str(line)))

          for combination in digit_generator(args.number):
            # Create an object to hash the line, combined with added digits
            combination_line = line + combination
            combination_hash = user_hash.copy()
            combination_hash.update(combination_line.encode("utf-8"))
            print(combination_hash.hexdigest() + ": " + combination_line,
              file=output)
            if args.database:
              cur.execute("insert into rainbow (hash, word) values (?, ?)", 
                (combination_hash.hexdigest(), combination_line))

    if args.database:
      cur.close()
      con.commit()
      con.close()

  except IOError as err:
    print("File error: " + str(err))
