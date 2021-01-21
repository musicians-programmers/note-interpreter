import os

import cv2
import numpy as np
from music21 import converter
from music21.note import Note
from tensorflow import keras

from location import create_table


def image_increase_height(image, height):
    """ This function increases inputted image to height by adding white lines """

    white_line = []
    for _ in range(image.shape[1]):
        white_line.append([255, 255, 255])
    white_line = np.array(white_line)

    upper_lines_number = height - image.shape[0]
    lower_lines_number = upper_lines_number // 2
    if upper_lines_number % 2 == 0:
        upper_lines_number //= 2
    else:
        upper_lines_number = lower_lines_number + 1

    new_image = []
    for line in range(height):
        if line < upper_lines_number or line >= height - lower_lines_number:
            new_image.append(white_line)
        else:
            new_image.append(image[line - upper_lines_number])
    new_image = np.array(new_image)
    new_image = new_image.astype(np.uint8)
    return new_image


def choose_notes(df, image):
    """ This function choose notes from the whole table """

    notes = []
    for i in range(df.shape[0]):
        if df.symbol[i].startswith('note'):
            notes.append(df.values[i][:4])

    # differ = 0
    notes_images = []
    for note in notes:
        current_note = []
        for y in range(image.shape[0]):
            current_line = []
            for x in range(note[0] + note[2] // 2 - 20, note[0] + note[2] // 2 + 30):
                if x > image.shape[1] - 1:
                    current_line.append(255)
                else:
                    current_line.append(image[y][x])
            current_line = np.array(current_line, dtype=np.uint8)
            current_note.append(current_line)
            # image[y][note[0] + note[2] // 2 - 25] = (255 - differ, 255, differ)
            # image[y][note[0] + note[2] // 2 + 25] = (255 - differ, 255, differ)
        current_note = np.array(current_note)
        notes_images.append(current_note)
        # differ += 80
        # if differ == 320:
        #     differ = 0

    notes_images = np.array(notes_images)
    return notes_images


def notes_from_image(path):
    """ This function return notes list from image """

    image = cv2.imread(path)
    image = image_increase_height(image, 250)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    df = create_table(image_gray, image.copy(), '../')
    notes = choose_notes(df, image_gray.copy())
    return np.array(notes)


def notes_from_midi(path, durations):
    """ This function return notes list from music """

    midi = converter.parse(path)
    notes = []
    for element in midi.recurse():
        if type(element) == Note:
            notes.append([durations.index(element.duration.fullName)])

    notes = np.array(notes, dtype=np.uint8)
    return notes


note_durations = ['Whole',
                  'Dotted Whole',
                  'Half',
                  'Dotted Half',
                  'Quarter',
                  'Dotted Quarter',
                  'Eighth',
                  'Dotted Eighth',
                  '16th',
                  'Dotted 16th']

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

    path_to_dataset = '../datasets/made_from_primus_dataset/train/'
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
    model.fit(notes_from_all_pictures, notes_from_all_music_files, epochs=100)

    model.save('notes_length.h5')
