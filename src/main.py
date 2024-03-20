import random

from music21 import *
from collections import Counter

midi = (converter.parse('../Sonate_No._14_Moonlight_1st_Movement.mxl')
        .flatten().getElementsByClass(note.NotRest)).stream()

mxl = (converter.parse('../Sonate_No._14_Moonlight_1st_Movement.mxl')
       .flatten().getElementsByClass(note.NotRest)).stream()


def get_seconds(element) -> float:
    midi_dict_list = midi.secondsMap
    for x in midi_dict_list:
        if x['element'] == element: return x['endTimeSeconds']
    return 'NOT FOUND!!!'


record = []


def match(midi_snip, mxl_snip) -> tuple:
    if Counter(map(str, midi_snip)) == Counter(map(str, mxl_snip)):
        print('matched')
        print(midi_snip, mxl_snip)
        # something to get seconds
        mxl_snip[-1].__setattr__('secrsss', get_seconds(midi_snip[-1]))
        record.append(mxl_snip[-1])
        print("end seconds: ", mxl_snip[-1].secrsss)
        print("record: ", record)

        return mxl_snip[-1].next(), midi_snip[-1].next()

    else:  # expands the range
        print(midi_snip, type(midi_snip))
        midi_snip.append(midi_snip[-1].next())
        mxl_snip.append(mxl_snip[-1].next())
        print('expanding')
        return midi_snip, mxl_snip


def iter(midi_snip, mxl_snip):
    while mxl_snip[0].offset <= mxl.last().offset:
        mxl_snip, midi_snip = match(mxl_snip, midi_snip)


iter(midi_snip=[midi[0]], mxl_snip=[mxl[0]])
