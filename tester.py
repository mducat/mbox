from mido import MidiFile

from mbox import *


if __name__ == '__main__':
    scale = Scale.minor('C#')
    print(scale)
    print(scale.analyse())

    chord_prog = [  # II - V - I
        Chord.triad(1, scale),
        Chord.triad(3, scale),
        Chord.triad(0, scale),
    ]
    print(chord_prog)

    out = create_midi(chord_prog)

    out.save('test.mid')

    file = MidiFile('test.mid', clip=True)
    file.print_tracks()

    """standard_tuning = Tunings.guitar_tuning

    positions = [-1, -1, 3, 2, 1, 0]

    st = StringChord(positions, standard_tuning)
    st.show()

    l = generate_positions(st)
    print(len(l))

    for v in l[:5]:
        StringChord(v).show()

    print('ALL SOLUTIONS:')
    for ch in chord_prog:
        for solution in generate_positions(ch):
            StringChord(solution).show()

    print('RESUME')
    for ch in chord_prog:
        StringChord(generate_positions(ch)[0]).show()"""
