#!/usr/bin/python2

#import pdb
from os import listdir
from os import unlink
from os import mkdir
from os import remove
from os.path import isdir
from os.path import islink
from os.path import exists
from os.path import realpath
from shutil import move
from shutil import rmtree
from shutil import copyfile
from logger import debug
from convert import svg2png
from utils import composepath
from themebuilder import buildtheme

# Mint-X-icons Basic Folder
MINT_X_ICON_BASE_DIR = "YOUR_MINT_X_ICON_PATH_HERE/mint-x-icons/usr/share/icons/Mint-X"
DEST_DIR = "YOUR_CUSTOM_THEME_PATH_HERE/Rootkit"
# Which folders you want to
ICON_FOLDERS = ['apps', 'categories', 'devices', 'mimetypes', 'places', 'status']
DIMEN_FOLDERS = ['8x8', '16x16', '22x22', '24x24', '32x32', '48x48', '256x256', 'scalable']
# Remove some icons if you don't want
REMOVE_LIST = {"devices": ['scanner', 'printer', 'system-config-printer']}
# replace some icons to the favor ones
REPLACE_LIST = {"mimetypes":{
"deb": {"apps" : "softwarecenter-debian"},
'application-x-deb': {"apps" : "softwarecenter-debian"},
"gnome-mime-application-x-deb": {"apps" : "softwarecenter-debian"} }}

# I would take the aqua styles :P
MINT_X_AQUA_BASE_DIR = 'YOUR_MINT_X_ICON_PATH_HERE/mint-x-icons/usr/share/icons/Mint-X-Aqua'
# Replace the original style
MINT_X_AQUA_ICON_FOLDERS = ['places']
MINT_X_AQUA_DIMEN_FOLDERS = ['16x16', '22x22', '24x24', '32x32', '48x48', '256x256']

def manual_fix_places(file, dimen):
	if dimen == '8x8' or dimen == '16x16':
		if file == 'stock_playlist.svg' or file == 'user-bookmarks.svg':
			return file.replace('svg', 'png')
	return file


def remove_icon(base, dimendirs, removelist):
	for icon, lst in removelist.iteritems():
		for fn in lst:
			for dimen in dimendirs:
				r = composepath(base, dimen, icon, fn)
				if exists(r + '.png'): remove(r + '.png')
				if exists(r + '.svg'): remove(r + '.svg')

def replace_icon(base, dimendirs, replacelist):
	for icon, lst in replacelist.iteritems():
		for fn, target in lst.iteritems():
			# Give a new picture
			for ticon, tfn in target.iteritems():
				tfile = composepath(ticon, tfn)

				for dimen in dimendirs:
					# Original file
					origin = composepath(base, dimen, icon, fn)
					tfinal = composepath(base, dimen, tfile)

					ext = ''
					if exists(origin + ".png"): ext = '.png'
					elif exists(origin + '.svg'): ext = '.svg'

					if ext != '':
						remove(origin + ext)
						copyfile(tfinal + ext, origin + ext)

def initialize(destdir, icondirs, dimendirs):
	debug("Initializing....")

	# Remove the folder
	if exists(destdir): rmtree(destdir)
	# Creating the folder
	mkdir(destdir)
	# Initialize the folders in base direcotry
	for folder in dimendirs:
		fn = composepath(destdir, folder)
		mkdir(fn)

		for icon in icondirs: mkdir(composepath(fn, icon))

def deepth_copy(srcdir, destdir, icondirs, dimendirs):
	#pdb.set_trace()
	print "Coping file...\n"
	# Through all of icon and dimen folders
	for icon in icondirs:
		for dimen in dimendirs:
			# The structure of Mint-X-icons folders are different to Adwaita folders
			# We should convert it to the origin name of folder
			src = compact(dimen, composepath(srcdir, icon))

			srcpath = composepath(srcdir, icon, src[0:src.index("x")])
			savepath = composepath(destdir, dimen, icon)

			if not exists(srcpath):
				debug(srcpath + " dosen't exist.")
				continue

			for file in listdir(srcpath):
				# Fix some files under PLACES folder
				fn = manual_fix_places(file, dimen)
				srcfile = composepath(srcpath, fn)
				savefile = composepath(savepath, fn)

				if not exists(srcfile):
					debug(srcfile + " dosen't exist.")
					continue

				# convert a .svg foramt to .png
				if convert(srcfile, dimen):
					srcfile = srcfile.replace(".svg", ".png")
					savefile = savefile.replace(".svg", ".png")

					move(srcfile, savefile)

					debug("Moved %s to %s" % (srcfile, savefile));
					continue

				copyfile(srcfile, savefile)

def compact(dimen, basepath):
	# The sources direcotry have no 8x8 dimens folder
	if dimen == '8x8':
		dimen = '16x16'
	elif dimen == '256x256':
		# Prefer to 128x128 dimens
		if exists(composepath(basepath, "128")):
			dimen = "128x128"
		elif exists(composepath(basepath, "96")):
			dimen = "96x96"
	elif dimen == 'scalable':
		dimen = "scalablex"

	return dimen

# Determind to convert a .svg file to .png format
def convert(file, dimen):
	# Do not convert a file in scalable folder
	if (dimen != "scalable" and file.endswith(".svg")):
		svg2png(file, dimen[0:dimen.index('x')])
		return True
	return False

def main():
	initialize(DEST_DIR, ICON_FOLDERS, DIMEN_FOLDERS)

	deepth_copy(MINT_X_ICON_BASE_DIR, DEST_DIR, ICON_FOLDERS, DIMEN_FOLDERS)
	remove_icon(DEST_DIR, DIMEN_FOLDERS, REMOVE_LIST)
	replace_icon(DEST_DIR, DIMEN_FOLDERS, REPLACE_LIST)
	# Replace the normal style
	deepth_copy(MINT_X_AQUA_BASE_DIR, DEST_DIR, MINT_X_AQUA_ICON_FOLDERS, MINT_X_AQUA_DIMEN_FOLDERS)

	buildtheme("Rootkit", DEST_DIR, "Rootkit Isn't Rootkit.", "Adwaita")

if __name__ == '__main__':
	main()
