#!/usr/bin/env bash

mongoexport -d infotheoretic -c k_simulation --fieldFile fields.txt --type=csv --out kuramoto.csv -q '{ "beta": { "$lt": 1 } }'