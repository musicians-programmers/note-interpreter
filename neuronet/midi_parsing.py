import numpy as np
from music21 import converter
from music21.note import Note


def notes_from_midi(path, durations):
    """ This function return notes list from music """

    midi = converter.parse(path)
    notes = []
    for element in midi.recurse():
        if type(element) == Note and element.nameWithOctave != 'F#9':
            notes.append([durations.index(element.duration.fullName)])

    notes = np.array(notes, dtype=np.uint8)
    return notes
