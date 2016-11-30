#!/usr/bin/python

import glob
import os
import sys

from ariastro import *


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


# # Reads some input data
# template 
with open("galfit.feedme.template.br", "r") as file:
  template = file.read()
# Galaxy table in CSV format
#COMMAND = "sed 's/[[:space:]]\{1,\}/,/g' ../outputs/output-mega-califa.txt > output-mega-califa.cvs"
#open original file
f = open('../outputs/output-mega-califa.txt')

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


# # Runs script for all galaxies
FEEDME_FILENAME = "galfit.feedme"
COMMAND = "./galfitm-1.1.8-osx "+FEEDME_FILENAME
for galaxy_name in galaxy_names:
    filename_test = os.path.join(PATH, galaxy_name+"_g.fits")

    goes = True
    if not os.path.isfile(filename_test):
        print "**WARNING**: file '%s' not found, skipping galaxy '%s' :(" % (filename_test, galaxy_name)
        goes = False

    if goes:
        row = find_row_by_galaxy_name2(table, galaxy_name)

        if not row:
            print "**WARNING**: galaxy '%s' not found in table :(" % (galaxy_name,)
            goes = False

    if goes:
        columns_needed = ["2_XC_G", "2_YC_G", "2_XC_R", "2_YC_R", "2_XC_I", "2_YC_I", "1_SKY_0",
                          "1_SKY_1", "1_SKY_2", "2_MAG_G", "2_MAG_R", "2_MAG_I","2_RE_G","2_RE_R","2_RE_I","2_N_R","2_N_G","2_N_I",
                          "2_AR_G","2_AR_R","2_AR_I",]
        
        #for name in columns_needed:
            #if not row[name]:
                #print "**WARNING**: row '%s' is empty, cannot process galaxy '%s' :(" % (name, galaxy_name)
                #goes = False
                #break

    if goes:
        width, height = get_dims(filename_test)

        row = find_row_by_galaxy_name2(table, galaxy_name)
        mag_g= row["2_MAG_G"]
        mag_r= row["2_MAG_R"]
        mag_i= row["2_MAG_I"]
        n_g= row["2_N_G"]
        n_r= row["2_N_R"]
        n_i= row["2_N_I"]
        re_g= row["2_RE_G"]
        re_r= row["2_RE_R"]
        re_i= row["2_RE_I"]
        ar_g= row["2_AR_G"]
        ar_r= row["2_AR_R"]
        ar_i= row["2_AR_I"]
        
        #except:
        #    print "Could not find galaxy '%s' in table" % galaxy_name

        if row:            
            contents = replace_pattern_in_template(template, "@@@@@@", galaxy_name)
            contents = replace_pattern_in_template(contents, "WWWWWW", str(width))
            contents = replace_pattern_in_template(contents, "HHHHHH", str(height))
            contents = replace_pattern_in_template(contents, "XGXGXG", row["2_XC_G"])
            contents = replace_pattern_in_template(contents, "XRXRXR", row["2_XC_R"])
            contents = replace_pattern_in_template(contents, "XIXIXI", row["2_XC_I"])
            contents = replace_pattern_in_template(contents, "YGYGYG", row["2_YC_G"])
            contents = replace_pattern_in_template(contents, "YRYRYR", row["2_YC_R"])
            contents = replace_pattern_in_template(contents, "YIYIYI", row["2_YC_I"])
            contents = replace_pattern_in_template(contents, "BKGG", row["1_SKY_0"])
            contents = replace_pattern_in_template(contents, "BKGR", row["1_SKY_1"])
            contents = replace_pattern_in_template(contents, "BKGI", row["1_SKY_2"])
            contents = replace_pattern_in_template(contents, "MMABG", str(float(mag_g)+1.5))
            contents = replace_pattern_in_template(contents, "MMABR", str(float(mag_r)+1.5))
            contents = replace_pattern_in_template(contents, "MMABI", str(float(mag_i)+1.5))
            contents = replace_pattern_in_template(contents, "MMADG", str(float(mag_g)+0.65))
            contents = replace_pattern_in_template(contents, "MMADR", str(float(mag_r)+0.65))
            contents = replace_pattern_in_template(contents, "MMADI", str(float(mag_i)+0.65))
            contents = replace_pattern_in_template(contents, "NNBG", str((float(n_g)+float(n_r)+float(n_i))/3))
            contents = replace_pattern_in_template(contents, "ARDG", str((float(ar_g)+float(ar_r)+float(ar_i))/3))
            contents = replace_pattern_in_template(contents, "REBG", str(float(re_g)*0.3))
            contents = replace_pattern_in_template(contents, "REBR", str(float(re_r)*0.3))
            contents = replace_pattern_in_template(contents, "REBI", str(float(re_i)*0.3))
            contents = replace_pattern_in_template(contents, "REDG", str(float(re_g)*1.5))
            contents = replace_pattern_in_template(contents, "REDR", str(float(re_r)*1.5))
            contents = replace_pattern_in_template(contents, "REDI", str(float(re_i)*1.5))


#        contents = replace_pattern_in_template(contents, "XXXXXX", str(float(width)/2))
#        contents = replace_pattern_in_template(contents, "YYYYYY", str(float(height)/2))
        
            with open(FEEDME_FILENAME, "w") as file:
                file.write(contents)
            os.system(COMMAND)  
#	break

##Read outputs from the SS fit
create_output_table("../outputs")
sys.exit()



#    pieces = os.path.basename(f)

