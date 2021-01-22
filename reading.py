import cv2
import pandas as pd
from tensorflow import keras

from neuronet.neuro_notes_length import image_increase_height, choose_notes, note_durations


def find_note_height(df):
    """ This function defines the pitch of a notes """

    height = 0
    y_start = 0
    df = df.drop(columns=['status'])
    for ind in range(df['x'].size):
        if df.loc[ind, 'symbol'] == 'staff':
            height = df.loc[ind, 'height']
            y_start = df.loc[ind, 'y']
            break

    middle = y_start + round(height / 2)
    step = height / 24

    middles = [middle]
    for i in range(9):
        middles.append(middle + 2 * step * (i + 1))
        middles.append(middle - 2 * step * (i + 1))

    middles.sort()
    note_height = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    note_meaning = ['D6', 'C6', 'H5', 'A5', 'G5', 'F5', 'E5', 'D5', 'C5', 'H4', 'A4', 'G4', 'F4', 'E4', 'D4', 'C4',
                    'H3', 'A3', 'G3']
    note_for_midi = [86, 84, 83, 81, 79, 77, 76, 74, 72, 71, 69, 67, 65, 64, 62, 60, 59, 57, 55]

    note_classifier = {'middles': middles, 'note_height': note_height, 'note_meaning': note_meaning,
                       'note_midi': note_for_midi}

    classifier = pd.DataFrame(data=note_classifier)

    note_centers = []
    for ind in range(df['x'].size):
        center = df.loc[ind, 'y'] + df.loc[ind, 'height'] / 2
        note_centers.append(center)
    df['centers'] = note_centers

    notes = []
    note_midi = []
    for i in range(df['x'].size):
        if df.loc[i, 'symbol'] == 'staff' or df.loc[i, 'symbol'] == 'pause1' or df.loc[i, 'symbol'] == 'pause2' or \
                df.loc[i, 'symbol'] == 'pause4' or df.loc[i, 'symbol'] == 'pause8':
            notes.append('-')
            note_midi.append(126)
        else:
            center = df.loc[i, 'centers']
            flag = 0
            for j in range(len(classifier.index)):
                m = classifier.loc[j, 'middles']
                if (center >= m - step) and (center < m + step):
                    notes.append(classifier.loc[j, 'note_meaning'])
                    note_midi.append(classifier.loc[j, 'note_midi'])
                    flag = 1
                    break
            if flag == 0:
                notes.append('not recognized')
                note_midi.append(60)
    df['notes'] = notes
    df['notes_midi'] = note_midi
    return df


def find_notes_length(table, image_color):
    """ This function find length for all found notes """

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

    image_color = image_increase_height(image_color, 250)
    image_gray = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)
    notes = choose_notes(table, image_gray)
    prediction = model.predict(notes)

    all_length = []
    for i in prediction:
        maximum = 0
        index = 0
        for j in range(len(i)):
            if i[j] > maximum:
                maximum = i[j]
                index = j
        all_length.append(index)

    index = 0
    for i in range(table.shape[0]):
        if table.symbol[i].startswith('note'):
            table.symbol[i] = note_durations[all_length[index]]
            index += 1
