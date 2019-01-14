#!/bin/sh

## From main __init__
if [ -e $PWD/microblog/__pycache__ ]
then
    rm -r $PWD/microblog/__pycache__
else
    echo $PWD/microblog/__pycache__ Not Found
fi

## From internal __init__
for f in $(find $PWD/microblog/app -iname __pycache__); do
    if [ -e $f ]
    then
        rm -r $f;
    else
        echo $f Not found
    fi
done


