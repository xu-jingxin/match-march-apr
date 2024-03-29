import random

import music21.note
from music21 import *
from collections import Counter


midi = converter.parse('../Sonate_No._14_Moonlight_1st_Movement.mxl')

def check_MM(midi):  # check metronome marks
    if len(midi.recurse().getElementsByClass(music21.tempo.MetronomeMark)
            .getElementsByClass(music21.tempo.MetronomeMark).getElementsByOffset(0)) == 0:
        raise ValueError("invalid midi: no MetronomeMark at the beginning")


midi_secondsMap = sorted(midi.flatten().getElementsByClass(note.NotRest)).stream().secondsMap, key=lambda x: x['offsetSeconds'])

mxl = converter.parse('../Sonate_No._14_Moonlight_1st_Movement.mxl')
       .flatten().getElementsByClass(note.NotRest)).stream()

def match(midi_snip, mxl_snip, annotated_dict, last_index) -> tuple:
    def expand(expansions=0):  # range expansion deals with wrong order of concurrent notes.
        midi_snip.append(midi_secondsMap[last_index + 1]['element'])
        mxl_snip.append(mxl_snip[-1].next())
        expansions += 1
        print('expanded')
        match(midi_snip, mxl_snip, annotated_dict, last_index + 1)


    if Counter(map(str, midi_snip)) == Counter(map(str, mxl_snip)):
        annotated_dict[midi_secondsMap[last_index]['element'].measureNumber] = midi_secondsMap[last_index]['endTimeSeconds']
        print('matched')
        return [midi_secondsMap[last_index+1]['element']], [mxl_snip[-1].next()], annotated_dict, last_index + 1
    else:  # expands the range -> deals with wrong order.
        expansion_success = expand()
        if not expansion_success:
            # missing or wrong element.



def iter(midi_snip, mxl_snip, annotated_dict, last_index=0):
    while mxl_snip[0].offset <= mxl.last().offset:
        mxl_snip, midi_snip, annotated_dict, last_index = match(mxl_snip, midi_snip, annotated_dict, last_index)
        print(mxl_snip, midi_snip, annotated_dict, last_index)

iter(midi_snip=[midi_secondsMap[0]['element']], mxl_snip=[mxl[0]], annotated_dict={})
