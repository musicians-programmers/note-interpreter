import sys
import cv2
import numpy as np
import pandas as pd
from midiutil.MidiFile import MIDIFile
import subprocess


def locate_symbol(image, count_of_iterations, offset, type, x_coordinate, y_coordinate, widths, heights, type_of_symbol, threshold):
    for i in range(count_of_iterations):  # note4/note8
        template = cv2.imread('templates/' + str(i+offset) + '.png', 0)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            x_coordinate.append(pt[0])
            y_coordinate.append(pt[1])
            widths.append(w)
            heights.append(h)
            type_of_symbol.append(type)


def create_table(img):
    x_coordinate = []
    y_coordinate = []
    widths = []
    heights = []
    type_of_symbol = []

    locate_symbol(img, 8, 80, 'staff', x_coordinate, y_coordinate, widths, heights, type_of_symbol, 0.85)
    locate_symbol(img, 7, 0, 'note8/note4', x_coordinate, y_coordinate, widths, heights, type_of_symbol, 0.79)
    locate_symbol(img, 10, 20, 'note2', x_coordinate, y_coordinate, widths, heights, type_of_symbol, 0.8)
    locate_symbol(img, 7, 40, 'flat', x_coordinate, y_coordinate, widths, heights, type_of_symbol, 0.88)
    locate_symbol(img, 2, 50, 'sharp', x_coordinate, y_coordinate, widths, heights, type_of_symbol, 0.8)

    d = {'x': x_coordinate, 'y': y_coordinate, 'width': widths, 'height': heights, 'symbol': type_of_symbol}
    df = pd.DataFrame(data=d)
    df = df.drop_duplicates(subset=['x'])
    df = df.sort_values(by='x')
    df = df.reset_index(drop=True)
    print('Dataframe before changing')
    print(df)

    indexes_for_drop =[]
    for i in range(df['x'].size - 1):
        if df.loc[i + 1, 'symbol'] != 'staff' and df.loc[i, 'x'] != 'staff' and df.loc[i + 1, 'x'] - df.loc[i, 'x'] <= 15:
            df.loc[i + 1, 'x'] = df.loc[i, 'x']
            df.loc[i + 1, 'width'] = df.loc[i + 1, 'x'] - df.loc[i, 'x'] + df.loc[i + 1, 'width']
            indexes_for_drop.append(i)
    df.drop(indexes_for_drop, inplace=True)
    df = df.reset_index(drop=True)

    rectangles_of_staff =[]
    for i in range(df['x'].size - 1):
        if df.loc[i, 'symbol'] == 'staff':
            if i == 0:
                rectangles_of_staff.append('start')
            elif df.loc[i - 1, 'symbol'] != 'staff' and df.loc[i + 1, 'symbol'] != 'staff':
                rectangles_of_staff.append('-')
            elif df.loc[i - 1, 'symbol'] != 'staff' and df.loc[i + 1, 'symbol'] == 'staff':
                rectangles_of_staff.append('start')
            elif df.loc[i - 1, 'symbol'] == 'staff' and df.loc[i + 1, 'symbol'] != 'staff':
                rectangles_of_staff.append('end')
            elif df.loc[i - 1, 'symbol'] == 'staff' and df.loc[i + 1, 'symbol'] == 'staff':
                rectangles_of_staff.append('drop')
        else:
            rectangles_of_staff.append('-')

    rectangles_of_staff.append('drop')
    df['status'] = rectangles_of_staff
    print('Dataframe with column STATUS')
    print(df)
    indexes_for_drop = df[df['status'] == 'drop'].index
    df.drop(indexes_for_drop, inplace=True)
    df = df.reset_index(drop=True)
    print('Dataframe after delete rows with STATUS == drop')
    print(df)

    for i in range(df['x'].size - 1):
        if df.loc[i, 'status'] == 'start':
            df.loc[i, 'width'] = df.loc[i + 1, 'x'] - df.loc[i, 'x'] + df.loc[i + 1, 'width']
            df.loc[i, 'x'] = df.loc[i, 'x']

    indexes_for_drop = df[df['status'] == 'end'].index
    df.drop(indexes_for_drop, inplace=True)
    df = df.reset_index(drop=True)
    print('Dataframe after delete rows with STATUS == end')
    print(df)

    for ind in range(df['x'].size):
        x = df.loc[ind, 'x']
        y = df.loc[ind, 'y']
        width = df.loc[ind, 'width']
        height = df.loc[ind, 'height']
        if df.loc[ind, 'symbol'] == 'sharp' or df.loc[ind, 'symbol'] == 'flat':
            cv2.rectangle(img_rgb, (x, y), (x + width, y + height), (0, 100, 0), 2)
        elif df.loc[ind, 'symbol'] == 'staff':
            cv2.rectangle(img_rgb, (x, y), (x + width, y + height), (0, 0, 255), 2)
        elif df.loc[ind, 'symbol'] == 'note8/note4':
            if df.loc[ind - 1, 'symbol'] == 'staff' and df.loc[ind + 1, 'symbol'] == 'staff': #note4
                cv2.rectangle(img_rgb, (x, y), (x + width, y + height), (255, 0, 255), 2)
                df.loc[ind, 'symbol'] = 'note4'
            else:
                cv2.rectangle(img_rgb, (x, y), (x + width, y + height), (220, 0, 100), 2) #note8
                df.loc[ind, 'symbol'] = 'note8'
        elif df.loc[ind, 'symbol'] == 'note2':
            cv2.rectangle(img_rgb, (x, y), (x + width, y + height), (0, 255, 255), 2)
    cv2.imwrite('res.png', img_rgb)
    return df


