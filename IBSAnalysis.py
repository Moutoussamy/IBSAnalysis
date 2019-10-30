#!/usr/bin/env python 

import sys
import re
import os
import argparse


"""
This script allow to compute the number of LYS ang ARG at the IBS.
Args : A pdb file processe by OPM
return : the number of ASP,GLU,ARG and LYS at the IBS
"""
__author__ = "Emmanuel Edouard MOUTOUSSAMY"
__version__  = "1.0.0"
__date__ = "2016/02"
__copyright__ = "CC_by_SA"
__dependencies__ = "sys and re module"


def GetArgs():

	"""
	Get the arguments: PDB and distance
	:return: arg.i = PDB and arg.d = distance from the bilayer plane
	"""
	parser = argparse.ArgumentParser(description='dddd.')

	parser.add_argument('-i', metavar = "pdb", type = str, help = "pdb file")
	parser.add_argument('-d', metavar="dist.", default=10, type=int, help= "distance from the bilayer plane")

	args = parser.parse_args()

	return args

def check_position(z_value,d):
	"""
	This function allow to check if the z value of an atom is between 0 and d or
	between 0 and -d.
	Args : a z value of an atom and a distance d
	Return : a boolean (0: the z value of the atom is not in the good range)
	"""
	flag = 0

	if z_value >= 0 and  z_value <= (15.400 + d):
		flag = 1
	elif z_value <= 0 and  z_value >= (-15.400 - d):
		flag = 1

	return flag



def compute_distance(pdb,Cut_off):
	"""
	This fonction count the number of positiv and negativ residues at the IBS.
	Args: a pdb id, a distance and the list of file of your directory
	Return : basic (# of basic residues) and acidic (# of acidic residues)
	"""

	basic = 0
	acidic = 0

	regex_basic = re.compile("ATOM.{9}CA {2}(LYS|ARG)")
	regex_acidic = re.compile("ATOM.{9}CA {2}(GLU|ASP)")

	pdb = open(pdb,"r")

	for line in pdb:
		if regex_basic.search(line):
			flag = check_position(float(line[46:54]),Cut_off)
			if flag == 1:
				print(line)
				basic += 1

		elif regex_acidic.search(line):
			flag = check_position(float(line[46:54]),Cut_off)
			if flag == 1:
				print(line)
				acidic += 1

	pdb.close()

	return basic,acidic

				

if __name__ == "__main__":


	args = GetArgs()

	basic,acidic = compute_distance(args.i,args.d)
	print("\n%s #Basic = %i and #acidic = %i \n"%(args.i,basic,acidic))



	
