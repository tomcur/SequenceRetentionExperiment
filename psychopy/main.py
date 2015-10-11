"""
@author Thomas Churchman

Experiment start-up script
"""

from psychopy import logging
from experimentHandler import *

logging.console.setLevel(logging.DEBUG)

eHandler = ExperimentHandler()
eHandler.run()