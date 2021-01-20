import cv2
import pandas as pd
from neuronet.neuro_notes_length import image_increase_height, choose_notes, note_durations
from tensorflow.keras.models import load_model


def find_note_height(img, df):
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
    for i in range(7):
        middles.append(middle + 2 * step * (i + 1))
        middles.append(middle - 2 * step * (i + 1))
    print(len(middles))
    middles.sort()
    note_height = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    note_meaning = ['H5', 'A5', 'G5', 'F5', 'E5', 'D5', 'C5', 'H4', 'A4', 'G4', 'F4', 'E4', 'D4', 'C4', 'H3']
    note_for_midi = [83, 81, 79, 77, 76, 74, 72, 71, 69, 67, 65, 64, 62, 60, 59]

    print(len(note_height))
    note_classifier = {'middles': middles, 'note_height': note_height, 'note_meaning': note_meaning,
                       'note_midi': note_for_midi}

    # check is everything ok with notes height
    # x = 500
    # for i in range(len(middles)):
    #     y = middles[i]
    #     cv2.rectangle(img_rgb, (x + 20 * i, int(y - step)), (x + 20 * i + 10, int(y + step)), (0, 0, 150), 2)

    # cv2.imwrite('result.png', img)
    classifier = pd.DataFrame(data=note_classifier)
    print('Dataframe note classifier')
    print(classifier)
    note_centers = []
    for ind in range(df['x'].size):
        center = df.loc[ind, 'y'] + df.loc[ind, 'height'] / 2
        note_centers.append(center)
    df['centers'] = note_centers
    print('Dataframe with centers')
    print(df)

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
    print(len(notes))
    df['notes'] = notes
    df['notes_midi'] = note_midi
    print('Dataframe with notes')
    print(df)
    return df


def find_notes_length(table, image_color):
    """ This function find length for all found notes """

    model = load_model('neuronet/notes_length.h5')

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
            if table.symbol[i] == 'note8' or table.symbol[i] == 'note4':
                table.symbol[i] = note_durations[all_length[index]]
            elif table.symbol[i] == 'note2':
                table.symbol[i] = 'Half'
            else:
                table.symbol[i] = 'Whole'
            index += 1
