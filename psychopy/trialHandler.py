"""
@author Thomas Churchman

Module that provides trial handling.
"""
from showText import *

class TrialHandler:
    def __init__(self, win, numRepetitions, conditionNr, task):
        self.win = win
        self.showText = ShowText(self.win)
        self.task = task
        self.conditionNr = conditionNr
        self.numRepetitions = numRepetitions
        
    def run(self):
        scoreList = []
        for t in range(0,self.numRepetitions):
            #pause screen for subject
            text = ("Condition " + str(self.conditionNr) + "/3\n" 
                + "Task " + str(t+1) + "/" + str(self.numRepetitions) + "\n"
                + "Press [space] to continue")
            self.showText.showUntilKeyPressed(text, keyList=['space'])
            
            #next task
            scoreList.append(self.task.run())
        return scoreList
    