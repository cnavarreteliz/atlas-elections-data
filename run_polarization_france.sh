## declare an array variable
years=("2002" "2007" "2012" "2017" "2022")
country="France"
level="department_id"
round="first_round"

## now loop through the above array
for year in "${years[@]}"
do
   python pipeline_files.py -c "$country" -y "$year" -l "$level" -r "$round"  -n 8 -m "nv"
done