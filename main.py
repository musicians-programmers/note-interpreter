import sys
import cv2
from midiutil.MidiFile import MIDIFile
import subprocess
from location import create_table
from reading import find_note_height


def open_file(path):
    cmd = {'linux': 'eog', 'win32': 'explorer', 'darwin': 'open'}[sys.platform]
    subprocess.run([cmd, path])


def search(array, elem):
    for i in range(len(array)):
        if array[i] == elem:
            return True
    return False


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

    flats = []
    sharps = []
    for i in range(df['x'].size):  # key signs
        if df.loc[i, 'symbol'] == 'flat':
            flats.append(df.loc[i, 'notes_midi'])
            flats.append(df.loc[i, 'notes_midi'] - 12)
            flats.append(df.loc[i, 'notes_midi'] + 12)
        elif df.loc[i, 'symbol'] == 'sharp':
            sharps.append(df.loc[i, 'notes_midi'])
            sharps.append(df.loc[i, 'notes_midi'] - 12)
            sharps.append(df.loc[i, 'notes_midi'] + 12)
        elif df.loc[i, 'symbol'] == 'note2' or df.loc[i, 'symbol'] == 'note4' or df.loc[i, 'symbol'] == 'note8':
            break

    for i in range(df['x'].size):
        if df.loc[i, 'symbol'] == 'note1' or df.loc[i, 'symbol'] == 'note2' or df.loc[i, 'symbol'] == 'note4' \
                or df.loc[i, 'symbol'] == 'note8':
            if search(flats, df.loc[i, 'notes_midi']):
                df.loc[i, 'notes'] = 'b' + df.loc[i, 'notes']
                df.loc[i, 'notes_midi'] -= 1
            if search(sharps, df.loc[i, 'notes_midi']):
                df.loc[i, 'notes'] = '#' + df.loc[i, 'notes']
                df.loc[i, 'notes_midi'] += 1

    print('Dataframe for play')
    print(df)

    for i in range(df['x'].size):
        if df.loc[i, 'symbol'] != 'staff' and df.loc[i, 'symbol'] != 'sharp' and df.loc[i, 'symbol'] != 'flat':
            duration = 0
            if df.loc[i, 'symbol'] == 'note1':
                duration = 4
            elif df.loc[i, 'symbol'] == 'note2':
                duration = 2
            elif df.loc[i, 'symbol'] == 'note4':
                duration = 1
            elif df.loc[i, 'symbol'] == 'note8':
                duration = 0.5
            elif df.loc[i, 'symbol'] == 'pause1':
                duration = 4
            elif df.loc[i, 'symbol'] == 'pause2':
                duration = 2
            elif df.loc[i, 'symbol'] == 'pause4':
                duration = 1
            elif df.loc[i, 'symbol'] == 'pause8':
                duration = 0.5
            pitch = df.loc[i, 'notes_midi']
            midi.addNote(track, channel, pitch, time, duration, volume)
            time += duration

    file = open("output.mid", 'wb')
    midi.writeFile(file)
    file.close()
    open_file('output.mid')


if __name__ == '__main__':
    img_rgb = cv2.imread('samples/from_dataset16.png')

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    print(img_gray.shape)

    notes_table = create_table(img_gray, img_rgb)
    notes_table = find_note_height(img_rgb, notes_table)
    to_midi(notes_table)
