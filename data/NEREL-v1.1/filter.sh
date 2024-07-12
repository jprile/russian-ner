#!/bin/bash

# Delete all .ann files without PERSON tokens
grep -r -L -Z 'PERSON' */*.ann | xargs --null rm

# Clear all lines not in {PERSON, ABBREVIATION, ALTERNATIVE_NAME}
for filename in ./*/*.ann; do
    sed -i '/PERSON\|ABBREVIATION\|ALTERNATIVE_NAME/!d' $filename
done

# Clear all lines with {ABBREVIATION | ALTERNATIVE_NAME} where the args dont exist
for filename in ./*/*.ann; do
    cat $filename | while read line
    do
        if [[ $line =~ (ABBREVIATION|ALTERNATIVE_NAME) ]]; then
            ssa="Arg1:" ; ssb=" Arg2:"
            token="${line#*${ssa}}" ; token="${token%${ssb}*}"
            if ! grep -q "$token\sPERSON" $filename ; then
                sed -i "/$line/d" $filename
            fi
        fi
    done
done

# Delete all .txt files without an equivalent .ann file
for filename in ./*/*.txt; do
    if [[ ! -f ${filename%%.txt}.ann ]]; then
        rm $filename
    fi
done