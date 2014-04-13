#!/usr/bin/env python3

import argparse
import glob
import hashlib
import os
import sys

from .generator import wordlist_generator
from .rainbow import create_rainbow_table

def main():
  """Main function."""
  # Create the command line arguments.
  parser = argparse.ArgumentParser(prog="leprechaun")
  parser.add_argument("-n", "--number", type=int, default=0,
    help="Number of integers to append to end of password string (default=0)")

  group_wordlist = parser.add_argument_group("wordlist arguments")
  group_wordlist.add_argument("-w", "--wordlist",
    help="The list of words to hash (default=included lists)")
  group_wordlist.add_argument("-g", "--generate-wordlist", action="store_true",
    help="Generate a wordlist dynamically instead of using a prebuilt one")
  group_wordlist.add_argument("-l", "--word-length", type=int, default=8,
    help="Maximum word length for generated wordlist")

  group_output = parser.add_argument_group("output arguments")
  group_output.add_argument("-o", "--output", default="rainbow",
    help="The name of the output file (default=rainbow)")
  group_output.add_argument("-d", "--use-database", action="store_true",
    help="Rainbow table will be an sqlite database, not a plaintext file")

  group_hashing = parser.add_argument_group("hashing arguments")
  group_hashing.add_argument("-m", "--md5", action="store_true",
    help="Generate MD5 hashes of given passwords (default)")
  group_hashing.add_argument("-s", "--sha1", action="store_true",
    help="Generate SHA1 hashes of given passwords")
  group_hashing.add_argument("-s2", "--sha256", action="store_true",
    help="Generate SHA256 hashes of given passwords")
  group_hashing.add_argument("-s5", "--sha512", action="store_true",
    help="Generate SHA512 hashes of given passwords")

  # Parse the command line arguments.
  args = parser.parse_args()

  # Generate a wordlist for the user if they request one.
  if args.generate_wordlist:
    wordlist_generator("wordlist.txt", args.word_length)

    # We just want to generate a wordlist, so exit the program when that's done.
    # Maybe in the future we'll hash the wordlist, but for now I don't really
    # want to.
    sys.exit(0)

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

  # Because this program is intended to be distributed, we need to update the
  # paths for both the included wordlists and the outputted rainbow table.
  output = os.getcwd() + "/" + args.output
  if not args.wordlist: # No need to interfere with the user's input!
    wordlists = os.path.dirname(os.path.realpath(__file__))
    wordlists = wordlists + "/data/wordlist*"

  # Determine if the user is going to use their own wordlist or if they're using
  # ours.
  if args.wordlist: # User is using their own wordlist.
    if args.use_database: # Save the rainbow table as an SQLite DB.
      create_rainbow_table(args.wordlist, hashing_algorithm, args.output,
        use_database=True)
    else: # Save the rainbow table as a plaintext file.
      create_rainbow_table(args.wordlist, hashing_algorithm, args.output)
  else: # User is using our wordlist.
    for wordlist in sorted(glob.glob(wordlists)):
      if args.use_database: # Save the rainbow table as an SQLite DB.
        create_rainbow_table(wordlist, hashing_algorithm, args.output,
          use_database=True)
      else: # Save the rainbow table as a plaintext file.
        create_rainbow_table(wordlist, hashing_algorithm, args.output)

if __name__ == "__main__":
  main()
