#!/usr/bin/env python3

import multiprocessing
import os
import signal

class Process(multiprocessing.Process):
  """A wrapper over the traditional multiprocessing Process. Allows for child
  processes to communicate with their parent and exchange PIDs, for easy message
  passing."""
  def __init__(self, parent_queue):
    Process.__init__(self)
    self.parent_queue = parent_queue

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