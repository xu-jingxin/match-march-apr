from typing import Tuple, List

import music21
from music21 import *
from collections import Counter

from music21.note import NotRest



def check_MM(midi) -> bool | ValueError:  # check metronome marks
    if len(midi.recurse().getElementsByClass(tempo.MetronomeMark).getElementsByOffset(0)) == 0:
        raise ValueError("invalid midi: no MetronomeMark at the beginning")
    else:
        return True


def expand(midi_snip: list[note.NotRest], mxl_snip: list[note.NotRest], last_index: int, midi_secondsMap = midi_secondsMap, expansions: int = 0) -> tuple[
    list[NotRest], list[NotRest], int]:
    # range expansion deals with wrong order of (almost) concurrent notes.
    midi_snip.append(midi_secondsMap[last_index + 1]['element'])
    mxl_snip.append(mxl_snip[-1].next())
    print('expanded')
    return midi_snip, mxl_snip, last_index + 1


def checked_second_in_first(a, b) -> bool:
    # checking if a subset of b
    for key in b:
        if key not in a:
            return False
        if b[key] > a[key]:
            return False
    return True


def checked_equal(midi_snip, mxl_snip) -> bool:
    return Counter(map(str, midi_snip)) == Counter(map(str, mxl_snip))



def match(midi_snip, mxl_snip, annotated_dict, last_index) -> tuple[list[note.NotRest], list[note.NotRest], dict, int]:
    def check(midi_snip, mxl_snip, expansions=0) -> tuple[list[note.NotRest], list[note.NotRest], dict, int]:
        if expansions >= 6:
            raise ValueError

        elif checked_equal(midi_snip, mxl_snip):
            annotated_dict[midi_secondsMap[last_index]['element'].measureNumber] \
                = midi_secondsMap[last_index]['endTimeSeconds']
            print('matched order')
            print([midi_secondsMap[last_index + 1]['element']], [mxl_snip[-1].next()], annotated_dict, last_index + 1)

            return [midi_secondsMap[last_index + 1]['element']], [mxl_snip[-1].next()], annotated_dict, last_index + 1

        elif checked_second_in_first(midi_snip, mxl_snip):  # assuming only the case of midi missing one note
            annotated_dict[midi_secondsMap[last_index]['element'].measureNumber] \
                = midi_secondsMap[last_index]['endTimeSeconds']
            print('matched subset')
            return ([midi_secondsMap[last_index + 1]['element']],
                    [mxl_snip[-1]], annotated_dict, last_index + 1) # step the midi but not the mxl

        else:
            check(expand(midi_snip, mxl_snip, last_index), expansions+1)

    return check(midi_snip, mxl_snip)

def iterate(midi_snip, mxl_snip, annotated_dict, last_index=0): # main driver fuction
    while last_index < len(mxl):  # mxl_snip[0].offset <= mxl.last().previous().offset:
        midi_snip, mxl_snip, annotated_dict, last_index = match(midi_snip, mxl_snip, annotated_dict, last_index)
        print(midi_snip, mxl_snip, annotated_dict, last_index)


# iterate(midi_snip=[midi_secondsMap[0]['element']], mxl_snip=[mxl[0]], annotated_dict={})
