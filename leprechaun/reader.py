#!/usr/bin/env python3

from multiprocessing import Process, Queue
import os
import signal

from .leprechaun_process import Process

class Reader(Process):
  """Reads in words from one or more wordlists, sending them to Worker processes
  to be hashed and saved."""
  def __init__(self, parent_queue, worker_queue):
    super().__init__(parent_queue)
    self.worker_queue = worker_queue
    self.workers = []

  def ready(self, signum, frame):
    """Called when the parent process has initialized everything properly. The
    parent process will then send a list of PIDs relating to the worker
    processes.

    Parameters:
      - self: A pointer to the current object.
      - signum: The ID of the signal which is being processed.
      - frame: The current stack frame.

    """
    # Read the worker PIDs from the parent queue
    self.workers = self.parent_queue.get()

    # Now, ignore all signals from the parent process. We don't need him
    # anymore.
    super().ready(signum, frame)

  def read(self, signum, frame)
    """Read each line from the wordlist(s) and put it into the worker queue

    Parameters:
      - self: A pointer to the current object.
      - signum: The ID of the signal which is being processed.
      - frame: The current stack frame.

    """
    pass