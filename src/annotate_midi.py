from music21 import *

def met_list(input_midi):
    metronome_iterator = input_midi.flatten().getElementsByClass(tempo.MetronomeMark)
    if len(metronome_iterator.getElementsByOffset(0)) == 0:
        raise ValueError("invalid midi: no MetronomeMark at the beginning")
    return sorted(metronome_iterator, key=lambda x: x.offset)

def find_measure_offsets(metlist, stream):
    measure_iterator = stream.recurse().getElementsByClass(stream.base.Measure)
    offset_seconds_dict = dict()
    next_index = 0
    next_offset = 0
    current_duration_seconds = 0
    last_index = len(met_list) - 1
    print(last_index)
    for measure in measure_iterator:
        if measure.offset >= next_offset:  # change of MetronomeMark
            current_secondsPerQuarter = met_list[next_index][1]
            next_index += 1
            if next_index == last_index:
                pass
            else:
                next_offset = met_list[next_index][0]

        current_duration_seconds += current_secondsPerQuarter  # * quarters in a measure
        offset_seconds_dict[measure.measureNumber] = current_duration_seconds
        print(offset_seconds_dict)
