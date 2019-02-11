#!/bin/sh

cd "$(dirname "$0")"

#Parse Weather and replace placeholder text in the svg template file
#python parse_weather.py
export TZ='America/Los_Angeles'

now=$(date +"%I:%M %p")

#dayWeek = $(date +"%A")
#echo $dayWeek
#cp weather-processed.svg weather-processed-tme.svg
sed  's/Bothell/'"$now"'/g' weather-processed.svg > weather-processed-tme.svg
#sed  's/As of TIME/'"$dayWeek"'/g' weather-processed.svg > weather-processed-tme.svg
#convert svg to png, and rotate 90 degrees for horizontal view
convert -depth 8 -rotate 0 weather-processed-tme.svg weather-processed-tme.png

#We optimize the image (necessary for viewing on the kindle)
pngcrush -q -c 0 weather-processed-tme.png weather-script-output-tme.png > /dev/null 2>&1

#We move the image where it needs to be (the webserver directory)
rm /var/www/html/weather-script-output-tme.png
mv weather-script-output-tme.png /var/www/html/weather-script-output-tme.png

#garbage cleanup
#rm weather-processed-tme.svg
#rm weather-processed-tme.png

