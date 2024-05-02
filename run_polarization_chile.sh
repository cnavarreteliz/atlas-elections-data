## declare an array variable
years=("1989" "1993" "1999" "2005" "2009" "2013" "2017" "2021")
country="Chile"
level="region_id"
round="first_round"
agg="circunscription"

## now loop through the above array
for year in "${years[@]}"
do
   python pipeline.py -c "$country" -y "$year" -l "$level" -r "$round" -n 4 -f 1 -a "$agg"
done