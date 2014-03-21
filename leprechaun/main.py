#!/usr/bin/env python3

import argparse
import generator

# Create command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--wordlist", default="data/wordlist.txt",
  help="The list of words to hash (default=data/wordlist.txt")
parser.add_argument("-g", "--generate-wordlist", action="store_true",
  help="Generate a wordlist dynamically instead of using a prebuilt one")

parser.add_argument("-d", "--db-name", default="rainbow.db",
  help="Name of the rainbow table database file (default=rainbow.db)")

parser.add_argument("-t", "--use-textfile", action="store_true",
  help="Save output to a plaintext file instead of sqlite database")
parser.add_argument("-f", "--file-name", default="rainbow.txt",
  help="Name of the plaintext file (default=rainbow.txt)")

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

def main():
  args = parser.parse_args()

  if args.database:
    con = sqlite3.connect(args.db_name)
    cur = con.cursor()
    cur.execute("""create table if not exists rainbow(id integer primary key
        autoincrement, hash text not null, word text not null)""")
    con.commit()
  
  # Figure out the user's choice in hashing algorithms and create the
  # appropriate hashlib object for the job.
  if hash_object == "sha1":
    hash_object = hashlib.sha1()
  elif hash_object == "sha256":
    hash_object = hashlib.sha256()
  elif hash_object == "sha512":
    hash_object = hashlib.sha512()
  else:
    hash_object = hashlib.md5()
  
  try:
    with open(args.output, "w") as output:
      with open(args.wordlist, "r") as wordlist:
        for line in wordlist:
          line = line.strip()

          # Create an object to hash the line
          line_hash = hash_object.copy()
          line_hash.update(line.encode("utf-8"))
          print(line_hash.hexdigest() + ": " + line, file=output)
          if args.database:
            cur.execute("insert into rainbow (hash, word) values (?, ?)", 
              (str(line_hash.hexdigest()), str(line)))

          for combination in digit_generator(args.number):
            # Create an object to hash the line, combined with added digits
            combination_line = line + combination
            combination_hash = hash_object.copy()
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

if __name__ == "__main__":
  main()
