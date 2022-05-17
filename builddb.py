import os
import cPickle as pickle

map = {}

for l in open('Unihan_Variants.txt'):
    if not l.strip() or l.startswith('#'):
        continue
    a,b,c = l.strip().split(None,2)
    #try:
    if True:
        if b == 'kSimplifiedVariant' or b == 'kZVariant' or b == 'kSemanticVariant':
            key = unichr(int(a[2:],16))
            if c.count('U+') > 1:
                # Too wide to be represented as a single unichar
                continue
            if '<' in c:
                c = c.split('<')[0]
            if key in map:
                map[key].append(unichr(int(c[2:],16)))
            else:
                map[key] = [unichr(int(c[2:],16))]
    #except ValueError: # Too wide to be represented as a single unichar
    #    pass

pickle.dump(map,open('simplified.pickle','w'))

