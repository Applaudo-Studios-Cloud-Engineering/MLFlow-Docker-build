#!/bin/bash

filename="./temp_artifacts/conda.yaml"
formatedfile="formated.yaml"
dependencies="dependencies.yaml"
temp="temp.txt"
import="import.txt"
template1="./templates/DockerTemplate1"
template2="./templates/DockerTemplate2"

sed "s/[<=>]\{1,\}/:/" < $filename > $formatedfile

regexpython='python[:]{1,}[0-9]{1,}.{1}[0-9]{1,}.{1}[0-9]{1,}'
regexpip='pip[:]{1}'
regexname='name[:]{1}'

array=()
flag=false
aux=0
auxini=0
auxend=0

while read line; do
        aux=$((aux+1))
        if [[ $line =~ $regexpip ]]
        then
            auxini=$((aux+1))
        fi
        if [[ $line =~ $regexname ]]
        then
            auxend=$((aux-1))
        fi
    done <$filename
declare -p array

#newformated=$(sed '3i New Line with sed' $formatedfile)
#echo $newformated > $formatedfile

sed "${auxini},${auxend}!d" < $filename > $dependencies.temp
sed "s/  - /RUN pip install /" < $dependencies.temp > $dependencies

rm $dependencies.temp
pyversion=""
while read line; do
        if [[ $line =~ $regexpython ]]
        then
            pyversion=$line
            #IFS='='
            #read -a strarr <<< "$line"
            #for val in "${strarr[@]}";
            #do
            #    array+=("$val")
            #done
            #flag=true
        fi
    done <$formatedfile

echo $pyversion > temp.txt
sed "s/- /FROM /" < temp.txt > $import
rm $temp
rm $formatedfile
echo $pyversion

cat $import > DockerFile
rm $import

cat $template1 >> DockerFile

cat $dependencies >> DockerFile
rm $dependencies

cat $template2 >> DockerFile