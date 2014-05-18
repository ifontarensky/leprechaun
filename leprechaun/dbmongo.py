#!/usr/bin/env python3

from .abstract_mongo import Mongo
import hashlib

def create_table(connections):
    """Creates a new table in the database.

    Parameters:
    - connection: The connection to the Mongo database.

    """
    for key in ["md5", "sha1", "sha256", "sha512"]:
        connections.create_index("rainbow", key)


def save_pair(connection, word):
    """Save both the original word and its digest into the database.

    Parameters:
    - connection: The connection to the SQLite database.
    - digest: The digest of the plaintext word; acts as the primary key.
    - word: The plaintext word.

    """
    if not connection.find_one("rainbow", {"word": word}):
        value = {
            "md5": hashlib.md5(word.encode()).hexdigest(),
            "sha1": hashlib.sha1(word.encode()).hexdigest(),
            "sha256": hashlib.sha256(word.encode()).hexdigest(),
            "sha512": hashlib.sha512(word.encode()).hexdigest(),
            "word": word
        }
        connection.insert("rainbow", value)


def get_password(connection, digest):
    """Query the database for the digest and return the plaintext password.

    Parameters:
    - connection: The connection to the SQLite database.
    - digest: The digest of the plaintext word.

    Returns:
    - The plaintext password associated with the given digest.

    """
    print(len(digest))
    return connection.find_one("rainbow", {"sha256": digest})

