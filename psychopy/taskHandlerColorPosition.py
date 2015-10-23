"""
@author Thomas Churchman

Module that provides a color + position task handler.
"""

from psychopy import core, visual, event
from taskHandlerPosition import *
import numpy

class TaskHandlerColorPosition(TaskHandlerPosition):
    """
    Class implementing a color + position task.
    """
    
    def __init__(self, win, tryout=False):
        TaskHandlerPosition.__init__(self, win, tryout)
    
    def startText(self):
        """
        The text to show when the task starts.
        """
        self.showText.showForXSec(u"Remember the following color and position sequence:", 1.5)
           
    def _showGrid(self, highlight=None):
        """
        Show the grid. If a highlight is given,
        then that entity will be highlighted.
        """
        for k in range(1, self.numOptions+1):
            rect = visual.Rect(self.win, 0.35, 0.35)
            rect.setFillColor(self.colors[k])
            rect.setPos(self.positions[k])
            rect.setLineWidth(0)
            if highlight == k:
                rect.setFillColor(self.highlightColors[k])
                
            rect.draw()
            
        self.win.flip()

    def _showAnswerGrid(self,highlight=None,click=False):
        """
        Show the answer grid. If a highlight is given,
        then that entity will be highlighted.
        """
        #draw text
        txt = "Repeat the sequence by clicking on the corresponding buttons"
        text = visual.TextStim(win=self.win, text= txt, color='#444444', height=0.05)
        text.setPos((0,0.3))
        text.draw()
        
        for k in range(1, self.numOptions+1):
            #draw rectangle
            rect = visual.Rect(self.win, 0.2, 0.2)
            rect.setFillColor(self.colors[k])
            rect.setPos(self.answerPositions[k])
            rect.setLineWidth(0)
            if highlight == k:
                rect.setLineWidth(2)
                rect.setLineColor(self.lineColor)
                if click:
                    rect.setFillColor(self.highlightColors[k])
                
            rect.draw()
            
        self.win.flip()
        