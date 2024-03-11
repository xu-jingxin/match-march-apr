import music21 as m21
midi_stream = m21.converter.parse("../Sonate_No._14_Moonlight_1st_Movement.mid")
midi_stream.show('text')
