#!/usr/bin/env python3

import sqlite3
import os
from .dbsqlite import create_table as sqlite_create_table
from .dbsqlite import save_pair as sqlite_save_pair
from .dbmongo import create_table as mongo_create_table
from .dbmongo import save_pair as mongo_save_pair
from .abstract_mongo import Mongo

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


def create_rainbow_table(
        wordlist, hashing_algorithm, output, use_database=False,
        use_sqlite=False, use_mongo=False):
    """Creates the rainbow table from the given plaintext wordlist.

    Parameters:
    - wordlist: The plaintext wordlist to hash.
    - hashing_algorithm: The algorithm to use when hashing the wordlist.
    - output: The name of the output file.
    - db: Flag whether the output is an SQLite DB or not (default=False).
    - use_sqlite : Flag if we want to store in sqlite database
    - use_mongo : Flag if we want to store in mongo database
    """
    # Create the database, if necessary.
    if use_database and use_sqlite:
        db_file = output + ".db"
        db_connection = sqlite3.connect(db_file)
        sqlite_create_table(db_connection)
    elif use_database and use_mongo:
        db_connection = Mongo(os.path.basename(output))
        mongo_create_table(db_connection)
    else:
        # Otherwise, create the plaintext file.
        txt_file = open(output + ".txt", "a")

      # Now actually hash the words in the wordlist.
    try:
        with open(wordlist, "r", encoding="utf-8") as wl:
            if use_database and use_sqlite:
                for entry in _hash_wordlist(wl, hashing_algorithm):
                    entries = entry.split(":")
                    sqlite_save_pair(db_connection, entries[0], entries[1])
            elif use_database and use_mongo:
                for entry in wl:
                    mongo_save_pair(db_connection, entry)
            else:
                for entry in _hash_wordlist(wl, hashing_algorithm):
                    txt_file.write(entry)
                txt_file.close()
    except IOError as err:
        print("File error: " + str(err))
