# The Atlas of Election Polarization

Welcome to our repo.

The Atlas of Election Polarization (https://electionpolarization.com) is the most important effort to provide a disaggregated and complete collection of standardized election data worldwide. The data was downloaded from official electoral institutions of each country and was curated as part of our research agenda on divisiveness and polarization in society.

We also provide a index of polarization of regions, which leverages our knowledge about geographical clustering of electorate on Election Day.

## Data Structure

### Dataset 1

The file `{year}_{election_type}_{agg}.csv.gz`, deposited on the folder `data_output/{country}/`, contains fine-grained data concerning an election.

The parameters can be summarized as follows:

- `country`: Election country.

- `year`: Election year.

- `election_type`: Election type. Values accepted are `first_round`, `runoff`, `plebiscite`, `senate`, and `representatives`.

- `agg`: The minimum aggregation level of data. Values accepted are `polling_station`, `precinct`, and `county`.

| polling_id | value | rate | candidate   | flag_candidate |
| ---------- | ----- | ---- | ----------- | -------------- |
| 1          | 10    | 0.1  | Candidate A | 1              |
| 1          | 90    | 0.9  | Candidate B | 1              |
| 1          | 10    | None | Abstentions | 0              |
| 2          | 50    | 0.5  | Candidate A | 1              |
| 2          | 50    | 0.5  | Candidate B | 1              |

We used GZIP as our compression format. The main advantage is reducing the size of big datasets. These files were tested using Python and R.

#### Attributes

- `polling_id`: The unique identifier for the minimum aggregation level. This feature serves as a concatenation of aggregation scales between Dataset 1 and Dataset 2.
- `value`: Number of votes of a given candidate in a `polling_id`.
- `rate`: Voting share of a given candidate (or party) in a `polling_id`.
- `candidate`: Candidate name. In case that the data contains political party, this value is added as a new column called `party`.
- `flag_candidate`: Dummy variable that identifies whether the value included in `candidate` is a political candidate or spoilt and blank votes.

###### Considerations

- The rows in which `flag_candidate == 0` were excluded from the calculations of rates for Election Polarization.
- When information of political party is available on the data, the column `party` is included.

### Dataset 2

The file `{year}_{election_type}_{agg}_location.csv.gz`, deposited on the folder `data_output/{country}/`, enriches the data by including information about the location associated to the `polling_id`.

## Selected Articles

Navarrete, Carlos, et al. "Understanding political divisiveness using online participation data from the 2022 French and Brazilian presidential elections." _Nature Human Behaviour_ 8.1 (2024): 137-148. https://www.nature.com/articles/s41562-023-01755-x
