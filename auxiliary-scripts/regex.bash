#!/bin/bash

regex='python[=<>]{1,}[0-9]+.+[0-9]+.+[0-9]+'
filename="prueba.txt"

while read line; do
        if [[ $line =~ $regex ]]
        then
            echo $line
        fi
        #ORIGIN="$(dirname "${line}")"
        #FILE="$(basename "${line}")"
        #date=$(date '+%Y-%m-%d %H:%M:%S')
        #mkdir -p "${DESTINATION}/${FILE}_${date}"
        #cp "${ORIGIN}/${FILE}" "${DESTINATION}/${FILE}_${date}/${FILE}"
    done <$filename