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
	parser = argparse.ArgumentParser(description='IBS composition Anlaysis') #Title

	parser.add_argument('-i', metavar = "pdb", type = str, help = "pdb file") #Argument for the pdb
	parser.add_argument('-d', metavar="dist.", default=10, type=int, help= "distance from the bilayer plane") #distance

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

	if z_value >= 0 and  z_value <= (15.400 + d): #check if the CA is within the distance d above the membrane plane
		flag = 1

	elif z_value <= 0 and  z_value >= (-15.400 - d):#check if the CA is within the distance d under the membrane plane
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
	basicAA,acidicAA = [],[]
	regex_basic = re.compile("ATOM.{9}CA {2}(LYS|ARG)") #regex for basic AA
	regex_acidic = re.compile("ATOM.{9}CA {2}(GLU|ASP)")#regex for acidic AA

	pdb = open(pdb,"r")

	for line in pdb:
		if regex_basic.search(line):
			flag = check_position(float(line[46:54]),Cut_off)
			if flag == 1:
				basic += 1
				aaInfos = "%s_%s"%(line[17:20],line[22:26])
				basicAA.append(aaInfos)


		elif regex_acidic.search(line):
			flag = check_position(float(line[46:54]),Cut_off)
			if flag == 1:
				acidic += 1
				aaInfos = "%s_%s" % (line[17:20], line[22:26])
				acidicAA.append(aaInfos)

	pdb.close()

	return basic,acidic,basicAA,acidicAA

def PrintAA(basicAA,acidicAA):
	"""
	Print the residues close to the membrane plane
	:param basicAA: list of basic amino acid close to the membrane plane
	:param acidicAA: list of acidic amino acid close to the membrane plane
	:return:
	"""

	print("\nBasic AA close to membrane plane:")
	for basic in basicAA:
		print(basic.replace("_",""))

	print("\n")

	print("Acidic AA close to membrane plane:")
	for acidic in acidicAA:
		print(acidic.replace("_",""))


if __name__ == "__main__":


	args = GetArgs() # get arguments
	basic,acidic,basicAA,acidicAA = compute_distance(args.i,args.d)
	PrintAA(basicAA,acidicAA)
	print("\n%s #Basic = %i and #acidic = %i \n"%(args.i,basic,acidic))
