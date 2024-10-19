# midi_to_plain_text
A python program to convert extremely simple midi files into plain text.

Takes in a simple midi file consisting of only single notes and rest, and saves a new file with tuples of note type and duration.

For example, a midi file containing the A major scale as included in the file example_scale.mid would save

(A3, wholeNote), (B3, wholeNote), (C#4, wholeNote), (D4, wholeNote), (E4, wholeNote), (F#4, wholeNote), (G#4, wholeNote), (A4, wholeNote)

to the file plain_example_scale.mid.txt

Adding support for Arduino Format, use with 

python midi_to_plain_text.py example_scale.mid arduino

to save the file arduino_example_scale.ino


int melody[] = {
  NOTE_G4, NOTE_G4, NOTE_G4, NOTE_DS4, NOTE_F4, NOTE_F4, NOTE_F4, NOTE_D4,
  NOTE_G4, NOTE_G4, NOTE_G4, NOTE_DS4, NOTE_F4, NOTE_F4, NOTE_F4, NOTE_D4,
  NOTE_G4, NOTE_G4, NOTE_G4, NOTE_G4, NOTE_G4, NOTE_F4, NOTE_F4,
  NOTE_G4, NOTE_G4, NOTE_G4, NOTE_G4, NOTE_G4, NOTE_F4, NOTE_F4,
  NOTE_G4, NOTE_G4, NOTE_G4, NOTE_DS4, NOTE_F4, NOTE_F4, NOTE_F4, NOTE_D4
};


// note durations: 4 = quarter note, 8 = eighth note, etc.:

int noteDurations[] = {
  8, 8, 8, 8, 8, 8, 8, 8,
  8, 8, 8, 8, 8, 8, 8, 8,
  4, 8, 8, 8, 8, 4, 4,
  4, 8, 8, 8, 8, 4, 4,
  8, 8, 8, 8, 8, 8, 8, 8
};
