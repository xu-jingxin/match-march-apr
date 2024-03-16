from music21 import *

midi = (converter.parse('../Sonate_No._14_Moonlight_1st_Movement.mxl')
        .flatten().getElementsByClass(note.NotRest))
def get_seconds(midi_stream):
    return midi_stream.secondsMap

mxl = converter.parse('../Sonate_No._14_Moonlight_1st_Movement.mxl').recurse().getElementsByClass(note.NotRest)

midi.show('text')
print('----------------------------------------')
mxl.show('text')
for i in range(10):
    midi_i = midi.getElementsByOffset(midi[i].offset)  # need to code such that elements with offsets close to but not equal are also put together
    mxl_i = midi.getElementsByOffset(midi[i].offset)
    print(midi_i.elements)
    print(mxl_i.elements)
    if midi_i.elements == mxl_i.elements:
        print('matched')
    else:
        print('not matched')
