#!/usr/bin/python2
DEBUG_ENABLE = True
DEBUG_APP = "[Mint-X-icons-Convert]: "

def debug(msg):
    if (DEBUG_ENABLE):
        print "%s%s\n" % (DEBUG_APP, msg)
