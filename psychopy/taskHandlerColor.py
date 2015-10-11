"""
@author Thomas Churchman

Module that provides a color task handler.
"""

from psychopy import core, visual, event
from taskHandler import *
import numpy

class TaskHandlerColor(TaskHandler):
    """
    Class implementing a color task.
    """
    colors = {1: "#22b14c", 2: "#ed1c24", 3: "#fff200", 4: "#00a2e8"}
    lineColor = "#656565"
    numOptions = 4
    
    def __init__(self, win):
        TaskHandler.__init__(self, win)
    
    def startText(self):
        self.showText.showForXSec(u"Remember the color sequence.", 1.5)
    
    def present(self, stimulus):
            # Present blank screen
            self.win.flip()
            core.wait (0.25)
            
            # Present stimulus
            rect = visual.Rect(self.win, 0.5, 0.5)
            rect.setFillColor(self.colors[stimulus])
            rect.draw()
            self.win.flip()
           
    def _showAnswers(self, permutation, highlight=None):
        """
        Show the answer grid with given permutation. If a highlight is given,
        then that color will be highlighted.
        """
        p = 0
        
        for k in permutation:
            rect = visual.Rect(self.win, 0.45/self.numOptions, 0.45/self.numOptions)
            rect.setFillColor(self.colors[k])
            rect.setPos((-0.5 + float(p) / self.numOptions + 0.1, 0))
            rect.setLineWidth(0)
            if k == highlight:
                rect.setLineWidth(10)
                rect.setLineColor(self.lineColor)
                
            rect.draw()
            
            p = p + 1
            
        self.win.flip()
        
           
    def answer(self):
        """
        Subject has to recall the sequence.
        Returns true if the answer was correct, false otherwise.
        """ 
        
        permutation = numpy.random.permutation(self.colors.keys())
        
        self._showAnswers(permutation)
        alreadyReset = True
        
        taskClock = core.Clock()
        taskClock.reset()
        
        event.clearEvents(eventType='keyboard')
        a = 0
        while a < len(self.sequence):
            # Listen for events for keys 1, 2, 3 and 4
            theseKeys = event.getKeys(['1', '2', '3', '4'])
            
            # Reset answer grid highlight after answer is given 
            # and specified time has elapsed
            if not alreadyReset:
                if taskClock.getTime() >= resetTime:
                    self._showAnswers(permutation)
                    alreadyReset = True
            
            if len(theseKeys) > 0:
                # Clear keyboard events
                event.clearEvents(eventType='keyboard')
                
                # Get the key that was pressed
                key = int(theseKeys[0])-1    
                
                # Get which answer is associated with this key
                answer = permutation[key]
                
                # Highlight the chosen color
                self._showAnswers(permutation, answer)
            
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
        self._showAnswers(permutation)
        return True 