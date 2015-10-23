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
    
    numOptions = 4
    
    def __init__(self, win, tryout=False):
        TaskHandler.__init__(self, win, tryout)
    
    def startText(self):
        """
        The text to show when the task starts.
        """
        self.showText.showForXSec(u"Remember the following position sequence:", 1.5)
    
    def present(self, stimulus=None):
        """
        Present the stimulus grid.
        """
        if stimulus == None:
            # Show non-stimulus grid
            self._showGrid()
        else:
            # Show stimulus on grid
            self._showGrid()
            core.wait(0.35)
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
                rect.setFillColor(self.highlightColor)
                
            rect.draw()
            
        self.win.flip()
        
    def _populateButtons(self):
        """
        Function is called when buttons have to be registered (i.e.,
        rects of button positions should be generated and registered)
        """
        for k in range(1, self.numOptions+1):
            rect = visual.Rect(self.win, 0.2, 0.2)
            rect.setPos(self.answerPositions[k])
            self._registerButton(rect, k)
    
        
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
            rect.setFillColor(self.color)
            rect.setPos(self.answerPositions[k])
            rect.setLineWidth(0)
            if highlight == k:
                rect.setFillColor(self.highlightColor)
                if click:
                    rect.setLineWidth(10)
                    rect.setLineColor(self.lineColor)
                
            rect.draw()
            
        self.win.flip()
        