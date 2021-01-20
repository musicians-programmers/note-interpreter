from tensorflow.keras.models import load_model
from neuro_notes_length import notes_from_image
from neuro_notes_length import note_durations
import numpy as np


if __name__ == '__main__':
    model = load_model('notes_length.h5')

    notes = notes_from_image('samples/picture_1.png')  # path to picture with notes
    prediction = model.predict(notes)

    for i in prediction:
        print(note_durations[np.where(i == 1)[0][0]])
