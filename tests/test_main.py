import unittest

from music21 import stream, note, tempo
from src import main


class Check_MM(unittest.TestCase):
    def test_raises_error(self):
        # midi lacks a metronome at the start, should raise error
        midi_stream = stream.Stream(note.Note())
        self.assertRaises(ValueError, main.check_MM, midi_stream)

    def test_does_not_raise_error(self):
        # midi has a metronome mark at the start, should not raise error
        midi_stream = stream.Stream([stream.Part([
            tempo.MetronomeMark(), stream.Measure(note.Note())])
        ])
        self.assertTrue(main.check_MM(midi_stream))

class Expand(unittest.TestCase):
    def setUp(self):
        self.C = note.Note('C')
        self.D = note.Note('D')
        self.mxl_strm = stream.Stream([self.C, self.D])

        self.fake_secondsMap = [
            {'element': self.C,
             'endTimeSeconds': 2},
            {
                'element': self.D,
                'endTimeSeconds': 4
            }
        ]

    def test_base(self):
        self.assertEqual(main.expand([self.C], [self.C], 0, midi_secondsMap=self.fake_secondsMap), ([self.C, self.D], [self.C, self.D], 1))
        self.assertIs(main.expand([self.C], [self.C], 0, midi_secondsMap=self.fake_secondsMap), tuple[list[note.NotRest], list[note.NotRest], int])


if __name__ == '__main__':
    unittest.main()
