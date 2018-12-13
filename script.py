#! /usr/bin/python3

import sys
from sys import exit

from os import access, R_OK
from os.path import isfile

import string

from re import search, sub

from json import loads


# 1)OK)
#	OK)	check argv[]
#	 	OK)	is a file ?
#	 	OK)	with the good right ?
#	 	OK)	is a valid json ?
# 2)OK)
# 	OK) load data in var
# 		OK) open -> get fd
# 		OK) read -> data
# 		OK) load them
#
# 3)OK)	extract data
# 		OK) # regex Street
# 		OK) # regex Date
# 		OK) # format in list
#		OK) # Concatene list


def exit_error():
	print("Usage: ./script.py FILE1 [FILE2, ...]")
	exit(1)


def get_json(file):
	try:
		file_content = open(file)
		json_content = file_content.read()		# Can be minify as:
		json_object = loads(json_content)		# json_object = loads(file_content.read())
		return json_object
	except:
		print("Error file format : \"%s\" is not a valid json file." % file, file=sys.stderr)
		raise


def check_file(file):
	if isfile(file):
		if access(file, R_OK):
			return
		print("Error file permissions : \"%s\" is not readable." % file, file=sys.stderr)
		raise
	print("Error file name : \"%s\" does not exist." % file, file=sys.stderr)
	raise

# We want to exract names of people who:
# -- live in a 'Street' (no 'Avenue', no 'Place', etc)
# -- and have been registered before NOV 2017
def extract_data(json_object):
	list_name = []
	for profil in json_object['profils']:
		if search(r' Street,', profil['address']):
			date = int(sub('[^%s]' % string.digits, '', profil['registered'][:7]))
			if (date <= 201711):
				list_name.append(profil['name'])
	return list_name


if __name__ == '__main__':

	final_data = []
	ret_value = 0


	if len(sys.argv) == 1:
		exit_error()

	# Check all files passed in argument
	for file in sys.argv[1:]:
		try:
			check_file(file)
			json_object = get_json(file)
			final_data += extract_data(json_object)

		except:
			ret_value |= 1
			pass

	if len(final_data) != 0:
		print (final_data)

	exit(ret_value)
































##
