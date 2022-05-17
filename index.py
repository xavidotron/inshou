#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi,cgitb

cgitb.enable()

import urllib

fs = cgi.FieldStorage()

default = u"印章".encode('utf-8')

print """Content-Type: text/html; charset=utf-8

<html>
<head>
<title>Inshou: Japanese Seals</title>
</head>
<body>
<object data="render.py?kanji=%s" type="image/svg+xml" width="500" height="250">
This gizmo needs SVG support.  I suggest <a href="http://getfirefox.com/">Firefox</a>.
</object>
<form method="get">
<label>Kanji: <input type="text" name="kanji" value="%s" /></label>
<input type="submit" value="Draw" />
</form>

<h3>FAQ</h3>
<dl>
<!--<dt>Why do I see overlapping normal-looking kanji?</dt>
<dd>You aren't loading the remote font we use to display.  In Firefox, make
sure that in Preferences:Content:Fonts:Advanced you have the box about
letting pages use their own fonts checked.  This won't work at all
in some older browsers or browsers without good SVG/CSS2 support.</dd>-->
<dt>Why does this look different from what this book/Solvieg says?</dt>
<dd>These seals are made automatically by a computer program I wrote in like 
30 minutes (plus 45 more to convert between different kanji variants).
It doesn't handle all the things you might do on a real seal, like draw
characters to make optimal use of space.  It also stretches characters
in various ways that makes the lines have different thicknesses.  Finally,
seals are basically signatures: each one's different, and there are a lot
of handwriting variations in exactly what angle the lines are, how long they
are, et cetera.  This is meant to be a helpful starting point, not a
complete solution.</dd>
<dt>Why is my seal missing characters or showing things that don't
look like they're in seal script?</dt>
<dd>We don't have seal-script versions for every character.  
If you have a seal script
version of a character we're missing, let us know.  (Alternately, your
browser may be too old or have lousy SVG support.  Recent versions
of Firefox are known to work.)</dd>
<dt>It says I'm using too many kanji.</dt>
<dd>Yeah, nag me and I'll figure out the dimension parameters for more than
four kanji.</dd>
<dt>Why is part of my seal sorta brownish/reddish?</dt>
<dd>When we don't find an exact match for your kanji, we look through a
database of 'kanji equivalents': things like simplified or traditional
variants on your kanji that we might have seal forms for.  The more conversions
we need to make to find a seal version of your kanji, the redder that
part of your seal is.  Use your own judgement as to whether a reddish seal
component looks correct.  If you find one you think is wrong, let me
know.</dt>
</dl>

<small>Written by Kihou (at mit dot edu).  Hosted by <a href="http://web.mit.edu/sca/www/">Mitgaard</a>.  Powered by <a href="http://scripts.mit.edu/">scripts</a>.</small>

</body>
</html>""" % (urllib.quote(fs.getfirst("kanji",default)),
              cgi.escape(fs.getfirst("kanji",default),quote=True))
