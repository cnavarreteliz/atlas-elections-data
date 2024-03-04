# The Atlas of Election Polarization and Competitiveness

Welcome to our repo.

Here, we provide a complete collection of election data worldwide. The data was downloaded from the official electoral institutions of each country and curated as part of our research agenda on divisiveness and polarization in society.

## Data Structure

The file `{year}_{election_type}.csv.gz`, deposited on the folder `data_output/{country}/`, contains information concerning a given `{election_type}`.

| polling_id | value | rate | candidate   | flag_candidate |
| ---------- | ----- | ---- | ----------- | -------------- |
| 1          | 10    | 0.1  | Candidate A | 1              |
| 1          | 90    | 0.9  | Candidate B | 1              |
| 1          | 10    | None | Abstentions | 0              |
| 2          | 50    | 0.5  | Candidate A | 1              |
| 2          | 50    | 0.5  | Candidate B | 1              |
