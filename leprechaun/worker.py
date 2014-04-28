#!/usr/bin/env python3

import multiprocessing
import os

class Worker(multiprocessing.Process):
  """A specialized process which will hash a wordlist."""
  def __init__(self, wordlist, hashing_algorithm, output_queue):
    super(Worker, self).__init__()
    self.wordlist = wordlist
    self.hashing_algorithm = hashing_algorithm
    self.output_queue = output_queue


  def hash_wordlist(self):
    """Hashes each of the words in the wordlist and puts the result into the
    output queue."""
    for word in self.wordlist:
      # Create a copy of the hashing algorithm so the digest doesn't become
      # corrupted.
      hash_obj = self.hashing_algorithm.copy()
      hash_obj.update(word.encode())

      lookup_string = hash_obj.hexdigest() + ":" + word
      self.output_queue.put(lookup_string)

  def run(self):
    self.hash_wordlist()
