from __future__ import with_statement

from fontTools import ttLib
import sys,os,subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))

fontpath = "data/Seal Script.TTF"

names = ttLib.TTFont(fontpath).getGlyphNames()

for n in names:
    if n.startswith('uni'):
        try:
            codepoint = str(int(n[3:],16))
        except ValueError:
            continue
        print "Writing %s..." % n
        ttf2svg = subprocess.Popen(['ttf2svg',fontpath,
                                    '-l',codepoint,'-h',codepoint],
                                   stdout=subprocess.PIPE)
        started = False
        ended = False
        with open('glyphs/%s.svg'%n,'w') as out:
            for l in ttf2svg.stdout:
                if l.startswith('<glyph'):
                    started = True
                if started and not ended:
                    out.write(l)
                if started and '/>' in l:
                    ended = True
            if ttf2svg.wait() != 0:
                print >>sys.stderr,"Got a %s!"%ttf2svg.returncode
                sys.exit(ttf2svg.returncode)
