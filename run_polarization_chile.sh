## declare an array variable
years=("2017")
country="Chile"
level="region_id"
round="first_round"
agg="circunscription"

## now loop through the above array
for year in "${years[@]}"
do
   python pipeline.py -c "$country" -y "$year" -l "$level" -r "$round" -n 4 -f 1 -a "$agg"
done