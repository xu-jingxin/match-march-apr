from typing import Tuple, List

import music21
from music21 import *
from collections import Counter

from music21.note import NotRest

midi = converter.parse('../Sonate_No._14_Moonlight_1st_Movement.mxl')


def check_MM(midi) -> bool | ValueError:  # check metronome marks
    if len(midi.recurse().getElementsByClass(tempo.MetronomeMark)
                   .getElementsByClass(tempo.MetronomeMark).getElementsByOffset(0)) == 0:
        raise ValueError("invalid midi: no MetronomeMark at the beginning")
    else:
        return True


check_MM(midi)

midi_secondsMap = sorted(midi.flatten().getElementsByClass(note.NotRest).stream().secondsMap,
                         key=lambda x: x['offsetSeconds'])

mxl = converter.parse('../Sonate_No._14_Moonlight_1st_Movement.mxl').flatten().getElementsByClass(note.NotRest).stream()


def match(midi_snip, mxl_snip, annotated_dict, last_index) -> tuple[list[note.NotRest], list[note.NotRest], dict, int]:
    def expand(midi_snip: list[note.NotRest], mxl_snip: list[note.NotRest], expansions: int = 0) -> tuple[
        list[NotRest], list[NotRest], int]:
        # range expansion deals with wrong order of concurrent notes.
        midi_snip.append(midi_secondsMap[last_index + 1]['element'])
        mxl_snip.append(mxl_snip[-1].next())
        print('expanded')
        return midi_snip, mxl_snip

    def checked_second_in_first(a, b) -> bool:
        # checking if element exists in second list
        for key in b:
            if key not in a:
                return False
            if b[key] > a[key]:
                return False
        return True

    def checked_equal(midi_snip, mxl_snip) -> bool:
        return Counter(map(str, midi_snip)) == Counter(map(str, mxl_snip))

    def check(midi_snip, mxl_snip, expansions=0) -> tuple[list[note.NotRest], list[note.NotRest], dict, int]:
        if expansions >= 6:
            raise ValueError

        elif checked_equal(midi_snip, mxl_snip):
            annotated_dict[midi_secondsMap[last_index]['element'].measureNumber] \
                = midi_secondsMap[last_index]['endTimeSeconds']
            print('matched order')
            print([midi_secondsMap[last_index + 1]['element']], [mxl_snip[-1].next()], annotated_dict, last_index + 1)

            return [midi_secondsMap[last_index + 1]['element']], [mxl_snip[-1].next()], annotated_dict, last_index + 1

        elif checked_second_in_first(mxl_snip, midi_snip):  # assuming only 2 and 3.
            annotated_dict[midi_secondsMap[last_index]['element'].measureNumber] \
                = midi_secondsMap[last_index]['endTimeSeconds']
            print('matched subset')
            return ([midi_secondsMap[last_index]['element']],
                    [mxl_snip[-1].next()], annotated_dict, last_index + 1)

        else:
            check(expand(midi_snip, mxl_snip), expansions+1)

    return check(midi_snip, mxl_snip)

def iterate(midi_snip, mxl_snip, annotated_dict, last_index=0):
    while last_index < len(mxl):  # mxl_snip[0].offset <= mxl.last().previous().offset:
        midi_snip, mxl_snip, annotated_dict, last_index = match(midi_snip, mxl_snip, annotated_dict, last_index)
        print(midi_snip, mxl_snip, annotated_dict, last_index)


iterate(midi_snip=[midi_secondsMap[0]['element']], mxl_snip=[mxl[0]], annotated_dict={})
