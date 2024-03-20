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


def match(midi_snip, mxl_snip, annotated_list) -> tuple:
    if Counter(map(str, midi_snip)) == Counter(map(str, mxl_snip)):
        print('matched', midi_snip, mxl_snip)

        # something to get seconds
        mxl_snip[-1].__setattr__('secrsss', get_seconds(midi_snip[-1]))
        annotated_list.append(mxl_snip[-1])
        print("end seconds: ", mxl_snip[-1].secrsss)

        print('returned values: ', mxl_snip[-1].next(), midi_snip[-1].next(), annotated_list, '\n')
        return [mxl_snip[-1].next()], [midi_snip[-1].next()], annotated_list

    else:  # expands the range
        print(midi_snip, type(midi_snip))
        midi_snip.append(midi_snip[-1].next())
        mxl_snip.append(mxl_snip[-1].next())
        print('expanding')  # NEED TO BUILD IN A LIMIT!!!
        return midi_snip, mxl_snip, annotated_list


def iter(midi_snip, mxl_snip, annotated_list):
    while mxl_snip[0].offset <= mxl.last().offset:
        mxl_snip, midi_snip, annotated_list = match(mxl_snip, midi_snip, annotated_list)


iter(midi_snip=[midi[0]], mxl_snip=[mxl[0]], annotated_list=[])
