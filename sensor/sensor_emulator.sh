#!/bin/bash
rps=300
delay_ms=$(echo "1/$rps" | bc -l)


while :
do
    data=$(echo '{}' | jq --arg dt "$(date +"%Y%m%d%H%M")" --arg value $[($RANDOM%1024)] '. | {datetime: $dt, payload: $value|tonumber}')
    curl -H "Content-Type: application/json" -d "$data" http://controller:8080/submit_data/ > /dev/null 2>&1
	# echo "$data"
	sleep $delay_ms
done