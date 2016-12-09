#!/usr/bin/python

import glob
import os
from ariastro import *
import numpy
import sys


# # Definition of constants


PROCESS_GALAXIES = False  # Simulation mode or fitting mode
FEEDME_FILENAME = "galfit.feedme"
TEMPLATE_FILENAME = "galfit.feedme.template"
COMMAND = "./galfitm-1.2.1-linux-x86_64  " + FEEDME_FILENAME
FILENAME_CSV_TABLE = "all-gal.csv"

# Tries to figure out the output filename pattern from inside the template
with open(TEMPLATE_FILENAME, "r") as file:
    for line in file:
        if line.startswith("B)"):
            pieces = line.split(" ")
            OUTPUT_PATTERN = pieces[1].strip()
            print "Found output filename pattern: '{}'".format(OUTPUT_PATTERN)
            if not "@@@@@@" in OUTPUT_PATTERN:
                raise RuntimeError("Could not figure out output pattern, sorry, gotta find new solution for this")

# PATH = "./all-fits"
PATH = "."

#
#
#

def replace_pattern_in_template(template, pattern, str_replace):
    """pattern by galaxy name and returns new string"""
    contents1 = template.replace(pattern, str_replace)
    return contents1



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
table = load_jma_gri(FILENAME_CSV_TABLE)

#print table[0]
# sys.exit()


# # Runs script for all galaxies

# print(galaxy_names)
# sys.exit()

igal = 0

for galaxy_name in galaxy_names:
    filename_test = os.path.join(PATH, galaxy_name + "_g.fits")

    # # Next is a series of tests to determine whether the galaxy will be **really** processed
    # If it is decided that it will not, a 'continue' statement will skip to the beginning of the next 'for' iteration

    # Test 0
    output_filename = replace_pattern_in_template(OUTPUT_PATTERN, "@@@@@@", galaxy_name)
    if os.path.isfile(output_filename):
        print "**INFO**: output file '%s' already exists, skipping galaxy '%s' :)" % (output_filename, galaxy_name)
        continue


    # Test 1
    if not os.path.isfile(filename_test):
        msg = "**WARNING**: file '%s' not found, skipping galaxy '%s' :(" % (filename_test, galaxy_name)
        print msg
        write_not_run(galaxy_name, msg)
        continue

    row = find_row_by_galaxy_name(table, galaxy_name)

    # Test 2
    if not row:
        msg = "**WARNING**: galaxy '%s' not found in table :(" % (galaxy_name,)
        print msg
        write_not_run(galaxy_name, msg)
        continue

    columns_needed = ["x0Fit2D_u", "x0Fit2D_g", "x0Fit2D_r", "x0Fit2D_i", "x0Fit2D_z", "y0Fit2D_u", "y0Fit2D_g",
                      "y0Fit2D_r", "y0Fit2D_i", "y0Fit2D_z", "skybg_u", "skybg_g",
                      "skybg_r", "skybg_i", "skybg_z", "u", "g", "r", "i", "z"]


    # Test 3
    for name in columns_needed:
        if not row[name]:
            msg = "**WARNING**: row '%s' is empty, cannot process galaxy '%s' :(" % (name, galaxy_name)
            print msg
            write_not_run(galaxy_name, msg)
            continue
            # break


    width, height = get_dims(filename_test)

    get_exptime(os.path.join(PATH, galaxy_name + "_u.fits"))

    row = find_row_by_galaxy_name(table, galaxy_name)

    # Test 4
    if not row:
        continue


    # **If reached this point in the code it is because the galaxy will be processed**

    # except:
    #    print "Could not find galaxy '%s' in table" % galaxy_name


    # If the following is put 'True', just pretends that galaxy will be processed, but does noth

    print("**Info**: GONNA PROCESS GALAXY {}".format(galaxy_name))
    igal = igal +1

    if not PROCESS_GALAXIES:
        continue

    zpu=24.63-2.5*numpy.log10(get_exptime(os.path.join(PATH, galaxy_name + "_u.fits")))
    zpg=25.11-2.5*numpy.log10(get_exptime(os.path.join(PATH, galaxy_name + "_g.fits")))
    zpr=24.80-2.5*numpy.log10(get_exptime(os.path.join(PATH, galaxy_name + "_r.fits")))
    zpi=24.36-2.5*numpy.log10(get_exptime(os.path.join(PATH, galaxy_name + "_i.fits")))
    zpz=22.83-2.5*numpy.log10(get_exptime(os.path.join(PATH, galaxy_name + "_z.fits")))

    contents = replace_pattern_in_template(template, "@@@@@@", galaxy_name)
    contents = replace_pattern_in_template(contents, "WWWWWW", str(width))
    contents = replace_pattern_in_template(contents, "HHHHHH", str(height))
    contents = replace_pattern_in_template(contents, "ZPU", str(float(zpu)))
    contents = replace_pattern_in_template(contents, "ZPG", str(float(zpg)))
    contents = replace_pattern_in_template(contents, "ZPR", str(float(zpr)))
    contents = replace_pattern_in_template(contents, "ZPI", str(float(zpi)))
    contents = replace_pattern_in_template(contents, "ZPZ", str(float(zpz)))
    contents = replace_pattern_in_template(contents, "XUXUXU", row["x0Fit2D_u"])
    contents = replace_pattern_in_template(contents, "XGXGXG", row["x0Fit2D_g"])
    contents = replace_pattern_in_template(contents, "XRXRXR", row["x0Fit2D_r"])
    contents = replace_pattern_in_template(contents, "XIXIXI", row["x0Fit2D_i"])
    contents = replace_pattern_in_template(contents, "XZXZXZ", row["x0Fit2D_z"])
    contents = replace_pattern_in_template(contents, "YUYUYU", row["x0Fit2D_u"])
    contents = replace_pattern_in_template(contents, "YGYGYG", row["y0Fit2D_g"])
    contents = replace_pattern_in_template(contents, "YRYRYR", row["y0Fit2D_r"])
    contents = replace_pattern_in_template(contents, "YIYIYI", row["y0Fit2D_i"])
    contents = replace_pattern_in_template(contents, "YZYZYZ", row["x0Fit2D_z"])
    contents = replace_pattern_in_template(contents, "BKGU", row["skybg_u"])
    contents = replace_pattern_in_template(contents, "BKGG", row["skybg_g"])
    contents = replace_pattern_in_template(contents, "BKGR", row["skybg_r"])
    contents = replace_pattern_in_template(contents, "BKGI", row["skybg_i"])
    contents = replace_pattern_in_template(contents, "BKGZ", row["skybg_z"])
    contents = replace_pattern_in_template(contents, "MMAGU", row["u"])
    contents = replace_pattern_in_template(contents, "MMAGG", row["g"])
    contents = replace_pattern_in_template(contents, "MMAGR", row["r"])
    contents = replace_pattern_in_template(contents, "MMAGI", row["i"])
    contents = replace_pattern_in_template(contents, "MMAGZ", row["z"])

    #        contents = replace_pattern_in_template(contents, "XXXXXX", str(float(width)/2))
    #        contents = replace_pattern_in_template(contents, "YYYYYY", str(float(height)/2))


    with open(FEEDME_FILENAME, "w") as file:
        file.write(contents)

    os.system(COMMAND)


   #break

##Read outputs from the SS fit
# create_output_table("../outputs")
# XSsys.exit()



#    pieces = os.path.basename(f)

print "I fit", igal,"galaxies"
