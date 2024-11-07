import unittest

from music21 import stream, note, tempo
from src import Timestamper


class Check_MM(unittest.TestCase):
    def test_does_not_raise_error(self):
        # midi has a metronome mark at the start, should not raise error
        midi_stream = stream.Stream([stream.Part([
            tempo.MetronomeMark(), stream.Measure(note.Note())])
        ])
        self.test_stamper = Timestamper.Stamper(midi_stream, midi_stream)
        self.assertTrue(self.test_stamper.check_MM())

    def test_raises_error(self):
        # midi lacks a metronome at the start, should raise error
        midi_stream = stream.Stream(note.Note())
        self.assertRaises(ValueError, lambda: Timestamper.Stamper(midi_stream, midi_stream))

class CheckExpand(unittest.TestCase):
    def setUp(self):
        self.C = note.Note('C')
        self.D = note.Note('D')
        self.mxl_strm = stream.Stream([self.C, self.D])

        fake_secondsMap = [
            {'element': self.C,
             'endTimeSeconds': 2},
            {
                'element': self.D,
                'endTimeSeconds': 4
            }
        ]

        self.stamper = Timestamper.Stamper(stream.Stream([tempo.MetronomeMark(),note.Note('c')]), self.mxl_strm)
        self.stamper.midi_secondsMap = fake_secondsMap
        assert len(self.stamper.midi_secondsMap) >0

    def test_base(self):
        self.assertEqual(self.stamper.expand([self.C], [self.C], 0), ([self.C, self.D], [self.C, self.D], 1))
    def test_return_type(self):
        self.assertIs(self.stamper.expand([self.C], [self.C], 0), tuple[list[note.NotRest], list[note.NotRest], int])

    def terminates_after_six(self):
        pass
class EqualityChecking(unittest.TestCase):
    def test_check_equal(self):
        pass
    def test_check_subset(self):
        pass



if __name__ == '__main__':
    unittest.main()
