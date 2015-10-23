"""
@author Thomas Churchman, Diede Kemper

Module that provides a color task handler.
"""

from psychopy import core, visual, event
from taskHandler import *
import numpy

class TaskHandlerColor(TaskHandler):
    """
    Class implementing a color task.
    """
    numOptions = 4
    
    # x-positions answer buttons will appear in
    answerPositionsX = [
        -0.375, 
        -0.125,
        0.125,
        0.375
    ]
    
    # Range of y-positions answer buttons will appear in
    answerPositionYRange = (-0.35, 0.15)
    
    buttonPositions = [];
    
    def __init__(self, win, tryout=False):
        TaskHandler.__init__(self, win, tryout)
    
    def startText(self):
        """
        The text to show when the task starts.
        """
        self.showText.showForXSec(u"Remember the following color sequence:", 1.5)
    
    def present(self, stimulus=None):
        """
        Present the stimulus grid.
        """
        if stimulus == None:
            # Present blank screen
            self.win.flip()
        else:
            # Present blank screen
            self.win.flip()
            core.wait(0.35)
            
            # Present stimulus
            rect = visual.Rect(self.win, 0.5, 0.5)
            rect.setFillColor(self.colors[stimulus])
            rect.draw()
            self.win.flip()
           
           
    def _populateButtons(self):
        """
        Function is called when buttons have to be registered (i.e.,
        rects of button positions should be generated and registered)
        """
        self.buttonPositions = []
        
        lowY = self.answerPositionYRange[0]
        highY = self.answerPositionYRange[1]
        
        permutation = numpy.random.permutation(len(self.answerPositionsX))
        
        for p in range(0,self.numOptions):
            button = permutation[p]+1
            xPos = self.answerPositionsX[p]
        
            pos = (xPos, (highY - lowY) * numpy.random.ranf() + lowY)
            self.buttonPositions.append((button, pos))
            
            rect = visual.Rect(self.win, 0.2, 0.2)
            rect.setPos(pos)
            
            self._registerButton(rect, button)
        
    def _showAnswerGrid(self, highlight=None, click=False):
        """
        Show the answer grid. If a highlight is given,
        then that entity will be highlighted.
        """
        #draw text
        txt = "Repeat the sequence by clicking on the corresponding buttons"
        text = visual.TextStim(win=self.win, text= txt, color='#444444', height=0.05)
        text.setPos((0,0.3))
        text.draw()
        
        p = 1
        
        for (button, pos) in self.buttonPositions:
            #draw rectangle
            rect = visual.Rect(self.win, 0.2, 0.2)
            rect.setFillColor(self.colors[button])
            rect.setPos(pos)
            rect.setLineWidth(0)
            if highlight == button:
                rect.setLineWidth(2)
                rect.setLineColor(self.lineColor)
                if click:
                    rect.setFillColor(self.highlightColors[button])
                
            rect.draw()
            
            p = p + 1
            
        self.win.flip()