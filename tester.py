
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

    standard_tuning = Tunings.guitar_tuning

    positions = [-1, -1, 3, 2, 1, 0]

    st = StringChord(positions, standard_tuning)
    st.show()

    # generate_positions(Chord())