def find_note_height(df):
    height = 0
    y_start = 0
    df = df.drop(columns=['status'])
    for ind in range(df['x'].size):
        if df.loc[ind, 'symbol'] == 'staff':
            height = df.loc[ind, 'height']
            y_start = df.loc[ind, 'y']
            break

    middle = y_start + round(height / 2)
    step = round(height / 24)

    middles = [middle]
    for i in range(7):
        middles.append(middle + 2 * step * (i + 1))
        middles.append(middle - 2 * step * (i + 1))
    print(len(middles))
    middles.sort()
    note_height = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    note_meaning = ['h5', 'a5', 'g5', 'f5', 'e5', 'd5', 'c5', 'h4', 'a4', 'g4', 'f4', 'e4', 'd4', 'c4', 'h3']
    note_for_midi = [83, 81, 79, 77, 76, 74, 72, 71, 69, 67, 65, 64, 62, 60, 59]

    print(len(note_height))
    note_classifier = {'middles': middles, 'note_height': note_height, 'note_meaning': note_meaning, 'note_midi': note_for_midi}

    # check is everything ok with notes height
    # x = 1340
    # for i in range(len(middles)):
    #     y = middles[i]
    #     cv2.rectangle(img_rgb, (x + 20 * i, y - step), (x + 20 * i + 10, y + step), (0, 0, 150), 2)

    cv2.imwrite('result.png', img_rgb)
    classifier = pd.DataFrame(data=note_classifier)
    print('Dataframe note classifier')
    print(classifier)
    note_centers =[]
    for ind in range(df['x'].size):
        center = df.loc[ind, 'y'] + int(df.loc[ind, 'height'] / 2)
        note_centers.append(center)
    df['centers'] = note_centers
    print('Dataframe with centers')
    print(df)

    notes = []
    note_midi = []
    for i in range(df['x'].size):
        if df.loc[i, 'symbol'] == 'staff':
            notes.append('-')
            note_midi.append(0)
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


def open_file(path):
    cmd = {'linux': 'eog', 'win32': 'explorer', 'darwin': 'open'}[sys.platform]
    subprocess.run([cmd, path])


def to_midi(df):
    indexes_for_drop = df[df['symbol'] == 'staff'].index
    df.drop(indexes_for_drop, inplace=True)
    df = df.reset_index(drop=True)
    print('Dataframe without staff')
    print(df)

    midi = MIDIFile(1)

    track = 0
    time = 0
    channel = 0
    volume = 100

    midi.addTrackName(track, time, "Track")
    midi.addTempo(track, time, 140)

    for i in range(df['x'].size):
        if df.loc[i, 'symbol'] == 'note2' or df.loc[i, 'symbol'] == 'note4' or df.loc[i, 'symbol'] == 'note8':
            duration = 0
            if df.loc[i, 'symbol'] == 'note2':
                duration = 2
            elif df.loc[i, 'symbol'] == 'note4':
                duration = 1
            elif df.loc[i, 'symbol'] == 'note8':
                duration = 0.5
            pitch = df.loc[i, 'notes_midi']
            midi.addNote(track, channel, pitch, time, duration, volume)
            time += duration

    binfile = open("output.mid", 'wb')
    midi.writeFile(binfile)
    binfile.close()
    open_file('output.mid')


if __name__ == '__main__':
    img_rgb = cv2.imread('samples/copy.png')

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    print(img_gray.shape)

    df = create_table(img_gray)
    df = find_note_height(df)
    to_midi(df)





