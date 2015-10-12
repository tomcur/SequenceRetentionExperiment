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
        
        # Experimenter info
        expName = self.showText.askQuestionUntilAnswered(u"Give experimenter name + press [enter]:");
        subjNumber = self.showText.askQuestionUntilAnswered(u"Give subject number + press [enter]:");
        
        # Welcome message 
        self.showText.showUntilKeyPressed(u"Welcome! Indicate you have read the text by pressing [space].") 
        
        self.familiarizeRoutine()
        
        self.showText.showUntilKeyPressed(u"The experiment will now begin.") 
        
        # TODO: counterbalance instead of randomize
        permutation = numpy.random.permutation(['color', 'position', 'colorPosition']);
        
        # Txt file to save data in
        file = open("data" + expName + str(subjNumber) + ".txt", "w")
        file.write("experimenter: " + expName + "\n")
        file.write("subject: " + str(subjNumber) + "\n")
        file.write("order: " + permutation[0] + ", " + permutation[1] + ", " + permutation[2]+"\n")
        
        nrOfTasks = 2 #nr of tasks per condition
        c = 1 #subject is at the c'th condition
        
        # walk through conditions
        for p in permutation:
            if p == 'color':
                trial = TrialHandler(self.win, nrOfTasks, c, TaskHandlerColor(self.win))
                scores = trial.run()
            elif p == 'position':
                trial = TrialHandler(self.win, nrOfTasks, c, TaskHandlerPosition(self.win))
                scores = trial.run()
            else:
                trial = TrialHandler(self.win, nrOfTasks, c, TaskHandlerColorPosition(self.win))
                scores = trial.run()
            #next condition
            c = c + 1 
            # Save data in each condition
            file.write(self.toDataString(p,scores))
        
        file.close()
        
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
        
        self.showText.showUntilKeyPressed(u"The first type is the color sequence task. Press [space] to start with an example.");
        
        colorTask = TaskHandlerColor(self.win)
        colorTask.run()
        
        self.showText.showUntilKeyPressed(u"The second type of sequence tasks is the position sequence task. Press [space] to start with an example.");
        
        positionTask = TaskHandlerPosition(self.win)
        positionTask.run()
        
        self.showText.showUntilKeyPressed(u"The third type of sequence tasks is the color+position sequence task. Press [space] to start with an example.");
        
        colorPositionTask = TaskHandlerColorPosition(self.win)
        colorPositionTask.run()
        
    def toDataString(self, condition, scores):
        """
        Creates data string from the scores from the given condition
        condition = string containing condition name
        scores = list with scores of all tasks within this condition
        """
        
        ff = ""
        for s in scores:
            ff = ff + str(s) + ","
            
        return condition + ":" + ff + "\n"
        

