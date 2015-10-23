"""
@author Thomas Churchman

Some sounds for use in the experiment.
"""

from psychopy import sound

sequencePresentSound = sound.SoundPyo(octave=4)
sequenceAnswerSound = sound.SoundPyo(octave=6)
buttonClickSound = sound.SoundPyo(octave=5, secs=0.075)
buttonClickSound.setVolume(0.5)