#!/bin/bash

for GET_DATE in "$@"
do
    mkdir $GET_DATE
    cd $GET_DATE
    curl --fail -O http://archive.routeviews.org/bgpdata/${GET_DATE:0:4}.${GET_DATE:4:2}/UPDATES/updates.$GET_DATE.[00-23][00-45:15].bz2
    cd ..
done