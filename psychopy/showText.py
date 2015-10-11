"""
@author Thomas Churchman

Module that provides easy text display.
"""

from psychopy import visual, core, data, logging, event, sound, gui
from numpy import random

class ShowText:
    """
    Class that provides easy text display.
    """
    
    def __init__(self, win):
        self.win = win
    
    def _display(self, text):
        text = visual.TextStim(win=self.win, text=text, color='#444444', height=0.07)
        text.draw()
        self.win.flip()
    
    def showForXSec(self, text, sec):
        """
        Show text for a given amount of seconds.
        """

        self._display(text)
        core.wait(sec)
        
    def showUntilKeyPressed(self, text, keyList=['space']):
        """
        Show text until the spacebar is pressed.
        """
        
        self._display(text)
        
        
        instructionClock = core.Clock()
        instructionClock.reset()
        
        keyPressed = False
        eventCheckStarted = False
        while not keyPressed:
            t = instructionClock.getTime()
            
            if t >= 0.5:
                # Do not check for events immediatelly, such that people do not accidentally
                # skip the message.
                
                if eventCheckStarted == False:
                    # Remove keyboard events that were sent before the "grace" period had elapsed
                    event.clearEvents(eventType='keyboard')
                    eventCheckStarted = True
                    
                # Check for keys
                theseKeys = event.getKeys(keyList=keyList)
                
                if len(theseKeys) > 0:
                    # A key was pressed, return it
                    return theseKeys[0]
            
            