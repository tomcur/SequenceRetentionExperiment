"""
@author Thomas Churchman, Diede Kemper

Module that provides experiment handling. This controls the flow of the experiment
(e.g. the order of the various routines).
"""

from psychopy import visual, core, data, event, logging, sound, gui
from itertools import *
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
        subjNr = self.showText.askQuestionUntilAnswered(u"Give subject number + press [enter]:");
        
        # Welcome message 
        self.showText.showUntilKeyPressed(u"Welcome! Press any key to indicate you have read the text.") 
        
        self.familiarizeRoutine()
        
        self.showText.showUntilKeyPressed(u"Press any key to start the experiment.") 
        
        # decide order of conditions
        order = self.giveOrder(subjNr)
        orderStr = order[0] + "-" + order[1] + "-" + order[2]
        
        # Txt file to save data in
        file = open("data" + expName + str(subjNr) + ".csv", "w")
        file.write("Nr,exp,order,cond,trial,score\n")
        
        nrOfTasks = 4 #nr of tasks per condition
        c = 1 #subject is at the c'th condition
        
        # walk through conditions
        for p in order:
            if p == 'c':
                self.familiarizeRoutine("color")
                trial = TrialHandler(self.win, nrOfTasks, c, "color", TaskHandlerColor(self.win))
                scores = trial.run()
            elif p == 'p':
                self.familiarizeRoutine("position")
                trial = TrialHandler(self.win, nrOfTasks, c, "position",TaskHandlerPosition(self.win))
                scores = trial.run()
            else:
                self.familiarizeRoutine("colorposition")
                trial = TrialHandler(self.win, nrOfTasks, c, "color+position", TaskHandlerColorPosition(self.win))
                scores = trial.run()
            #next condition
            c = c + 1 
            # Save data in each condition
            file.write(self.toDataString(subjNr,expName, orderStr, p, scores))
        
        file.close()
        
        self.showText.showUntilKeyPressed(u"The experiment is complete. Thank you!") 
        
        logging.info('Experiment finished')
        
        
    def familiarizeRoutine(self, condition="start"):
        """
        Task familiarization routine.
        """
        if condition == "start":
        
            self.showText.showUntilKeyPressed(u"In this experiment you have to perform three tasks. In each task you will have to remember an increasingly long sequence. Each time you remember the sequence correctly, its length increases by 2. After every presentation, you have to input the correct sequence.")
            self.showText.showUntilKeyPressed(u"When a sequence is going to be presented, you will hear the following sound.");
            sounds.sequencePresentSound.play();
            
            core.wait(1.0);
            self.showText.showUntilKeyPressed(u"When you have to answer a sequence, you will hear the following sound.");
            sounds.sequenceAnswerSound.play();
            core.wait(1.0);
            
            self.showText.showUntilKeyPressed(u"There are three types of sequence tasks you will perform. The color sequence task, the position sequence task and the color+position sequence task. Before performing each task, you will be given an example task to practice with. ");
            
        elif condition == "color":
        
            self.showText.showUntilKeyPressed(u"You will now perform the color sequence task. Press any key to start with an example.");
            
            colorTask = TaskHandlerColor(self.win, True)
            length = colorTask.run()
            
            while(length < 6):
                self.showText.showUntilKeyPressed(u"Please practice the color sequence task again. Press any key to start.");
                length = colorTask.run()
            
            self.showText.showUntilKeyPressed(u"You seem to understand this task. Press any key to start with this task for the experiment.");
        
        elif condition == "position":
        
            self.showText.showUntilKeyPressed(u"You will now perform the position sequence task. Press any key to start with an example.");
            
            positionTask = TaskHandlerPosition(self.win, True)
            length = positionTask.run()
            
            while(length < 6):
                self.showText.showUntilKeyPressed(u"Please practice the position sequence task again. Press any key to start.");
                length = positionTask.run()
            
            self.showText.showUntilKeyPressed(u"You seem to understand this task. Press any key to start with this task for the experiment.");
        
        elif condition == "colorposition":
        
            self.showText.showUntilKeyPressed(u"You will now perform the color+position sequence task. Press any key to start with an example.");
            
            colorPositionTask = TaskHandlerColorPosition(self.win, True)
            length = colorPositionTask.run()
            
            while(length < 6):
                self.showText.showUntilKeyPressed(u"Please practice the color+position sequence task again. Press any key to start.");
                length = colorPositionTask.run()
                
            self.showText.showUntilKeyPressed(u"You seem to understand this task. Press any key to start with this task for the experiment.");
        
        else:
            return;
        
        
    def toDataString(self, subjNr, expName, order,condition, scores):
        """
        Creates data string from the scores from the given condition
        condition = string containing condition name
        scores = list with scores of all tasks within this condition
        """
        trial = 1
        ff = ""
        for s in scores:
            ff = ff + subjNr + "," + expName + "," + order + "," + condition + "," + str(trial) + "," + str(s) + "\n"
            trial = trial + 1
            
        return ff
        
    def giveOrder(self,subjNr):
        """
        Decides in which order the conditions will appear for this subject. A counterbalansing
        method is used based on the subject number.
        """
        orders = list(permutations(["c","p","cp"]))
        index = (int(float(subjNr))-1)%6
        return orders[index]
        

