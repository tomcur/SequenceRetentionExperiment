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

    
    
    lineColor = "#656565"
    numOptions = 4
    
    def __init__(self, win):
        TaskHandler.__init__(self, win)
    
    def startText(self):
        self.showText.showForXSec(u"Remember the following position sequence:", 1.5)
    
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
        
    def _showAnswerGrid(self,highlight=None):
        """
        Show the answer grid. If a highlight is given,
        then that entity will be highlighted.
        """
        #draw text
        txt = "Repeat the sequence by pressing the corresponding keys on your keyboard"
        text = visual.TextStim(win=self.win, text= txt, color='#444444', height=0.05)
        text.setPos((0,0.3))
        text.draw()
        
        for k in range(1, self.numOptions+1):
            #draw rectangle
            rect = visual.Rect(self.win, 0.2, 0.2)
            rect.setFillColor(self.color)
            rect.setPos(self.answerPositions[k])
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
            
        self.win.flip()
        
           
