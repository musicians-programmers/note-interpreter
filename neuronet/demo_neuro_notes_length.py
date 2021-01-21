import numpy as np
from tensorflow import keras

from neuronet.neuro_notes_length import notes_from_image
from neuronet.neuro_notes_length import note_durations


if __name__ == '__main__':
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(250, 50)),
        keras.layers.Dense(12500, activation='relu'),
        keras.layers.Dense(1000, activation='relu'),
        keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.load_weights('neuronet/notes_length.h5')

    notes = notes_from_image('samples/picture_1.png')  # path to picture with notes
    prediction = model.predict(notes)

    for i in prediction:
        print(note_durations[np.where(i == 1)[0][0]])
