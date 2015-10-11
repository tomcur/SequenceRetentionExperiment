"""
@author Thomas Churchman

Module that provides trial handling.
"""

class TrialHandler:
    def __init__(self, win, numRepetitions, task):
        self.win = win
        self.task = task
        self.numRepetitions = numRepetitions
        
    def run(self):
        for t in range(0,self.numRepetitions):
            self.task.run()
    