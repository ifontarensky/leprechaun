#!/usr/bin/env python3

from multiprocessing import Queue
import os
import signal

from .leprechaun_process import Process

class Writer(Process):
  """Writes the rainbow values to a file or database."""
  def __init__(self, parent_queue, worker_queue, use_database=False):
    super().__init__(parent_queue)
    self.worker_queue = worker_queue
    self.use_database = use_database

    # Send this processes PID to the parent
    self.parent_queue.put(self.pid)
    os.kill(os.getppid(), signal.SIGUSR1)

    # Listen for the "all ready" signal from the parent, after which we can
    # get to work.
    signal.signal(signal.SIGUSR1, ready)

  def ready(self, signum, frame):
    """Called when the parent process has initialized everything properly.

    Parameters:
      - self: A pointer to the current object.
      - signum: The ID of the signal which is being processed.
      - frame: The current stack frame.

    """
    signal.signal(signal.SIGUSR1, signal.SIG_IGN) # Ignore the "USR1" signal
    signal.signal(signal.SIGUSR2, write) # Listen for signals from the Workers

  def write(self, signum, frame)
    """Write the hashed line to the file or database.

    Parameters:
      - self: A pointer to the current object.
      - signum: The ID of the signal which is being processed.
      - frame: The current stack frame.

    """
    pass