"""
@author Thomas Churchman

Module that provides trial handling.
"""
from showText import *

class TrialHandler:
    def __init__(self, win, numRepetitions, conditionNr, conditionName, task):
        self.win = win
        self.showText = ShowText(self.win)
        self.task = task
        self.conditionNr = conditionNr
        self.numRepetitions = numRepetitions
        self.conditionName = conditionName
        
    def run(self):
        scoreList = []
        for t in range(0,self.numRepetitions):
            #pause screen for subject
            text = ("Condition " + str(self.conditionNr) + "/3: " + self.conditionName + "\n" 
                + "Task " + str(t+1) + "/" + str(self.numRepetitions) + "\n"
                + "Press any key to continue")
            self.showText.showUntilKeyPressed(text)
            
            #next task
            scoreList.append(self.task.run())
        return scoreList
    