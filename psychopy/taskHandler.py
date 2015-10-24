"""
@author Thomas Churchman, Diede Kemper

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
    colors = {1: "#22b14c", 2: "#ed1c24", 3: "#bcbf00", 4: "#00a2e8"}
    highlightColors = {1: "#a6ffc1", 2: "#ffa6a9", 3: "#feffa6", 4: "#a6e4ff"}
    color = "#000000"
    highlightColor = "#b3b3b3"
    lineColor = "#757575"
    
    buttons = []
    
    def __init__(self, win, tryout=False):
        self.win = win
        self.showText = ShowText(self.win)
        self.tryout = tryout
    
    def _emptyButtons(self):
        self.buttons = []
    
    def _registerButton(self, shape, button):
        self.buttons.append(
        ( 
            shape, button
        ));
    
    def __increaseSequence(self):
        """
        Increase the sequence by 1
        """
        if len(self.sequence) > 0:
            last = self.sequence[-1]
        else:
            last = None
        
        while True:
            append = numpy.random.randint(0, self.numOptions)+1
            
            # New button may not be the same as the previous button
            if not append == last:
                self.sequence.append(append)
                break
            
   
    def _increaseSequence(self, amount=1):
        """
        Increase the sequence by length amount
        """
        for i in range(0, amount):
            self.__increaseSequence()
        
    
    def run(self):
        """
        Run the task.
        """
        self.sequence = []
        rememberedLength = 0
        
        self.startText()
        
        while True:
            
            if(self.tryout and rememberedLength==6): #tryout tasks only take 3 correct answers (3x2 = 6)
                return rememberedLength
            
            self._increaseSequence(amount=2)
            
            sounds.sequencePresentSound.play()
            self._presentSequence()
            
            sounds.sequenceAnswerSound.play()
            correct = self.answer()
            
            if correct:
                rememberedLength = rememberedLength + 2
            else:
                self.showText.showForXSec(u"Wrong.", 1)
                return rememberedLength
            
    def _presentSequence(self):
        """
        Present a stimulus sequence.
        """
        self.present(None)
        core.wait(0.5)
        for stimulus in self.sequence:
            # Present stimulus
            self.present(stimulus)
            core.wait(0.9)
        self.present(None)
        core.wait(0.8)

    def answer(self):
        """
        Subject has to recall the sequence.
        Returns true if the answer was correct, false otherwise.
        """ 
        
        self._emptyButtons()
        self._populateButtons()
        
        self._showAnswerGrid()
        alreadyReset = True
        
        event.clearEvents(eventType='mouse')
        a = 0
        
        # Track current highlighted shape
        highlight = None
        
        # Click toggle
        clickChanged = False
        _isPressed = False
        
        # Track shape presses
        pressStart = None
        
        mouse = event.Mouse()
        while a < len(self.sequence) or _isPressed:
            pr = mouse.getPressed()
            pr = pr[0]
            
            # Track whether the mouse went from pressed to unpressed,
            # or vice versa
            clickChanged = not pr == _isPressed
            _isPressed = pr
            
            # Highlight button that is hovered over
            pos = mouse.getPos()
            newHighlight = None
            for (shape, button) in self.buttons:
                if shape.contains(pos):
                    newHighlight = button
            if (not newHighlight == highlight) or clickChanged:
                highlight = newHighlight
                self._showAnswerGrid(highlight, pr)
                        
            # Find which (if any) button is pressed
            pressed = None
            if clickChanged and _isPressed:
                for (shape, button) in self.buttons:
                    if mouse.isPressedIn(shape, [0]):
                        pressed = button
                        
            # A button was pressed (with an initial press)
            if not pressed == None:
                pressStart = pressed
            
            # A button is clicked if the mouse was first pressed at its 
            # location, and if the mouse is released at its location
            clicked = None
            if clickChanged and _isPressed == False:
                if pressStart == highlight:
                    clicked = pressStart
            
            if not clicked == None:
                sounds.buttonClickSound.play();
                if self.sequence[a] == clicked:
                    # Correct answer at this position in the sequence
                    a = a + 1
                else:
                    # Incorrect answer
                    return False
                    
        core.wait(1)
        self._showAnswerGrid()
        return True 