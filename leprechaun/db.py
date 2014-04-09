#!/usr/bin/env python3

import sqlite3

def create_table(connection):
  """Creates a new table in the database.

  Parameters:
    - connection: The connection to the SQLite database.

  """
  cursor = connection.cursor()
  cursor.execute("""CREATE TABLE IF NOT EXISTS rainbow
    (id INTEGER PRIMARY KEY, digest TEXT, word TEXT)""")
  connection.commit()

def save_pair(connection, digest, word):
  """Save both the original word and its digest into the database.

  Parameters:
    - connection: The connection to the SQLite database.
    - digest: The digest of the plaintext word; acts as the primary key.
    - word: The plaintext word.

  """
  cursor = connection.cursor()
  t = (digest, word)

  cursor.execute("""INSERT INTO rainbow
    VALUES (NULL, ?, ?)""", t)
  
  connection.commit()

def get_password(connection, digest):
  """Query the database for the digest and return the plaintext password.

  Parameters:
    - connection: The connection to the SQLite database.
    - digest: The digest of the plaintext word.

  Returns:
    - The plaintext password associated with the given digest.
  
  """
  cursor = connection.cursor()
  t = (digest)
  cursor.execute("SELECT word FROM rainbow WHERE digest=?", t)
  return cursor.fetchone()
