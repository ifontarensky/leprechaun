#!/usr/bin/env python3

import sqlite3

class DB(object):
  """A class for handling all database operations."""

  def __init__(self, db_file):
    self.connection = sqlite3.connect(db_file)

  def create_table(self):
    """Creates a new table in the database."""
    with self.connection:
      cursor = self.connection.cursor()
      cursor.execute("""CREATE TABLE IF NOT EXISTS rainbow
        (id INTEGER PRIMARY KEY, digest TEXT, word TEXT)""")

  def save_pair(self, digest, word):
    """Save both the original word and its digest into the database.

    Parameters:
      - digest: The digest of the plaintext word; acts as the primary key.
      - word: The plaintext word.

    """
    with self.connection:
      cursor = self.connection.cursor()
      _t = (digest, word)

      cursor.execute("""INSERT INTO rainbow
        VALUES (NULL, ?, ?)""", _t)
      
  def get_password(self, digest):
    """Query the database for the digest and return the plaintext password.

    Parameters:
      - connection: The connection to the SQLite database.
      - digest: The digest of the plaintext word.

    Returns:
      - The plaintext password associated with the given digest.
    
    """
    with self.connection:
      cursor = self.connection.cursor()
      _t = (digest,)
      cursor.execute("SELECT word FROM rainbow WHERE digest=?", _t)
      return cursor.fetchone()
