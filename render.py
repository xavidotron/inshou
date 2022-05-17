#!/usr/bin/python
from __future__ import with_statement

import cgi,cgitb
import os

cgitb.enable()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

fs = cgi.FieldStorage()
kanji = unicode(fs.getfirst('kanji',u'\u4F55'.encode('utf-8')),'utf-8')

print """Content-Type: image/svg+xml; charset=utf-8

<?xml version="1.0" standalone="yes"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink">
"""

dimmap = {
    1: ((-50,140,.14,-.08),),
    2: (( 60,140,.07,-.08),
        (-25,140,.07,-.08)),
    3: (( 60,140,.07,-.08),
        (-25, 75,.07,-.04),
        (-25,160,.07,-.04)),
    4: (( 60, 70,.07,-.04),
        ( 60,160,.07,-.04),
        (-25, 70,.07,-.04),
        (-25,160,.07,-.04))}

from fontTools import ttLib

alternate_font = fs.getfirst('font', False)

if alternate_font:
    names = frozenset(ttLib.TTFont("data/FZ.ttf").getGlyphNames())
else:
    names = frozenset(ttLib.TTFont("data/Seal Script.TTF").getGlyphNames())
simpmap = None

def glyphname(k):
    return 'uni%04X' % ord(k)

if len(kanji) not in dimmap:
    print '    <text x="0pt" y="64pt">Too many kanji!</text>'
else:
    print '<defs>'
    print
    print '<g id="seal">'
    print '<rect height="180" width="180" fill="white" stroke="black" rx="15"/>\n'
    dims = dimmap[len(kanji)]
    for k,d in zip(kanji,dims):
        sketch = 0
        path = []
        glyph = glyphname(k)
        if glyph not in names:
            if simpmap is None:
                import cPickle as pickle
                simpmap = pickle.load(open('simplified.pickle'))
            orig = k
            k = u' '
            if orig in simpmap:
                done = set((orig,))
                will = [(s,1,[orig]) for s in simpmap[orig]]
                while len(will) > 0:
                    now, nsketch, npath = will.pop()
                    done.add(now)
                    if glyphname(now) in names:
                        k = now
                        sketch = nsketch
                        path = npath
                        break
                    elif now in simpmap:
                        for s in simpmap[now]:
                            if s not in done:
                                will.append((s,nsketch+1,npath+[now]))
        if path:
            print '    <!--%s-->' % path
        print ('    <g transform="translate(%s,%s)"><g class="seal" transform="scale(%s,%s)" fill="#%s0000">\n'
               % (d + (hex(min(sketch*3,15))[2:]*2,))).encode('utf-8')
        if k != u' ':
            gnam = glyphname(k)
            with open('glyphs/%s.svg'%gnam) as gfile:
                for l in gfile:
                    print l,
        print ('    </g></g>\n')
    print '</g>'
    print

    print '</defs>'
    print
    print '<a xlink:href="http://sca.scripts.mit.edu/inshou/?kanji=%s" target="_top">' % kanji.encode('utf-8')
    print '<text transform="translate(0,16)">Seal (as on paper):</text>'
    print
    print '<g transform="translate(10,30)">'
    print '<use xlink:href="#seal" />'
    print '</g>'
    print 
    print '<text transform="translate(250,16)">Flipped (for carving):</text>'
    print
    print '<g transform="translate(450,30) scale(-1,1)">'
    print '<use xlink:href="#seal" />'
    print '</g>'
    print '</a>'
    print
print """</svg>"""
