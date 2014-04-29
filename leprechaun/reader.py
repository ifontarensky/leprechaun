#!/usr/bin/env python3

import glob
import os
import signal

class Reader(object):
  """Reads through all of the lines in a wordlist, passing them off to a Worker
  process to be hashed."""
  def __init__(self, wordlist, queue, workers, multiple_wordlists=False):
    self.wordlist = wordlist
    self.queue = queue
    self.workers = workers # This is a list of pointers to the workers
    self.multiple_wordlists = multiple_wordlists

  def _send_word(self, word, worker_pid):
    """Put the given word into the Queue for the Worker processes to hash.

    Parameters:
      - word: The word to send off.
      - worker_pid: The worker to signal saying there's a word available.

    """
    word = word.split()
    self.queue.put(word)

    # Signal the worker that there's a new word ready to be pulled. Whether they
    # get that EXACT same word to work on is irrelevant, as long as they get a
    # word!
    os.kill(worker_pid, signal.SIGUSR1)

  def read(self):
    """Read through every line in the wordlist(s) provided, putting every line
    into a queue, from which the Worker processes pull from."""
    split = len(workers)
    index = 0

    if self.multiple_wordlists: # There are multiple wordlists to work with
      for wordlist in sorted(glob.glob(os.path.abspath(self.wordlist +
        "/*.txt"))):
        for word in wordlist:
          worker_pid = self.workers[index].pid

          # Send the word to the worker
          self._send_word(word, worker_pid)

          # Move onto the next worker
          index = (index + 1) % split
    else:
      for word in os.path.abspath(self.wordlist):
        worker_pid = self.workers[index].pid

        # Send the word to the worker
        self._send_word(word, worker_pid)

        # Move onto the next worker
        index = (index + 1) % split
