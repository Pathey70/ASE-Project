"""
xpln: multi-goal semi-supervised explanation

USAGE: lua xpln.lua [OPTIONS] [-g ACTIONS]
  
OPTIONS:
  -b  --bins    initial number of bins       = 16
  -c  --cliffs  cliff's delta threshold      = .147
  -d  --d       different is over sd*d       = .35
  -f  --file    data file                    = ../etc/data/auto93.csv
  -F  --Far     distance to distant          = .95
  -g  --go      start-up action              = nothing
  -h  --help    show help                    = False
  -H  --Halves  search space for clustering  = 512
  -m  --min     size of smallest cluster     = .5
  -M  --Max     numbers                      = 512
  -p  --p       dist coefficient             = 2
  -r  --rest    how many of rest to sample   = 4
  -R  --Reuse   child splits reuse a parent pole = True
  -s  --seed    random number seed           = 937162211
ACTIONS:
"""
import getopt
import re
import sys

import TestEngine


def coerce(s):
    "coerce a string to some type"
    s = s.strip()
    if s == "False":
        return False
    elif s == "True":
        return True
    try:
        return int(s)
    except:
        try:
            return float(s)
        except:
            return s


def get_default():
    global the
    p = r"\n[\s]+-[\S]+[\s]+--([\S]+)[^\n]+= ([\S]+)"
    for k, v in re.findall(p, __doc__):
        the[k] = coerce(v)
    # return t


def update(opts, t):
    for opt, arg in opts:
        if opt in ("-d", "--dump"):
            t['dump'] = coerce(arg)
        if opt in ("-g", "--go"):
            t['go'] = coerce(arg)
        if opt in ("-h", "--help"):
            t['help'] = coerce(arg)
        if opt in ("-s", "--seed"):
            t['seed'] = coerce(arg)
    return t


# Stores arguments in the variable
# use python3 Main.py --[options]
the = {}
if __name__ == "__main__":
    get_default()
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, ":dghs", ["dump=", "go=", "help=", "seed="])
    except getopt.GetoptError:
        print('Please provide appropriate arguments')
        sys.exit(2)
    the = update(opts, the)
    if the['help']:
        print(__doc__)
        sys.exit(2)
    sys.exit(TestEngine.run(the))
