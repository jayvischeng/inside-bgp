#!/bin/bash

CITY="amsterdam"
YEAR="2013"
MONTH="04"
mkdir ${CITY}
cd ${CITY}
mkdir ${YEAR}
cd ${YEAR}
mkdir ${MONTH}
cd ${MONTH}
for DAY in {01..30}
do
    echo ">> Retrieving day ${DAY}"
    mkdir ${YEAR}${MONTH}${DAY}
    cd ${YEAR}${MONTH}${DAY}
    for HOUR in {00..23}
    do
        for MINUTE in {00..55..5}
        do
            curl --limit-rate 400K --fail -O http://data.ris.ripe.net/rrc00/${YEAR}.${MONTH}/updates.${YEAR}${MONTH}${DAY}.${HOUR}${MINUTE}.gz
        done
    done
    cd ..
done
