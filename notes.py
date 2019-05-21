import collections
import itertools
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

def fretboard(strings):
    def f(pair):
        string, fret = pair
        return move_up(integer_notation(string), fret)
    return collections.Counter(map(f, itertools.product(strings, range(14))))

def fill_measure(notes):
    duration = {1: '2.', 2: '4.', 3: '4'}[len(notes)]
    return ' '.join(note + str(duration) for note in notes) + ' |'

strings = [('e', 4), ('b', 3), ('g', 3), ('d', 3), ('a', 2), ('e', 2)]
board = fretboard(strings)

def positions(chord):
    chord = list(chord)
    answers = []
    for permutation in itertools.permutations(range(len(strings)), len(chord)):
        frets = {}
        for note_index, string_index in enumerate(permutation):
            note = integer_notation(chord[note_index])
            string = integer_notation(strings[string_index])
            for fret in range(21):
                if note == move_up(string, fret):
                    frets[string_index] = fret
        if len(frets) == len(chord):
            answers.append(frets)
    return answers

def ease(position, capo):
    frets = set(position.values()) - {capo}
    candidate = True
    for fret in frets:
        if fret < capo:
            candidate = False
    if candidate:
        return max(frets) - min(frets) if len(frets) > 0 else 0

def easiest(choices, capo):
    best = None
    for position in choices:
        position_ease = ease(position, capo)
        if best == None or (position_ease != None and position_ease < best):
            best = position_ease
    return best

def display_string(index, position, capo):
    if index in position:
        return str(position[index]).rjust(2)
    else:
        return '  '

def display_position(position, capo):
    strings = [display_string(index, position, capo) for index in range(6)]
    print(' '.join(strings))

chordses = [
    [
        {('f', 3), ('f', 4), ('a', 4), ('c', 5)},
        {('e', 3), ('g', 4), ('c', 5)},
        {('d', 3), ('f', 4), ('a', 4), ('c', 5)},
        {('c', 3), ('f', 4), ('a', 4), ('c', 5)},
        {('bes', 2), ('f', 4), ('g', 4), ('d', 5)},
        {('c', 3), ('e', 4), ('g', 4), ('c', 5)},
        {('f', 3), ('f', 4), ('a', 4), ('c', 5)},
        {('c', 3), ('e', 4), ('g', 4), ('c', 5)}
    ],
    [
        {('f', 3), ('c', 4), ('f', 4), ('a', 4)},
        {('e', 3), ('c', 4), ('g', 4)},
        {('d', 3), ('c', 4), ('f', 4), ('a', 4)},
        {('c', 3), ('c', 4), ('f', 4), ('a', 4)},
        {('bes', 2), ('d', 4), ('f', 4), ('g', 4)},
        {('c', 3), ('c', 4), ('e', 4), ('g', 4)},
        {('f', 3), ('c', 4), ('f', 4), ('a', 4)},
        {('c', 3), ('c', 4), ('e', 4), ('g', 4)}
    ],
    [
        {('f', 3), ('a', 3), ('c', 4), ('f', 4)},
        {('e', 3), ('g', 3), ('c', 4), ('g', 4)},
        {('d', 3), ('a', 3), ('c', 4), ('f', 4)},
        {('c', 3), ('a', 3), ('c', 4), ('f', 4)},
        {('bes', 2), ('g', 3), ('d', 4), ('f', 4), ('g', 4)},
        {('c', 3), ('g', 3), ('c', 4), ('e', 4), ('g', 4)},
        {('f', 3), ('a', 3), ('c', 4), ('f', 4)},
        {('c', 3), ('g', 3), ('c', 4), ('e', 4)}
    ]
]

# for chords in chordses:
#     for capo in range(21):
#         eases = [easiest(positions(chord), capo) for chord in chords]
#         if None in set(eases):
#             break
#         print(capo, eases)
#     print()

capos = [1, 3, 3]

for i, chords in enumerate(chordses):
    capo = capos[i]
    print(' e  B  G  D  A  E')
    for chord in chords:
        best_closed = None
        best_ease = None
        best_pos = None
        best_position = None
        for position in positions(chord):
            position_closed = len([fret for fret in position.values() if fret != capo])
            position_ease = ease(position, capo)
            position_pos = None
            if position_ease != None and position_ease < 4 and (best_closed == None or position_closed < best_closed):
                best_ease = position_ease
                best_closed = position_closed
                best_pos = position_pos
                best_position = position
        display_position(best_position, capo)
    print()

# print('\\version "2.18.2" { \\clef "treble_8" \\time 3/4')
# for measure in range(100):
#     note = random.choice(list(board.keys()))
#     count = board[note]
#     spell = random.choice(list(spellings(note)))
#     print(fill_measure(count * [scientific_to_lilypond(spell)]))
# print('}')
