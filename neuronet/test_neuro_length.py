import os

from tensorflow import keras
import numpy as np

from neuronet.neuro_notes_length import notes_from_image, note_durations
from neuronet.midi_parsing import notes_from_midi


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
    model.load_weights('notes_length.h5')

    path_to_dataset = '../datasets/made_from_primus_dataset/test/'
    directory = os.listdir(path_to_dataset)
    notes_from_all_pictures = []
    notes_from_all_music_files = []
    index = 1
    for subdir in directory:
        print('File {0}'.format(index))
        index += 1
        notes_from_picture = notes_from_image(path_to_dataset + subdir + '/' + subdir + '.png')
        notes_from_music = notes_from_midi(path_to_dataset + subdir + '/' + subdir + '.mid',
                                           note_durations)
        for pict_note in notes_from_picture:
            notes_from_all_pictures.append(pict_note)
        for music_note in notes_from_music:
            notes_from_all_music_files.append(music_note)

    notes_from_all_pictures = np.array(notes_from_all_pictures) / 255.0
    notes_from_all_music_files = np.array(notes_from_all_music_files)
    prediction = model.predict(notes_from_all_pictures)
    result = []
    for i in prediction:
        maximum = 0
        index = 0
        for j in range(len(i)):
            if i[j] > maximum:
                maximum = i[j]
                index = j
        result.append(index)

    # Testing
    mistakes = 0
    notes_variants = [0]*10
    notes_mistakes = [0]*10
    for i in range(len(notes_from_all_music_files)):
        notes_variants[notes_from_all_music_files[i][0]] += 1
        if result[i] != notes_from_all_music_files[i][0]:
            mistakes += 1
            notes_mistakes[notes_from_all_music_files[i][0]] += 1

    print("Total notes: {0}. Percent of right evaluations {1}%".format(len(notes_from_all_music_files),
          (len(notes_from_all_music_files) - mistakes) * 100 / len(notes_from_all_music_files)))
    for i in range(9):
        print("Total {0}: {1}. Percent of right evaluations {2}%".format(
            note_durations[i],
            notes_variants[i],
            (notes_variants[i] - notes_mistakes[i]) * 100 / notes_variants[i]
        ))
