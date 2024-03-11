from music21 import stream, tempo
a_stream = stream.Stream()
print(len(a_stream.getElementsByOffset(0).getElementsByClass(tempo.MetronomeMark)))
