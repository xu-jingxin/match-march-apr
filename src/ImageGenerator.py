""""with to generate a picture with lilypond"""

import music21
from music21 import stream, note, lily, converter, corpus, environment
print(environment.UserSettings()["lilypondPath"])
scr = converter.parse('C:/Users/jingx/PycharmProjects/SR/Sonate_No._14_Moonlight_1st_Movement.mxl')
# print(isinstance(scr, music21.base.Music21Object))
# scr.show('text')
scr.show('lily')
scr.write('lilypond.png', "test")
lpc = lily.translate.LilypondConverter()
b = corpus.parse('bach/bwv66.6')
txt = lpc.loadObjectFromScore(b)
print(txt)
