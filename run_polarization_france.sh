## declare an array variable
years=("2002" "2007" "2012" "2017" "2022")
country="France"
level="department_id"
round="runoff"

## now loop through the above array
for year in "${years[@]}"
do
   python pipeline.py -c "$country" -y "$year" -l "$level" -r "$round"  -n 2 -f 1
done