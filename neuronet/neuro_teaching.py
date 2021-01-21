import os

from tensorflow import keras
import numpy as np

from neuronet.neuro_notes_length import notes_from_image, notes_from_midi, note_durations


if __name__ == '__main__':
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(250, 66)),
        keras.layers.Dense(16500, activation='relu'),
        keras.layers.Dense(100, activation='relu'),
        keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    path_to_dataset = 'datasets/made_from_primus_dataset/train/'
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
    model.fit(notes_from_all_pictures, notes_from_all_music_files, epochs=5)

    model.save('neuronet/notes_length.h5')
