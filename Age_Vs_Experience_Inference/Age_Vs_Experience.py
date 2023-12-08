import pandas as pd
import csv
from fastf1.ergast import Ergast
import builtins
from collections import defaultdict
import plotly.express as px

def get_schedule_span(start_year, end_year):
    """
    Retrieve and organize Formula 1 race schedules and results for a span of multiple years. You may select a span between 1992 to 2022.
    **NOTE: Retrieving data may take some time**
 
    Parameters:
    - start_year (int): The starting year of the desired span.
    - end_year (int): The ending year of the desired span.

    Returns:
    - dict: A dictionary where keys are years and values are DataFrames containing race schedules and results.
    - DataFrames contain round #, country, driver code, and points
    """

    assert isinstance (start_year, int) and isinstance (end_year, int), "inputs must be years as ints"
    assert start_year >= 1992, "Ergast data starts from 1992"
    assert end_year <= 2022, "Ergast data ends at 2022"
    assert start_year < end_year, "start_year must be < end_year"

    # generate ergast object
    ergast = Ergast()
    
    race_schedules = {}  # Initialize the dictionary outside the loop

    # Grab the race schedule for each year between start_year and end_year
    for year in range(start_year, end_year + 1):
        races = ergast.get_race_schedule(year)

        # stores results for each year
        results = []
        
        # For each race in the season
        for rnd, race in races['raceName'].items():
            # Get results. Note that we use the round no. + 1, because the round no.
            # starts from one (1) instead of zero (0)
            temp = ergast.get_race_results(season=year, round=rnd + 1)
            temp = temp.content[0]

            # If there is a sprint, get the results as well
            sprint = ergast.get_sprint_results(season=2022, round=rnd + 1)
            if sprint.content and sprint.description['round'][0] == rnd + 1:
                temp = pd.merge(temp, sprint.content[0], on='driverCode', how='left')
                # Add sprint points and race points to get the total
                temp['points'] = temp['points_x'] + temp['points_y']
                temp.drop(columns=['points_x', 'points_y'], inplace=True)

            # Add round no. and grand prix name
            temp['round'] = rnd + 1
            temp['race'] = race.removesuffix(' Grand Prix')
            # temp = temp[['round', 'race', 'driverCode', 'points']]  # Keep useful cols.
            results.append(temp)

        # Append all races into a single dataframe
        results = pd.concat(results)
        races = results['race'].drop_duplicates()
        race_schedules[year] = results

        # print(year)
        # print(results)

    # print(race_schedules)
    return race_schedules


#Fetching data from 2012 to 2022
race_schedules = get_schedule_span(2012, 2022) 

#Declaring dataframes for individual years
df_2012 = race_schedules[2012][['number', 'position', 'points', 'status', 'driverId', 'driverCode', 'givenName', 'familyName', 'dateOfBirth', 'constructorId', 'constructorName', 'round']].assign(year = 2012)
df_2013 = race_schedules[2013][['number', 'position', 'points', 'status', 'driverId', 'driverCode', 'givenName', 'familyName', 'dateOfBirth', 'constructorId', 'constructorName', 'round']].assign(year = 2013)
df_2014 = race_schedules[2014][['number', 'position', 'points', 'status', 'driverId', 'driverCode', 'givenName', 'familyName', 'dateOfBirth', 'constructorId', 'constructorName', 'round']].assign(year = 2014)
df_2015 = race_schedules[2015][['number', 'position', 'points', 'status', 'driverId', 'driverCode', 'givenName', 'familyName', 'dateOfBirth', 'constructorId', 'constructorName', 'round']].assign(year = 2015)
df_2016 = race_schedules[2016][['number', 'position', 'points', 'status', 'driverId', 'driverCode', 'givenName', 'familyName', 'dateOfBirth', 'constructorId', 'constructorName', 'round']].assign(year = 2016)
df_2017 = race_schedules[2017][['number', 'position', 'points', 'status', 'driverId', 'driverCode', 'givenName', 'familyName', 'dateOfBirth', 'constructorId', 'constructorName', 'round']].assign(year = 2017)
df_2018 = race_schedules[2018][['number', 'position', 'points', 'status', 'driverId', 'driverCode', 'givenName', 'familyName', 'dateOfBirth', 'constructorId', 'constructorName', 'round']].assign(year = 2018)
df_2019 = race_schedules[2019][['number', 'position', 'points', 'status', 'driverId', 'driverCode', 'givenName', 'familyName', 'dateOfBirth', 'constructorId', 'constructorName', 'round']].assign(year = 2019)
df_2020 = race_schedules[2020][['number', 'position', 'points', 'status', 'driverId', 'driverCode', 'givenName', 'familyName', 'dateOfBirth', 'constructorId', 'constructorName', 'round']].assign(year = 2020)
df_2021 = race_schedules[2021][['number', 'position', 'points', 'status', 'driverId', 'driverCode', 'givenName', 'familyName', 'dateOfBirth', 'constructorId', 'constructorName', 'round']].assign(year = 2021)
df_2022 = race_schedules[2022][['number', 'position', 'points', 'status', 'driverId', 'driverCode', 'givenName', 'familyName', 'dateOfBirth', 'constructorId', 'constructorName', 'round']].assign(year = 2022)

