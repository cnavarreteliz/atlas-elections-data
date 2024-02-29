## declare an array variable
years=("2000" "2004" "2008" "2012" "2016" "2020")
country="United States"
level="state"
round="first_round"

## now loop through the above array
for year in "${years[@]}"
do
   python pipeline.py -c "$country" -y "$year" -l "$level" -r "$round"  -n 2
done