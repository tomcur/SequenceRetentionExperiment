"""
@author Thomas Churchman

Module that provides an abstract task handler.
"""

from psychopy import core
import numpy
from showText import *
import sounds

class TaskHandler:
    """
    'Abstract' class implementing a task.
    """
    colors = {1: "#22b14c", 2: "#ed1c24", 3: "#fff200", 4: "#00a2e8"}
    color = "#000000"
    positions = { #normal grid positions
        1: (-0.225, 0.225), 
        2: (0.225, 0.225), 
        3: (0.225, -0.225), 
        4: (-0.225, -0.225)
    }
    answerPositions = { #grid positions of answer grid
        1: (-0.13, 0.05), 
        2: (0.13, 0.05), 
        3: (0.13, -0.21), 
        4: (-0.13, -0.21)
    }
    textPositions = { #positions of key text in answer grid
        1: (-0.3, 0.05), 
        2: (0.3, 0.05), 
        3: (0.3, -0.21), 
        4: (-0.3, -0.21)
    }
    positionKeys = {1: "q", 2: "w", 3: "s", 4: "a"}
    
    def __init__(self, win):
        self.win = win
        self.showText = ShowText(self.win)
    
    def run(self):
        """
        Run the task.
        """
        self.sequence = []
        rememberedLength = 0
        
        self.startText()
        
        while True:
            self.sequence.append(numpy.random.randint(1, self.numOptions+1))
            
            sounds.sequencePresentSound.play()
            core.wait(1.0)
            self._presentSequence()
            
            sounds.sequenceAnswerSound.play()
            correct = self.answer()
            
            if correct:
                rememberedLength = rememberedLength + 1
            else:
                self.showText.showForXSec(u"Wrong.", 1)
                return rememberedLength
            
    def _presentSequence(self):
        """
        Present a stimulus sequence.
        """
        
        for stimulus in self.sequence:
            # Present stimulus
            self.present(stimulus)
            core.wait(1)

    def answer(self):
        """
        Subject has to recall the sequence.
        Returns true if the answer was correct, false otherwise.
        """ 
        
        self._showAnswerGrid()
        alreadyReset = True
        
        taskClock = core.Clock()
        taskClock.reset()
        
        event.clearEvents(eventType='keyboard')
        a = 0
        while a < len(self.sequence):
            # Listen for events for keys q, w, s, a
            theseKeys = event.getKeys(self.positionKeys.values())
            invKeyMap = {v: k for k, v in self.positionKeys.items()}
            
            # Reset answer grid highlight after answer is given 
            # and specified time has elapsed
            if not alreadyReset:
                if taskClock.getTime() >= resetTime:
                    self._showAnswerGrid()
                    alreadyReset = True
            
            if len(theseKeys) > 0:
                # Clear keyboard events
                event.clearEvents(eventType='keyboard')
                
                # Get the key that was pressed
                key = theseKeys[0]
                
                # Get the answer that was chosen
                answer = invKeyMap[key]
                
                # Highlight the chosen answer
                self._showAnswerGrid(answer)
                
                # Set time at which to reset the grid to no highlight
                resetTime = taskClock.getTime() + 1.0
                alreadyReset = False
                
                if self.sequence[a] == answer:
                    # Correct answer at this position in the sequence
                    a = a + 1
                else:
                    # Incorrect answer
                    return False
        core.wait(1)
        self._showAnswerGrid()
        return True 