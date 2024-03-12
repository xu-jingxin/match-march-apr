from music21 import stream, tempo, note, converter

# midi_stream = converter.parse("../Sonate_No._14_Moonlight_1st_Movement.mid")

strm = stream.Stream([
    stream.Part([
        stream.Measure(note.Note(type='whole'), number=1, offset=0),
        stream.Measure(number=2, offset=4)
    ], offset=20)
])
strm.show('text')
map = strm.recurse().getElementsByClass(stream.base.Measure).secondsMap
print(map)

# p0 = stream.Part(id='part0')
# m01 = stream.Measure(number=1)
# m01.append(note.Note('C', type='whole'))
# m02 = stream.Measure(number=2)
# m02.append(note.Note('D', type='whole'))
# p0.append([m01, m02])
# p0.show('text')
