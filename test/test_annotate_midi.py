import unittest
from src import annotate_midi
from music21 import stream, note, tempo


class met_list(unittest.TestCase):
    def test_raises_error(self): # midi lacks a metronome at the start, should raise error
        midi_stream = stream.Stream(note.Note())
        self.assertRaises(ValueError, annotate_midi.met_list, midi_stream)
        midi_stream = stream.Stream(tempo.MetronomeMark(30))
        self.assertEqual(annotate_midi.met_list(midi_stream), [tempo.MetronomeMark(30)])
    def test_creates_list(self):
        class TestCase:
            def __init__(self, name, input, expected):
                self.name: str = name
                self.input: stream.Stream = input
                self.expected: list = expected

        nested_marks = stream.Stream([
            tempo.MetronomeMark(number=30, offset=3),
            stream.Part(tempo.MetronomeMark(number=40, offset=0))
        ])
        composite_stream = stream.Stream([
            tempo.MetronomeMark(number=30, offset=3),
            note.Note('C'),
            stream.Part(tempo.MetronomeMark(number=40, offset=0))
        ])

        testcases = [
            TestCase(name="one MetronomeMark",
                     input=stream.Stream(tempo.MetronomeMark(number=40, offset=0)),
                     expected=[tempo.MetronomeMark(number=40)]
                     ),
            TestCase(name="two nested marks",
                     input=nested_marks,
                     expected=[
                         tempo.MetronomeMark(number=30, offset=0),
                         tempo.MetronomeMark(number=40, offset=4)]
                    ),
            TestCase(name="things other than MetronomeMarks",
                     input=composite_stream,
                     expected=[
                         tempo.MetronomeMark(number=30, offset=0),
                         tempo.MetronomeMark(number=40, offset=4)]
                     )
        ]

        for case in testcases:
            # print(case.name)
            # case.input.show('text')
            actual = annotate_midi.met_list(case.input)
            self.assertListEqual(
                case.expected,
                actual,
            )


class the_rest(unittest.TestCase):
    def test_find_measure_offsets(self):
        the_dictionary = {
            1: 0.0,
            2: 3
        }
        self.assertEqual(find_measure_offsets(metlist, stream), the_dictionary)
if __name__ == '__main__':
    unittest.main()
