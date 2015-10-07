#!/usr/bin/python2

from sys import argv
from os import system

def svg2png(fn, dimen):
	fn = fn[0:fn.rindex('.')]
	cmd = "inkscape -z -e %s.png -w %s -h %s %s.svg" % (fn, dimen, dimen, fn)
	system(cmd)

if __name__ == "__main__":
	svg2png(argv[1], argv[2])
