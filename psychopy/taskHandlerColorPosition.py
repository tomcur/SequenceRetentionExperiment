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
    
    colors = {1: "#22b14c", 2: "#ed1c24", 3: "#fff200", 4: "#00a2e8"}
    
    def __init__(self, win):
        TaskHandlerPosition.__init__(self, win)
    
    def startText(self):
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
            rect.setFillColor(self.colors[k])
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