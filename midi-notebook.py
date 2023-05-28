import datetime
import mido
print("Initializing...")
# Define the MIDI note numbers for C5 to B5
notes_default = [60, 62, 64, 65, 67, 69, 71]
octave_offset = input("Octave Offset (Default 1 = C5)\n")
if octave_offset is "":
    notes = notes_default
else:
    notes = [x + int(octave_offset)*12 for x in notes_default]
# Define the default note length in ticks (assuming 120 BPM and 4/4 time signature)
default_note_length = 120


# Define the ticks per beat (TPB) for the MIDI file
ticks_per_beat = 480

def create_midi_file(note_string, filename):
    # Create a new MIDI file
    midi_file = mido.MidiFile(ticks_per_beat=ticks_per_beat)

    # Create a new MIDI track
    track = mido.MidiTrack()

    # Add the track to the MIDI file
    midi_file.tracks.append(track)

    # Set the tempo of the MIDI file (120 BPM)
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))

    # Set the time signature of the MIDI file (4/4)
    track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4))

    # Parse the note string and add MIDI messages to the track
    current_time = 0
    i = 0
    while i < len(note_string):
        # Reset note_length to default value at the beginning of each note
        note_length = default_note_length
        char = note_string[i]
        if char.isdigit():
            note_index = int(char) - 1
            note_number = notes[note_index]
            note_length = default_note_length
            while True:
                if i+1 < len(note_string) and note_string[i+1:i+2] == '.':
                    note_length += default_note_length
                    i += 1
                else:
                    break
            if i+2 < len(note_string) and note_string[i+1:i+2] == "(" and note_string[i+3:i+4] == ")":
                octave_modifier = 0
                accidental_modifier = 0
                note_modifier = note_string[i+2:i+3]
                if note_modifier == "+":
                    octave_modifier = 12
                    i += 1
                elif note_modifier == "-":
                    octave_modifier = -12
                    i += 1
                note_modifier = note_string[i+2:i+3]
                if note_modifier == "#":
                    accidental_modifier = 1
                    i += 1
                elif note_modifier == "b":
                    accidental_modifier = -1
                    i += 1
                note_number += octave_modifier + accidental_modifier
            note_off_time = note_length
            track.append(mido.Message('note_on', note=note_number, velocity=127, time=current_time))
            track.append(mido.Message('note_off', note=note_number, velocity=0, time=note_off_time))
            #current_time += note_length
            current_time = 0
        i += 1

    # Save the MIDI file
    midi_file.save(filename)

# Example usage: create a MIDI file from the note string "123.456.7"
inputstr = input("Insert string\n")
current_datetime = datetime.datetime.now()
filename = current_datetime.strftime("%Y%m%d-%H%M%S.mid")
create_midi_file(inputstr, filename)
print("File {} created!".format(filename))