#!/usr/bin/env sh

echo "SWAG"
python3 -u ./SerialSensor.py --input $1 --output /tmp/togetic-0 > ./donnees_capteur/valeur_brutes_sans_mouvement.dat &
echo ${pidSensor}
pidSensor=$!
echo "Attente pendant 60 secondes"
sleep 60
echo "Assez attendu, on kill le $pidSensor"
kill -9 $pidSensor
cd donnees_capteur/
echo "data transformation"
python2 ./data_transform.py valeur_brutes_sans_mouvement.dat
echo "plot"
python2 ./plot.py
echo "FINI"
# ./Filter.py --input /tmp/togetic-1 &
# pidFilter=$!
