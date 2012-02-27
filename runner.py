#! /usr/bin/python
import os
import sys
import re
import subprocess
from subprocess import PIPE, Popen

Errfile = '.errors'

p = Popen(['python']+sys.argv[1:], stderr=PIPE)
p.wait()
errs = p.stderr.read()
print >> open(Errfile , 'w'), errs

patt = re.compile(r'^\s+File "(.+)", line (\d+)', re.M)
result = []
for err in errs.split('\n'):
    g = patt.match(err)
    if g:
        result.append(g.groups())
# raw_input('Press...')
if result:
    file, line = result[-1]
    try:
        Popen(['vim', '-n', '-O2', '-S', 'runnersession.vim', '+%s'%line, file, Errfile]).wait()
    except KeyboardInterrupt as e:
        pass
