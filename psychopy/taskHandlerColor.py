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
    
    def __init__(self, win, tryout=False):
        TaskHandler.__init__(self, win, tryout)
    
    def startText(self):
        self.showText.showForXSec(u"Remember the following color sequence:", 1.5)
    
    def present(self, stimulus):
            # Present blank screen
            self.win.flip()
            core.wait (0.25)
            
            # Present stimulus
            rect = visual.Rect(self.win, 0.5, 0.5)
            rect.setFillColor(self.colors[stimulus])
            rect.draw()
            self.win.flip()
           
        
    def _showAnswerGrid(self,permutation, highlight=None):
        """
        Show the answer grid. If a highlight is given,
        then that entity will be highlighted.
        """
        #draw text
        txt = "Repeat the sequence by pressing the corresponding keys on your keyboard"
        text = visual.TextStim(win=self.win, text= txt, color='#444444', height=0.05)
        text.setPos((0,0.3))
        text.draw()
        
        p = 1
        
        for k in permutation:
            #draw rectangle
            rect = visual.Rect(self.win, 0.2, 0.2)
            rect.setFillColor(self.colors[k])
            rect.setPos(self.answerPositions[p])
            rect.setLineWidth(0)
            if highlight == k:
                rect.setLineWidth(10)
                rect.setLineColor(self.lineColor)
                
            rect.draw()
            
            #draw corresponding key
            txt = "[" + str(self.positionKeys[k]) + "]"
            key = visual.TextStim(win=self.win,text=txt, color='#444444', height=0.05)
            key.setPos(self.textPositions[k])
            key.draw()
            
            p = p + 1
            
        self.win.flip()
       
    def answer(self):
        """
        Subject has to recall the sequence.
        Returns true if the answer was correct, false otherwise.
        """ 
        permutation = numpy.random.permutation(self.colors.keys())
        
        self._showAnswerGrid(permutation)
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
                    self._showAnswerGrid(permutation)
                    alreadyReset = True
            
            if len(theseKeys) > 0:
                # Clear keyboard events
                event.clearEvents(eventType='keyboard')
                
                # Get the key that was pressed
                key = theseKeys[0]
                
                # Get the answer that was chosen
                index = invKeyMap[key]
                answer = permutation[(index-1)]
                
                # Highlight the chosen answer
                self._showAnswerGrid(permutation, answer)
                
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
        self._showAnswerGrid(permutation)
        return True 
    