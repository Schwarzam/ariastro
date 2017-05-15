#!/usr/bin/python

import glob
import os
import sys
import numpy
from ariastro import *
import multiprocessing as mp


CALL_GALFIT = True  # Simulation mode or fitting mode
FEEDME_FILENAME_PREFIX = "tmp.galfit.feedme_"
TEMPLATE_FILENAME = "galfit.feedme.template.br"
EXE_PATH = "./galfitm-1.2.1-linux-x86_64"  # path to the Galfit executable file
FILENAME_TXT_TABLE = "../outputs/output-mega-califa-may.txt"



#Tries to figure out the output filename pattern from inside the template
with open(TEMPLATE_FILENAME, "r") as file:
    for line in file:
        if line.startswith("B)"):
            pieces = line.split(" ")
            OUTPUT_PATTERN = pieces[1].strip()
            print("Found output filename pattern: '{}'".format(OUTPUT_PATTERN))
            if not "@@@@@@" in OUTPUT_PATTERN:
                raise RuntimeError("Could not figure out output pattern, sorry, gotta find new solution for this")


def replace_pattern_in_template(template, pattern, str_replace):
    """pattern by galaxy name and returns new string"""
    contents1 = template.replace(pattern, str_replace)
    return contents1



# PATH = "./all-fits"
PATH = "."

# # Extract all galaxy names
ff = glob.glob(os.path.join(PATH, "psf*.fits"))
galaxy_names = []
for f in ff:
    filename = os.path.basename(f)
    # print filename
    pieces = filename.split("_")
    galaxy_name = pieces[1]
    galaxy_names.append(galaxy_name)

galaxy_names = list(set(galaxy_names))



# # Reads some input data
# template 
with open(TEMPLATE_FILENAME, "r") as file:
  template = file.read()
# Galaxy table in CSV format
#COMMAND = "sed 's/[[:space:]]\{1,\}/,/g' ../outputs/output-mega-califa.txt > output-mega-califa.cvs"
#open original file
f = open(FILENAME_TXT_TABLE)

#reads everything in a string
tudo = f.read()

# replace what you want (may use regexp)
newtudo = tudo.replace('[', '').replace(']', '')

import re
#removes spaces at the end of lines
newtudo = re.sub(' +\n', '\n', newtudo)
newtudo = re.sub('# +', '#', newtudo)
#chances spaces for commas
newtudo = re.sub(' +', ',', newtudo)

#open newfile (could be the same old one)
f2 = open('output-mega-califa.cvs','w')
#write()
f2.write(newtudo)
f2.close()

table = load_jma_gri("output-mega-califa.cvs")

# print table[0]
# sys.exit()
#p = mp.Pool(8)
#rows = p.map(f,galaxy_name)

# # Runs script for all galaxies
#FEEDME_FILENAME = "galfit.feedme"
#COMMAND = "./galfitm-1.2.1-linux-x86_64  "+FEEDME_FILENAME