# Concatenate all DataFrames
all_years_df = pd.concat([df_2012, df_2013, df_2014, df_2015, df_2016, df_2017, df_2018, df_2019, df_2020, df_2021, df_2022])

#Convert DoB to datetime
all_years_df['dateOfBirth'] = pd.to_datetime(all_years_df['dateOfBirth'])

# Extract year from 'dateOfBirth'
all_years_df['birthYear'] = all_years_df['dateOfBirth'].dt.year

# Calculate 'currentAge'
all_years_df['currentAge'] = all_years_df['year'] - all_years_df['birthYear']

# Group by 'driverCode' and collect the 'year' values
driver_years = all_years_df.groupby('driverCode')['year'].apply(lambda x: list(set(x))).to_dict()
for years in driver_years:
    driver_years[years].sort()


#Fetching debut years data for drivers
debut_df = pd.read_csv('/Users/abhishikta/Documents/Python Code/ECE 143/Project/drivers_debut_years.csv')

# Create the full name in all_years_df for the merge
all_years_df['fullname'] = all_years_df['givenName'] + ' ' + all_years_df['familyName']

# Perform the merge operation with 'debut_df' to match 'Drivers' with 'fullname'
# and include 'Debut Year' into 'all_years_df'
all_years_df = all_years_df.merge(debut_df, how='left', left_on='fullname', right_on='Drivers')

# Drop the extra columns that came from debut_df
all_years_df.drop(columns=['Drivers', 'fullname'], inplace=True)
all_years_df.rename(columns={'Debut Year': 'debutYears'}, inplace=True)

# Now all_years_df has a new column 'debutYears' with the corresponding debut years
print(all_years_df)

#Calculate age of the drivers
all_years_df['age'] = all_years_df['year'] - all_years_df['birthYear']

#Calculate experience of the drivers since their debut year
all_years_df['experience'] = all_years_df['year'] - all_years_df['debutYears']

# Group by 'driverID' and 'year' to sum the points for each driver per year
grouped_df = all_years_df.groupby(['driverCode', 'year']).agg({
    'age': 'first', 
    'experience': 'first', 
    'points': 'sum'  # Summing up all points per year
}).reset_index()

# Rename columns to match the desired output format
grouped_df.rename(columns={
    'driverID': 'Driver',
    'year': 'Year',
    'age': 'Age',
    'experience': 'Experience',
    'points': 'Total_Points'
}, inplace=True)

# Convert the DataFrame to a dictionary
data = grouped_df.to_dict(orient='list')
print(data)

#Convert data to CSV file. This file will be used in Age_Vs_Experience.ipynb to view the plot
file_path = '/Users/abhishikta/Documents/Python Code/ECE 143/Project/ageVsExperienceData.csv' #Change path according to your current working directory while running the code
grouped_df.to_csv(file_path, index=False)

#Draw plot for gauging driver performance with respect to Age vs Experience

agg_df = grouped_df.groupby('driverCode').agg({
    'Age': 'first',  
    'Experience': 'first',  
    'Total_Points': 'sum'  
}).reset_index()


# Create an interactive bubble chart using Plotly
fig = px.scatter(agg_df, x='Age', y='Experience', size='Total_Points', color='Total_Points',
                 hover_name='driverCode', size_max=60, title='Driver Performance: Age vs Experience (Bubble Size: Total Points)', color_continuous_scale=[(0, 'red'), (1, 'black')])

# Add axis labels
fig.update_layout(xaxis_title='Average Age', yaxis_title='Total Experience')

# Show the plot
fig.show()





