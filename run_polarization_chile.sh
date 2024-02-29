## declare an array variable
years=("2013" "2017" "2021")
country="Chile"
level="region_id"
round="first_round"

## now loop through the above array
for year in "${years[@]}"
do
   python pipeline.py -c "$country" -y "$year" -l "$level" -r "$round" -n 999 -f 1
   python pipeline.py -c "$country" -y "$year" -l "$level" -r "$round" -n 999 -f 0
done