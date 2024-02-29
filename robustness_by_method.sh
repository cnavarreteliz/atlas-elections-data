python pipeline_files.py -c France -y 2022 -l nuts_2 -r first_round -m er -a 0.25
python pipeline_files.py -c France -y 2022 -l nuts_2 -r first_round -m er -a 1
python pipeline_files.py -c France -y 2022 -l nuts_2 -r first_round -m nv
python pipeline_files.py -c France -y 2022 -l nuts_2 -r first_round -m std

python pipeline_files.py -c Chile -y 2021 -l region_id -r first_round -m er -a 0.25
python pipeline_files.py -c Chile -y 2021 -l region_id -r first_round -m er -a 1
python pipeline_files.py -c Chile -y 2021 -l region_id -r first_round -m tw -m nv
python pipeline_files.py -c Chile -y 2021 -l region_id -r first_round  -m tw -m std

python pipeline_files.py -c "United States" -y 2020 -l state -r first_round -n 2 -m er -a 0.25
python pipeline_files.py -c "United States" -y 2020 -l state -r first_round -n 2 -m er -a 1
python pipeline_files.py -c "United States" -y 2020 -l state -r first_round -n 2 -m nv
python pipeline_files.py -c "United States" -y 2020 -l state -r first_round -n 2 -m std
