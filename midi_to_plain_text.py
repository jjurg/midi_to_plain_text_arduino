import subprocess
import sys

try:
    filename = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else 'text'
except:
    print("Usage: python3 {} filename.mid [text|arduino]".format(sys.argv[0]))
    exit(1)

try:
    from mido import MidiFile
except ImportError:
    package = 'mido'
    # Use pip to install the package
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    from mido import MidiFile

midi_note_dict = {
    0: 'rest',
    21: 'A0', 22: 'A#0', 23: 'B0',
    24: 'C1', 25: 'C#1', 26: 'D1', 27: 'D#1', 28: 'E1', 29: 'F1', 30: 'F#1', 31: 'G1', 32: 'G#1', 33: 'A1', 34: 'A#1', 35: 'B1',
    36: 'C2', 37: 'C#2', 38: 'D2', 39: 'D#2', 40: 'E2', 41: 'F2', 42: 'F#2', 43: 'G2', 44: 'G#2', 45: 'A2', 46: 'A#2', 47: 'B2',
    48: 'C3', 49: 'C#3', 50: 'D3', 51: 'D#3', 52: 'E3', 53: 'F3', 54: 'F#3', 55: 'G3', 56: 'G#3', 57: 'A3', 58: 'A#3', 59: 'B3',
    60: 'C4', 61: 'C#4', 62: 'D4', 63: 'D#4', 64: 'E4', 65: 'F4', 66: 'F#4', 67: 'G4', 68: 'G#4', 69: 'A4', 70: 'A#4', 71: 'B4',
    72: 'C5', 73: 'C#5', 74: 'D5', 75: 'D#5', 76: 'E5', 77: 'F5', 78: 'F#5', 79: 'G5', 80: 'G#5', 81: 'A5', 82: 'A#5', 83: 'B5',
    84: 'C6', 85: 'C#6', 86: 'D6', 87: 'D#6', 88: 'E6', 89: 'F6', 90: 'F#6', 91: 'G6', 92: 'G#6', 93: 'A6', 94: 'A#6', 95: 'B6',
    96: 'C7', 97: 'C#7', 98: 'D7', 99: 'D#7', 100: 'E7', 101: 'F7', 102: 'F#7', 103: 'G7', 104: 'G#7', 105: 'A7', 106: 'A#7', 107: 'B7',
    108: 'C8'
}

midi = MidiFile(filename)

notes = []
current_notes = {}
clocks_per_quarter = midi.ticks_per_beat

print("Parsing MIDI file...")
for track in midi.tracks:
    current_time = 0
    for msg in track:
        current_time += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
            current_notes[msg.note] = current_time
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            if msg.note in current_notes:
                start_time = current_notes.pop(msg.note)
                duration = current_time - start_time
                note = midi_note_dict.get(msg.note, 'unknown')
                notes.append((note, duration))
                if note == 'unknown':
                    print(f"Warning: Missing note for MIDI value {msg.note}")

# Now notes is in the format (A4, 256), (C5, 512) for example

# Now we just need to convert from clocks to note type
note_length_dict = {
    clocks_per_quarter / 16: 'sixtyfourthNote',
    clocks_per_quarter / 8: 'thirtysecondNote',
    clocks_per_quarter / 4: 'sixteenthNote',
    clocks_per_quarter / 2: 'eighthNote',
    clocks_per_quarter: 'quarterNote',
    clocks_per_quarter * 2: 'halfNote',
    clocks_per_quarter * 4: 'wholeNote',
    clocks_per_quarter * 8: 'doublewholeNote',
    clocks_per_quarter * 16: 'quadruplewholeNote'
}

# Change the second entry to the corresponding dictionary value
notes = [(note[0], note_length_dict.get(note[1], 'unknown')) for note in notes]

for note, duration in notes:
    if duration == 'unknown':
        print(f"Warning: Missing duration for clock value {note[1]}")

if output_format == 'text':
    print("Writing to file...")
    with open("plain_{}.txt".format(filename), 'w') as f:
        # [1:-1] to avoid the brackets of the list
        note_string = str(notes)[1:-1]
        note_string = note_string.replace("'", "")
        f.write(note_string)
    print("Successfully saved the converted file to {}".format("plain_{}.txt".format(filename)))

elif output_format == 'arduino':
    print("Writing to Arduino format file...")
    melody = []
    noteDurations = []

    for note, duration in notes:
        if note != 'rest':
            melody.append(f'NOTE_{note}')
        else:
            melody.append('0')
        noteDurations.append(str(duration).replace('sixtyfourthNote', '64')
                                        .replace('thirtysecondNote', '32')
                                        .replace('sixteenthNote', '16')
                                        .replace('eighthNote', '8')
                                        .replace('quarterNote', '4')
                                        .replace('halfNote', '2')
                                        .replace('wholeNote', '1'))

    with open("arduino_{}.ino".format(filename), 'w') as f:
        f.write("int melody[] = {\n  " + ', '.join(melody) + "\n};\n\n")
        f.write("// note durations: 4 = quarter note, 8 = eighth note, etc.:\n")
        f.write("int noteDurations[] = {\n  " + ', '.join(noteDurations) + "\n};\n")
    print("Successfully saved the converted file to {}".format("arduino_{}.ino".format(filename)))
else:
    print("Invalid output format. Use 'text' or 'arduino'.")
