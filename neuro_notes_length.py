import cv2
import numpy as np
import pandas as pd
import os
from tensorflow import keras
from music21 import converter
from music21.note import Note


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


def locate_symbol(image, count_of_iterations, offset, symbol_type, x_coordinate, y_coordinate, widths, heights,
                  symbol_types, threshold):
    for i in range(count_of_iterations):
        template = cv2.imread('templates/' + str(i+offset) + '.png', 0)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            x_coordinate.append(pt[0])
            y_coordinate.append(pt[1])
            widths.append(w)
            heights.append(h)
            symbol_types.append(symbol_type)


def create_table(gray_img, color_img):
    x_coordinate = []
    y_coordinate = []
    widths = []
    heights = []
    type_of_symbol = []

    locate_symbol(gray_img, 8, 80, 'staff', x_coordinate, y_coordinate, widths, heights, type_of_symbol, 0.85)
    locate_symbol(gray_img, 7, 0, 'note8/note4', x_coordinate, y_coordinate, widths, heights, type_of_symbol, 0.79)
    locate_symbol(gray_img, 10, 20, 'note2', x_coordinate, y_coordinate, widths, heights, type_of_symbol, 0.8)
    locate_symbol(gray_img, 4, 30, 'note1', x_coordinate, y_coordinate, widths, heights, type_of_symbol, 0.65)
    locate_symbol(gray_img, 8, 40, 'flat', x_coordinate, y_coordinate, widths, heights, type_of_symbol, 0.76)    # 0.88
    locate_symbol(gray_img, 6, 50, 'sharp', x_coordinate, y_coordinate, widths, heights, type_of_symbol, 0.8)

    locate_symbol(gray_img, 1, 100, 'pause1', x_coordinate, y_coordinate, widths, heights, type_of_symbol, 0.883)
    locate_symbol(gray_img, 1, 110, 'pause2', x_coordinate, y_coordinate, widths, heights, type_of_symbol, 0.83)
    locate_symbol(gray_img, 1, 111, 'pause2', x_coordinate, y_coordinate, widths, heights, type_of_symbol, 0.8)  # 0.7
    locate_symbol(gray_img, 2, 120, 'pause4', x_coordinate, y_coordinate, widths, heights, type_of_symbol, 0.7)
    locate_symbol(gray_img, 2, 130, 'pause8', x_coordinate, y_coordinate, widths, heights, type_of_symbol, 0.8)

    d = {'x': x_coordinate, 'y': y_coordinate, 'width': widths, 'height': heights, 'symbol': type_of_symbol}
    df = pd.DataFrame(data=d)
    df = df.drop_duplicates(subset=['x'])
    df = df.sort_values(by='x')
    df = df.reset_index(drop=True)
    # print('Dataframe before changing')
    # print(df)

    indexes_for_drop = []
    for i in range(df['x'].size - 1):
        if df.loc[i + 1, 'symbol'] != 'staff' and df.loc[i, 'x'] != 'staff' \
                and df.loc[i + 1, 'x'] - df.loc[i, 'x'] <= 15:
            df.loc[i + 1, 'x'] = df.loc[i, 'x']
            df.loc[i + 1, 'width'] = df.loc[i + 1, 'x'] - df.loc[i, 'x'] + df.loc[i + 1, 'width']
            indexes_for_drop.append(i)
    df.drop(indexes_for_drop, inplace=True)
    df = df.reset_index(drop=True)

    rectangles_of_staff = []
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
    # print('Dataframe with column STATUS')
    # print(df)
    indexes_for_drop = df[df['status'] == 'drop'].index
    df.drop(indexes_for_drop, inplace=True)
    df = df.reset_index(drop=True)
    # print('Dataframe after delete rows with STATUS == drop')
    # print(df)

    for i in range(df['x'].size - 1):
        if df.loc[i, 'status'] == 'start':
            df.loc[i, 'width'] = df.loc[i + 1, 'x'] - df.loc[i, 'x'] + df.loc[i + 1, 'width']
            df.loc[i, 'x'] = df.loc[i, 'x']

    indexes_for_drop = df[df['status'] == 'end'].index
    df.drop(indexes_for_drop, inplace=True)
    df = df.reset_index(drop=True)
    # print('Dataframe after delete rows with STATUS == end')
    # print(df)

    for ind in range(df['x'].size):
        x = df.loc[ind, 'x']
        y = df.loc[ind, 'y']
        width = df.loc[ind, 'width']
        height = df.loc[ind, 'height']
        if df.loc[ind, 'symbol'] == 'sharp' or df.loc[ind, 'symbol'] == 'flat':
            cv2.rectangle(color_img, (x, y), (x + width, y + height), (0, 100, 0), 2)
        elif df.loc[ind, 'symbol'] == 'staff':
            cv2.rectangle(color_img, (x, y), (x + width, y + height), (0, 0, 255), 2)
        elif df.loc[ind, 'symbol'] == 'note8/note4':
            if df.loc[ind - 1, 'symbol'] == 'staff' and df.loc[ind + 1, 'symbol'] == 'staff':   # note4
                cv2.rectangle(color_img, (x, y), (x + width, y + height), (255, 0, 255), 2)
                df.loc[ind, 'symbol'] = 'note4'
            else:
                cv2.rectangle(color_img, (x, y), (x + width, y + height), (220, 0, 100), 2)     # note8
                df.loc[ind, 'symbol'] = 'note8'
        elif df.loc[ind, 'symbol'] == 'note2':
            cv2.rectangle(color_img, (x, y), (x + width, y + height), (0, 255, 255), 2)
        elif df.loc[ind, 'symbol'] == 'note1':
            cv2.rectangle(color_img, (x, y), (x + width, y + height), (0, 130, 255), 2)
        else:
            cv2.rectangle(color_img, (x, y), (x + width, y + height), (255, 130, 0), 2)
    # cv2.imshow('after_finding_all_types', color_img)
    return df


def choose_notes(df, image):
    """ This function choose notes from the whole table """

    notes = []
    for index in range(df.shape[0]):
        if df.symbol[index].startswith('note'):
            notes.append(df.values[index][:4])

    # differ = 0
    notes_images = []
    for note in notes:
        current_note = []
        for y in range(image.shape[0]):
            current_line = []
            for x in range(note[0] + note[2] // 2 - 25, note[0] + note[2] // 2 + 41):
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
    df = create_table(image_gray, image.copy())
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
        keras.layers.Flatten(input_shape=(250, 66)),
        keras.layers.Dense(16500, activation='relu'),
        keras.layers.Dense(1000, activation='relu'),
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
    model.fit(notes_from_all_pictures, notes_from_all_music_files, epochs=100)

    model.save('notes_length.h5')
