#!/usr/bin/env bash

#
# This script is used to pre-process train and test data
# in order to extract additional features.
#

# make folder where to store the files
mkdir -p "data"

# create new features and merge them together
root="data_raw"
dest="data"
for type in "train" "test"; do

	# compute files to put together
	features="${root}/NLSPARQL.${type}.feats.txt"
	tags="${root}/NLSPARQL.${type}.data"
	capitalized="${dest}/${type}-capitalized.txt"
	languages="${dest}/${type}-languages.txt"
	prexif1="${dest}/${type}-prexif1.txt"
	prexif2="${dest}/${type}-prexif2.txt"
	prexif3="${dest}/${type}-prexif3.txt"
	suffix1="${dest}/${type}-suffix1.txt"
	suffix2="${dest}/${type}-suffix2.txt"
	suffix3="${dest}/${type}-suffix3.txt"

	# word is capitalized
	cat ${features} | cut -f 3 | sed 's/^[[:upper:]].*$/Capitalized/' | sed 's/^[^A-Z].*/-/' > ${capitalized}

	# languages (# = match, - = not match)
	cat ${features} | cut -f 3 | sed -e "$(sed 's:.*:s/&/#/ig:' extra/languages)" | sed 's/^.*#.*$/#/' | sed 's/^[^#].*/-/' > ${languages}

	# prexix
	cat ${features} | cut -f 1 | cut -c 1 > ${prexif1}
	cat ${features} | cut -f 1 | cut -c 1-2 > ${prexif2}
	cat ${features} | cut -f 1 | cut -c 1-3 > ${prexif3}

	# suffix
	cat ${features} | cut -f 1 | rev | cut -c 1 | rev > ${suffix1}
	cat ${features} | cut -f 1 | rev | cut -c 1-2 | rev > ${suffix2}
	cat ${features} | cut -f 1 | rev | cut -c 1-3 | rev > ${suffix3}

	# generate final file
	# total cols: 3 + 1+1+1 + 1+1+1 + 1 + 1 + (1)+1
	paste ${features} ${capitalized} ${languages} ${prexif1} ${prexif2} ${prexif3} ${suffix1} ${suffix2} ${suffix3} ${tags} | cut -f 1-11,13 > "${dest}/${type}.txt"

	# cleanup
	rm -f ${capitalized}
	rm -f ${prexif1}
	rm -f ${prexif2}
	rm -f ${prexif3}
	rm -f ${suffix1}
	rm -f ${suffix2}
	rm -f ${suffix3}
	rm -f ${languages}

done
