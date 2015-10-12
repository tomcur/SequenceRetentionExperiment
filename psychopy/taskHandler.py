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