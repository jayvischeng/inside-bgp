#!/bin/bash

CITY="oregon"
YEAR="2013"
MONTH="05"
mkdir ${CITY}
cd ${CITY}
mkdir ${YEAR}
cd ${YEAR}
mkdir ${MONTH}
cd ${MONTH}
for DAY in {29..30}
do
    echo ">> Retrieving day ${DAY}"
    mkdir ${YEAR}${MONTH}${DAY}
    cd ${YEAR}${MONTH}${DAY}
    curl --limit-rate 400K --fail -O http://data.ris.ripe.net/rrc15/${YEAR}.${MONTH}/updates.${YEAR}${MONTH}${DAY}.[00-23][00-55:5].gz
    #curl --limit-rate 400K --fail -O http://archive.routeviews.org/bgpdata/${YEAR}.${MONTH}/UPDATES/updates.${YEAR}${MONTH}${DAY}.[00-23][00-55:15].bz2
    cd ..
done