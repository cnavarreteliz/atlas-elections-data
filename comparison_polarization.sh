## declare an array variable
arr=("nv" "er" "std" "wstd" "kurtosis" "skew")
year=2022
country="France"
level="department_id"
round="first_round"

## now loop through the above array
for method in "${arr[@]}"
do
   python pipeline.py -c "$country" -y "$year" -l "$level" -r "$round" -m "$method"
done