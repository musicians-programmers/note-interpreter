import cv2
import numpy as np

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
