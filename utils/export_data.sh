#!/usr/bin/env bash

mongoexport -d infotheoretic -c kuramoto_simulation --fieldFile fields.txt --type=csv --out kuramoto_gamma_5.csv -q '{ threshold: 0.5 }'
mongoexport -d infotheoretic -c kuramoto_simulation --fieldFile fields.txt --type=csv --out kuramoto_gamma_6.csv -q '{ threshold: 0.6 }'
mongoexport -d infotheoretic -c kuramoto_simulation --fieldFile fields.txt --type=csv --out kuramoto_gamma_7.csv -q '{ threshold: 0.7 }'
mongoexport -d infotheoretic -c kuramoto_simulation --fieldFile fields.txt --type=csv --out kuramoto_gamma_8.csv -q '{ threshold: 0.8 }'
mongoexport -d infotheoretic -c kuramoto_simulation --fieldFile fields.txt --type=csv --out kuramoto_gamma_9.csv -q '{ threshold: 0.9 }'
