"""
@author Thomas Churchman

Module that provides experiment handling. This controls the flow of the experiment
(e.g. the order of the various routines).
"""

from psychopy import visual, core, data, event, logging, sound, gui
from numpy import random
from showText import *
from trialHandler import *
from taskHandlerColor import *
from taskHandlerPosition import *
from taskHandlerColorPosition import *
import sounds

class ExperimentHandler:
    """
    Class that provides experiment handling.
    """
    
    def __init__(self):
        self.win = visual.Window(units='height', color='#ffffff')
        self.showText = ShowText(self.win)
    
    def run(self):
        """
        Run the experiment.
        """
        
        logging.info('Experiment started')
        
        # Welcome message 
        self.showText.showUntilKeyPressed(u"Welcome! Indicate you have read the text by pressing [space].") 
        
        self.familiarizeRoutine()
        
        self.showText.showUntilKeyPressed(u"The experiment will now begin.") 
        
        # TODO: counterbalance instead of randomize
        permutation = numpy.random.permutation(['color', 'position', 'colorPosition']);
        
        for p in permutation:
            if p == 'color':
                trial = TrialHandler(self.win, 2, TaskHandlerColor(self.win))
                trial.run()
            elif p == 'position':
                trial = TrialHandler(self.win, 2, TaskHandlerPosition(self.win))
                trial.run()
            else:
                trial = TrialHandler(self.win, 2, TaskHandlerColorPosition(self.win))
                trial.run()
        
        
        self.showText.showUntilKeyPressed(u"Experiment is complete.") 
        
        logging.info('Experiment finished')
       
    def familiarizeRoutine(self):
        """
        Task familiarization routine.
        """
        answer = self.showText.showUntilKeyPressed(u"Would you like to be familiarized with the tasks? y/n", ['y', 'n']) 
        
        if answer == 'n':
            return
           
        self.showText.showUntilKeyPressed(u"You will now be presented the three tasks. In each task you will have to remember an increasingingly long sequence. Each time you remember the sequence correctly, its length increases by 1. After every presentation, you have to input the correct sequence.")
        self.showText.showUntilKeyPressed(u"When a sequence is going to be presented, you will hear the following sound.");
        sounds.sequencePresentSound.play();
        
        core.wait(1.0);
        self.showText.showUntilKeyPressed(u"When you have to answer a sequence, you will hear the following sound.");
        sounds.sequenceAnswerSound.play();
        core.wait(1.0);
        
        self.showText.showUntilKeyPressed(u"There are three types of sequence tasks you will perform...");
        
        self.showText.showUntilKeyPressed(u"Color.");
        
        colorTask = TaskHandlerColor(self.win)
        colorTask.run()
        
        self.showText.showUntilKeyPressed(u"Position.");
        
        positionTask = TaskHandlerPosition(self.win)
        positionTask.run()
        
        self.showText.showUntilKeyPressed(u"Color + Position");
        
        colorPositionTask = TaskHandlerColorPosition(self.win)
        colorPositionTask.run()
        
       