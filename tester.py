
from mbox import *


if __name__ == '__main__':
    scale = Scale.major('F')
    print(scale)
    print(scale.analyse())

    chord_prog = [
        Chord.triad(1, scale),
        Chord.triad(4, scale),
        Chord.triad(0, scale),
    ]
    print(chord_prog)

    out = create_midi(chord_prog)

    with open('test.mid', 'wb') as f:
        out.writeFile(f)

    standard_tuning = Chord(
            Note('E2'),
            Note('A2'),
            Note('D3'),
            Note('G3'),
            Note('B3'),
            Note('E4'),
        )

    intended_chord = [
        Note('F'),
        Note('C'),
        Note('A'),
    ]

    print(len(standard_tuning.notes))
    print(standard_tuning.notes[0].octave)

    positions = [-1, -1, 3, 2, 1, 1]

    st = StringChord(intended_chord, positions, standard_tuning)
    st.show()

    # generate_positions(Chord())
