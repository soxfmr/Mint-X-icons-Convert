#!/usr/bin/python2

from sys import argv
from os import listdir
from os.path import isdir
from logger import debug
from utils import composepath
from string import Template

TEMPLATE_HEADER = '''[Icon Theme]
Name=$tp_name
Comment=$tp_comment
$tp_inherit

'''

TEMPLATE_KED_SPECIAL = '''# KDE Specific Stuff
DisplayDepth=32
LinkOverlay=link_overlay
LockOverlay=lock_overlay
ZipOverlay=zip_overlay
DesktopDefault=48
DesktopSizes=16,22,32,48,64,72,96,128
ToolbarDefault=22
ToolbarSizes=16,22,32,48
MainToolbarDefault=22
MainToolbarSizes=16,22,32,48
SmallDefault=16
SmallSizes=16
PanelDefault=32
PanelSizes=16,22,32,48,64,72,96,128

'''

TEMPLATE_DIMEN = '''[${tp_dimen}/${tp_icon}]
Context=$tp_context
Size=$tp_size
Type=$tp_type

'''

def getcontext(icon):
    if (icon == 'apps'):
        icon = 'Applications'
    return icon.capitalize()

def buildtheme(name, path, comment = '', inherit = ''):
    if not isdir(path): return False
    if (comment == ''): comment = name

    handle = open(composepath(path, "index.theme"), "w+")
    try:
        tp = Template( TEMPLATE_HEADER )
        if (inherit != ''): inherit = "Inherit=%s" % inherit

        handle.write(tp.substitute(tp_name=name, tp_comment=comment, tp_inherit=inherit))
        handle.write( TEMPLATE_KED_SPECIAL )

        directories = "Directories="
        dimen_desc = ""
        for dimen in listdir(path):
            file = composepath(path, dimen)
            if not isdir(file): continue

            for icon in listdir(file):
                directories += composepath(dimen, icon) + ','
                if dimen == 'scalable':
                    n_size = "16\nMinSize=8\nMaxSize=512"
                    n_type = 'Scalable'
                else:
                    n_size = dimen[0:dimen.index('x')]
                    n_type = 'Fixed'

                n_context = getcontext(icon);

                tp = Template( TEMPLATE_DIMEN )
                dimen_desc += tp.substitute(tp_dimen=dimen, tp_icon=icon, tp_context=n_context, tp_size=n_size, tp_type=n_type)

        handle.write(directories + "\n\n")
        handle.write(dimen_desc)
    except Exception, e:
        debug("Oops, It seem something wrong: " + str(e))
    finally:
        handle.close()

if __name__ == "__main__":
    buildtheme(argc[1], argc[2])
