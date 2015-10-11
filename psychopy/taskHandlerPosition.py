"""
@author Thomas Churchman

Module that provides a position task handler.
"""

from psychopy import core, visual, event
from taskHandler import *
import numpy

class TaskHandlerPosition(TaskHandler):
    """
    Class implementing a position task.
    """
    #colors = {1: "#22b14c", 2: "#ed1c24", 3: "#fff200", 4: "#00a2e8"}
    
    color = "#000000"
    positions = {
        1: (-0.225, 0.225), 
        2: (0.225, 0.225), 
        3: (0.225, -0.225), 
        4: (-0.225, -0.225)
    }
    positionKeys = {1: "q", 2: "w", 3: "s", 4: "a"}
    
    
    lineColor = "#656565"
    numOptions = 4
    
    def __init__(self, win):
        TaskHandler.__init__(self, win)
    
    def startText(self):
        self.showText.showForXSec(u"Remember the position sequence.", 1.5)
    
    def present(self, stimulus):
        """
        Present the stimulus grid.
        """
        self._showGrid()
        core.wait(0.25)
        self._showGrid(stimulus)
           
    def _showGrid(self, highlight=None):
        """
        Show the grid. If a highlight is given,
        then that entity will be highlighted.
        """
        for k in range(1, self.numOptions+1):
            rect = visual.Rect(self.win, 0.35, 0.35)
            rect.setFillColor(self.color)
            rect.setPos(self.positions[k])
            rect.setLineWidth(0)
            if highlight == k:
                rect.setLineWidth(10)
                rect.setLineColor(self.lineColor)
                
            rect.draw()
            
        self.win.flip()
        
           
    def answer(self):
        """
        Subject has to recall the sequence.
        Returns true if the answer was correct, false otherwise.
        """ 
        
        self._showGrid()
        alreadyReset = True
        
        taskClock = core.Clock()
        taskClock.reset()
        
        event.clearEvents(eventType='keyboard')
        a = 0
        while a < len(self.sequence):
            # Listen for events for keys 1, 2, 3 and 4
            theseKeys = event.getKeys(self.positionKeys.values())
            invKeyMap = {v: k for k, v in self.positionKeys.items()}
            
            # Reset answer grid highlight after answer is given 
            # and specified time has elapsed
            if not alreadyReset:
                if taskClock.getTime() >= resetTime:
                    self._showGrid()
                    alreadyReset = True
            
            if len(theseKeys) > 0:
                # Clear keyboard events
                event.clearEvents(eventType='keyboard')
                
                # Get the key that was pressed
                key = theseKeys[0]
                
                # Get the answer that was chosen
                answer = invKeyMap[key]
                
                # Highlight the chosen answer
                self._showGrid(answer)
                
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
        self._showGrid()
        return True 