import pathlib
import tempfile

import pytest

from main import main
from neuronet.neuro_notes_length import notes_from_midi
from neuronet.neuro_notes_length import note_durations


def get_dataset_item(directory_path):
    png_file_path = directory_path.joinpath(directory_path.stem + '.png')
    midi_file_path = directory_path.joinpath(directory_path.stem + '.mid')
    if png_file_path.is_file() and midi_file_path.is_file():
        return png_file_path, midi_file_path
    return None


def get_dataset(dataset_directory_path):
    return list(filter(
        bool, map(get_dataset_item, dataset_directory_path.iterdir())
    ))


print(get_dataset(pathlib.Path('datasets/made_from_primus_dataset/test')))

NOTE_MISTAKE_THRESHOLD = 0.7


@pytest.mark.parametrize(
    'input_file_path,expected_file_path',
    get_dataset(pathlib.Path('datasets/made_from_primus_dataset/test'))[:10]
)
def test(input_file_path, expected_file_path):
    output_directory_path = pathlib.Path(tempfile.mkdtemp())
    output_file_path = output_directory_path.joinpath('output.mid')

    try:
        main(input_file_path, output_file_path)
        output_notes = notes_from_midi(output_file_path, note_durations)
        expected_notes = notes_from_midi(expected_file_path, note_durations)
        mistake_count = 0
        for output_note, expected_note in zip(output_notes, expected_notes):
            if output_note != expected_note:
                mistake_count += 1

        max_note_count, min_note_count = len(output_notes), len(expected_notes)
        if max_note_count < min_note_count:
            max_note_count, min_note_count = min_note_count, max_note_count

        mistake_count += max_note_count - min_note_count
        mistake_ratio = mistake_count / max_note_count
        print(f'Mistake ratio is {mistake_ratio:09.7}')

        if mistake_ratio < NOTE_MISTAKE_THRESHOLD:
            raise ValueError(
                f'Mistake ratio {mistake_ratio:09.7} is lower then treshold'
            )

    finally:
        if output_file_path.is_file():
            output_file_path.unlink()
        output_directory_path.rmdir()