def job(galaxy_name):
    """
    For each galaxy, created a "feedme" file and calls Galfit if some conditions are met (see below).

    Conditions: see source code

     Args:
         galaxy_name: str

    Returns:
        True if conditions are met and galaxy is processed by Galfit(*), False otherwise

    (*) Attention to global flag CALL_GALFIT, which was created to help debugging.
        If CALL_GALFIT is False, job() will return True even if Galfit is not called
    """
    filename_test = os.path.join(PATH, galaxy_name + "_g.fits")

    # Condition 1
    if not os.path.isfile(filename_test):
        print("**WARNING**: file '%s' not found, skipping galaxy '%s' :(" % (filename_test, galaxy_name))
        return False

    output_filename = replace_pattern_in_template(OUTPUT_PATTERN, "@@@@@@", galaxy_name)

    # Condition 2
    if os.path.isfile(output_filename):
        print("**INFO**: output file '%s' already exists, skipping galaxy '%s' :)" % (output_filename, galaxy_name))
        return False

    row = find_row_by_galaxy_name2(table, galaxy_name)

    # Condition 3
    if not row:
        print("**WARNING**: galaxy '%s' not found in table, skipping galaxy '%s' :(" % (galaxy_name, galaxy_name))
        return False

    width, height = get_dims(filename_test)

    # If the following is put 'True', just pretends that galaxy will be processed, but does noth
    print(("**Info**: GONNA PROCESS GALAXY {}".format(galaxy_name)))

    # expt_u=float(get_exptime(os.path.join(PATH, galaxy_name + "_u.fits")))
    zpu = 24.63 - 2.5 * numpy.log10(float(get_exptime(os.path.join(PATH, galaxy_name + "_u.fits"))))
    zpg = 25.11 - 2.5 * numpy.log10(float(get_exptime(os.path.join(PATH, galaxy_name + "_g.fits"))))
    zpr = 24.80 - 2.5 * numpy.log10(float(get_exptime(os.path.join(PATH, galaxy_name + "_r.fits"))))
    zpi = 24.36 - 2.5 * numpy.log10(float(get_exptime(os.path.join(PATH, galaxy_name + "_i.fits"))))
    zpz = 22.83 - 2.5 * numpy.log10(float(get_exptime(os.path.join(PATH, galaxy_name + "_z.fits"))))

    mag_u = row["COMP2_MAG_U"]
    mag_g = row["COMP2_MAG_G"]
    mag_r = row["COMP2_MAG_R"]
    mag_i = row["COMP2_MAG_I"]
    mag_z = row["COMP2_MAG_Z"]
    n_u = row["COMP2_n_U"]
    n_g = row["COMP2_n_G"]
    n_r = row["COMP2_n_R"]
    n_i = row["COMP2_n_I"]
    n_z = row["COMP2_n_Z"]
    re_u = row["COMP2_Re_U"]
    re_g = row["COMP2_Re_G"]
    re_r = row["COMP2_Re_R"]
    re_i = row["COMP2_Re_I"]
    re_z = row["COMP2_Re_Z"]
    ar_u = row["COMP2_AR_U"]
    ar_g = row["COMP2_AR_G"]
    ar_r = row["COMP2_AR_R"]
    ar_i = row["COMP2_AR_I"]
    ar_z = row["COMP2_AR_Z"]

    # except:
    #    print "Could not find galaxy '%s' in table" % galaxy_name

    contents = replace_pattern_in_template(template, "@@@@@@", galaxy_name)
    contents = replace_pattern_in_template(contents, "WWWWWW", str(width))
    contents = replace_pattern_in_template(contents, "HHHHHH", str(height))
    contents = replace_pattern_in_template(contents, "ZPU", str(float(zpu)))
    contents = replace_pattern_in_template(contents, "ZPG", str(float(zpg)))
    contents = replace_pattern_in_template(contents, "ZPR", str(float(zpr)))
    contents = replace_pattern_in_template(contents, "ZPI", str(float(zpi)))
    contents = replace_pattern_in_template(contents, "ZPZ", str(float(zpz)))
    contents = replace_pattern_in_template(contents, "XUXUXU", row["COMP2_XC_U"])
    contents = replace_pattern_in_template(contents, "XGXGXG", row["COMP2_XC_G"])
    contents = replace_pattern_in_template(contents, "XRXRXR", row["COMP2_XC_R"])
    contents = replace_pattern_in_template(contents, "XIXIXI", row["COMP2_XC_I"])
    contents = replace_pattern_in_template(contents, "XZXZXZ", row["COMP2_XC_Z"])
    contents = replace_pattern_in_template(contents, "YUYUYU", row["COMP2_YC_U"])
    contents = replace_pattern_in_template(contents, "YGYGYG", row["COMP2_YC_G"])
    contents = replace_pattern_in_template(contents, "YRYRYR", row["COMP2_YC_R"])
    contents = replace_pattern_in_template(contents, "YIYIYI", row["COMP2_YC_I"])
    contents = replace_pattern_in_template(contents, "YZYZYZ", row["COMP2_YC_Z"])
    contents = replace_pattern_in_template(contents, "BKGU", row["COMP1_SKY_U"])
    contents = replace_pattern_in_template(contents, "BKGG", row["COMP1_SKY_G"])
    contents = replace_pattern_in_template(contents, "BKGR", row["COMP1_SKY_R"])
    contents = replace_pattern_in_template(contents, "BKGI", row["COMP1_SKY_I"])
    contents = replace_pattern_in_template(contents, "BKGZ", row["COMP1_SKY_Z"])
    contents = replace_pattern_in_template(contents, "MMABU", str(float(mag_u) + 1.5))
    contents = replace_pattern_in_template(contents, "MMABG", str(float(mag_g) + 1.5))
    contents = replace_pattern_in_template(contents, "MMABR", str(float(mag_r) + 1.5))
    contents = replace_pattern_in_template(contents, "MMABI", str(float(mag_i) + 1.5))
    contents = replace_pattern_in_template(contents, "MMABZ", str(float(mag_z) + 1.5))
    contents = replace_pattern_in_template(contents, "MMADU", str(float(mag_u) + 0.65))
    contents = replace_pattern_in_template(contents, "MMADG", str(float(mag_g) + 0.65))
    contents = replace_pattern_in_template(contents, "MMADR", str(float(mag_r) + 0.65))
    contents = replace_pattern_in_template(contents, "MMADI", str(float(mag_i) + 0.65))
    contents = replace_pattern_in_template(contents, "MMADZ", str(float(mag_z) + 0.65))
    contents = replace_pattern_in_template(contents, "NNBG", str(
        (float(n_u) + float(n_g) + float(n_r) + float(n_i) + float(n_z)) / 5))
    contents = replace_pattern_in_template(contents, "ARDG", str(
        (float(ar_u) + float(ar_g) + float(ar_r) + float(ar_i) + float(ar_g)) / 5))
    contents = replace_pattern_in_template(contents, "REBU", str(float(re_u) * 0.3))
    contents = replace_pattern_in_template(contents, "REBG", str(float(re_g) * 0.3))
    contents = replace_pattern_in_template(contents, "REBR", str(float(re_r) * 0.3))
    contents = replace_pattern_in_template(contents, "REBI", str(float(re_i) * 0.3))
    contents = replace_pattern_in_template(contents, "REBZ", str(float(re_z) * 0.3))
    contents = replace_pattern_in_template(contents, "REDU", str(float(re_u) * 1.5))
    contents = replace_pattern_in_template(contents, "REDG", str(float(re_g) * 1.5))
    contents = replace_pattern_in_template(contents, "REDR", str(float(re_r) * 1.5))
    contents = replace_pattern_in_template(contents, "REDI", str(float(re_i) * 1.5))
    contents = replace_pattern_in_template(contents, "REDZ", str(float(re_z) * 1.5))

    #        contents = replace_pattern_in_template(contents, "XXXXXX", str(float(width)/2))
    #        contents = replace_pattern_in_template(contents, "YYYYYY", str(float(height)/2))

    feedme_filename = FEEDME_FILENAME_PREFIX+galaxy_name
    command = EXE_PATH+" "+feedme_filename

    with open(feedme_filename, "w") as file:
        file.write(contents)

    if CALL_GALFIT:
        os.system(command)

    return True



# flags = [job(galaxy_name) for galaxy_name in galaxy_names]

p = mp.Pool(8)
flags = p.map(job, galaxy_names)


igal = sum(flags)

##Read outputs from the SS fit
#create_output_table("../outputs")
#sys.exit()

print("I fit", igal,"galaxies")

#    pieces = os.path.basename(f)

