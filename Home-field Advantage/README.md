# Introduction
## Hypothesis: 
This analysis was an attempt to analyze whether f1 drivers would be ranked higher if they competed in their home country.

## Parameters: 
In home country or not.

## Correlation Analysis and Conclusion: 
Found limited correlation between country and driver performance.

 
Our graph shows that there is no obvious influence on whether the driver is racing in his own country or not.

### Details
We plotted the average rankings of the drivers in and out of their home country. From this part of the graph, we can't assume that they will perform better in their home country. Furthermore, in the entire dataset, less than 20% of drivers will be ranked higher in their own country, while 15% of drivers will be ranked worse in their own country, with no significant change in rankings for the rest of the drivers. So we conclude that drivers in f1 are barely affected by whether they race in their home country or not.

## Data Collection
from: kaggle
https://www.kaggle.com/datasets/selfishgene/historical-hourly-weather-data/data
https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020/
main data file: circuits.csv constructor_results.csv constructor_standings.csv constructors.csv
                driver_standings.csv drivers.csv lap_times.csv pit_stops.csv qualifying.csv
                races.csv results.csv seasons.csv sprint_results.csv status.csv
all needed files are saved in the 'archive'               

## needed libs
pandas, numpy, csv, matplotlib

