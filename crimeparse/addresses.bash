#!/bin/bash
# Look up recent crimes at addresses we have on file

for FILE in `ls addresses`; do
    echo '**************************'
    echo $FILE
    echo '**************************'
    while IFS='|' read -ra RECORD; do
        echo ${RECORD[0]} ',' ${RECORD[1]} ':'
        #./parse.py --action specific --address ${RECORD[1]}
        ./parse.py --action search --address "${RECORD[1]}"
    done < addresses/$FILE
done
