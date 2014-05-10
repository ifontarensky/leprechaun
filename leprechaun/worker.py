#!/usr/bin/env python3

from multiprocessing import Process, Queue
import os
import signal

from .leprechaun_process import Process

class Worker(Process):
  """Hashes all words sent over from the Reader process, sending the hashed
  values over to a Writer process to be saved."""
  def __init__(self, parent_queue, reader_queue, writer_queue,
      hashing_algorithm):
    super().__init__(parent_queue)
    self.worker_queue = worker_queue
    self.reader_queue = reader_queue
    self.writer_queue = writer_queue
    self.hashing_algorithm = hashing_algorithm

    # Send this processes PID to the parent
    self.parent_queue.put(self.pid)
    os.kill(os.getppid(), signal.SIGUSR1)

    # Listen for the "all ready" signal from the parent, after which we can
    # get to work.
    signal.signal(signal.SIGUSR1, ready)

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
    signal.signal(signal.SIGUSR1, signal.SIG_IGN)

  def read(self, signum, frame)
    """Read each line from the wordlist(s) and put it into the worker queue

    Parameters:
      - self: A pointer to the current object.
      - signum: The ID of the signal which is being processed.
      - frame: The current stack frame.

    """
    pass