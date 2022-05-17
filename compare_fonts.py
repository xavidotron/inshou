from fontTools import ttLib

names = frozenset(ttLib.TTFont("data/Seal Script.TTF").getGlyphNames())
names2 = frozenset(ttLib.TTFont("data/FZ.ttf").getGlyphNames())

for c in sorted(names2 - names):
    if c.startswith('uni'):
        print unichr(int(c[3:], 16))
