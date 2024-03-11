from music21 import *

midi_stream = converter.parse("../Sonate_No._14_Moonlight_1st_Movement.mid")
metronome_iterator = midi_stream.recurse().getElementsByClass(tempo.MetronomeMark)
if len(metronome_iterator.getElementsByOffset(0)) == 0:
    raise ValueError("invalid midi: no MetronomeMark at the beginning")

measure_iterator = midi_stream.recurse().getElementsByClass(stream.base.Measure)
met_list = list()
for mm in metronome_iterator:
    met_list.append([mm.offset, mm.secondsPerQuarter()])
    met_list = sorted(met_list)
met_list.append([4.0, 2.49])
met_list.append([20, 30])
print(met_list)

offset_seconds_dict = dict()
next_index = 0
next_offset = 0
last_index = len(met_list)-1
print(last_index)
for measure in measure_iterator:
    if measure.offset >= next_offset:
        current_secondsPerQuarter = met_list[next_index][1]
        next_index += 1
        if next_index == last_index:
            pass
        else:
            next_offset = met_list[next_index][0]

    offset_seconds_dict[measure.measureNumber] = measure.offset * current_secondsPerQuarter
    print(offset_seconds_dict)


# class AnnotatedMidi():
#     def check_stream(self):  # check that there is a metronome mark at offset 0
#         if len(self.metronome_iterator.getElementsByOffset(0)) != 0:
#             pass
#         else:
#             raise ValueError("invalid midi: no MetronomeMark at the beginning")
#
#     def __init__(self, midi_stream):
#         self.metronome_iterator = midi_stream.recurse().getElementsByClass(tempo.MetronomeMark)
#         self.measure_iterator = midi_stream.recurse().getElementsByClass(stream.base.Measure)
#         met_list = list()
#         current_metronome_index = 0
#         self.check_stream()
#
#     def update_met_list(self):
#         for mm in self.metronome_iterator:
#             self.met_list.append([mm.offset, mm.secondsPerQuarter()])
#         self.met_list = sorted(self.met_list)
#         print(self.met_list)



