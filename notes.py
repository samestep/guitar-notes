import random

def normalize(note):
    pitch_class, octave = note
    return divmod(pitch_class + 12 * octave, 12)[::-1]

def move_up(note, semitones):
    pitch_class, octave = note
    return normalize((pitch_class + semitones, octave))

letters_to_classes = {'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11}
classes_to_letters = dict(map(reversed, letters_to_classes.items()))

def integer_notation(note):
    pitch_class, octave = note
    letter = pitch_class[0]
    base = letters_to_classes[letter]
    shifted = base - pitch_class.count('es') + pitch_class.count('is')
    return normalize((shifted, octave))

def spelling(note, shift):
    pitch_class, octave = move_up(note, shift)
    if pitch_class in classes_to_letters:
        letter = classes_to_letters[pitch_class]
        return letter + abs(shift) * ('is' if shift < 0 else 'es'), octave

max_accidentals = 1
shift_range = list(range(-max_accidentals, max_accidentals + 1))

def spellings(note):
    unfiltered = (spelling(note, shift) for shift in shift_range)
    return set(candidate for candidate in unfiltered if candidate is not None)

def scientific_to_lilypond(note):
    pitch_class, octave = note
    primes = abs(octave - 3)
    return pitch_class + primes * ("," if octave < 3 else "'")

strings = [('e', 4), ('b', 3), ('g', 3), ('d', 3), ('a', 2), ('e', 2)]
print('\\version "2.18.2" { \\clef "treble_8"')
for measure in range(100):
    string = random.randrange(len(strings))
    fret = random.randrange(15)
    candidates = spellings(move_up(integer_notation(strings[string]), fret))
    note = scientific_to_lilypond(random.choice(list(candidates)))
    print(note + '1^"' + str(string + 1) + '"')
print('}')
