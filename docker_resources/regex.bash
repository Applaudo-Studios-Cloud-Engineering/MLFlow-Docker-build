#!/bin/bash

filename="./temp_artifacts/conda.yaml"
formatedfile="formated.yaml"
dependencies="dependencies.yaml"
temp="temp.txt"
import="import.txt"
template1="./templates/DockerTemplate1"
template2="./templates/DockerTemplate2"
dockerFile="DockerFile"

sed "s/[<=>]\{1,\}/:/" < $filename > $formatedfile

regexpython='python[:]{1,}[0-9]{1,}.{1}[0-9]{1,}.{1}[0-9]{1,}'
regexpip='pip[:]{1}'
regexname='name[:]{1}'

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

sed "${auxini},${auxend}!d" < $filename > $dependencies.temp
sed "s/[ ]\{1,\}[-]\{1\}[ ]\{1\}/RUN pip install /" < $dependencies.temp > $dependencies
rm $dependencies.temp

pythonversion=""

while read line; do
        if [[ $line =~ $regexpython ]]
        then
            pythonversion=$line
        fi
    done <$formatedfile

echo "$pythonversion" > temp.txt
sed "s/[-]\{1\}[ ]\{1\}/FROM /" < temp.txt > $import
rm $temp
rm $formatedfile

cat $import > $dockerFile
rm $import

cat $template1 >> $dockerFile

cat $dependencies >> $dockerFile
rm $dependencies

cat $template2 >> $dockerFile