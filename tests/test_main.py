import unittest

from music21 import stream, note, tempo
from src import main


class TestCheck_MM(unittest.TestCase):
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


    # def test_something(self):
    #     self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
