import pandas as pd
import fastf1
from fastf1.ergast import Ergast
import time

####################################################################################################################################################

def get_schedule_span(start_year, end_year):
    """
    Retrieve and organize Formula 1 race schedules and results for a span of multiple years. You may select a span between 1992 to 2022. It saves the
    data into 'schedules.csv'
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
    combined_schedules = [] # Initilize the list outside the loop

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
            temp = temp[['round', 'race', 'driverCode', 'points']]  # Keep useful cols.
            results.append(temp)

        # Append all races into a single dataframe
        results = pd.concat(results)
        races = results['race'].drop_duplicates()
        race_schedules[year] = results

        # Append all races into a single dataframe
        results['year'] = year  # Add the year column
        results.rename(columns={'race': 'Country'}, inplace=True)  # Rename 'race' to 'Country'
        combined_schedules.append(results)

        # Combine all DataFrames into a single DataFrame
        combined_df = pd.concat(combined_schedules, ignore_index=True)

        # Write the combined DataFrame to a CSV file
        combined_df.to_csv('schedules.csv', index=False)

    return race_schedules

####################################################################################################################################################

def get_weather(schedules): # schedules is a dictionary defined by get_schedule_span()
    """
    Fetches and aggregates weather data for Formula 1 races based on the provided schedules.

    Parameters:
    - schedules (dict): A dictionary returned by the get_schedule_span() function,
                       containing information about the race schedules.

    Returns:
    - weather_data_dict (dict): A dictionary where keys are years and values are DataFrames
                                containing aggregated weather data for each country and race session.

    The function iterates through the provided schedule, fetches weather data for each race session,
    calculates the rounded mean for specific weather parameters, and aggregates the data into a DataFrame.
    The resulting DataFrames are then stored in a dictionary, where each key corresponds to a year.

    The final aggregated weather data is saved to a CSV file named 'weather_data.csv'.
    The function also prints the runtime for execution.
    """
    assert isinstance(schedules, dict), "input must be a dictionary"

    # record start_time
    start_time = time.time()

    # saving the years from the schedule span
    years = list(schedules.keys())

    # saving the countries from the first DataFrame for later use
    first_df = next(iter(schedules.values()))
    countries = set(first_df['Country'].values)
    print(len(countries))

    # Create an empty DataFrame with columns
    columns = ['Country', 'AirTemp', 'Humidity', 'Pressure','TrackTemp', 'WindSpeed']
    this_yr_weather_df = pd.DataFrame(columns=columns)

    weather_data_dict = {}

    for year in years:
        for country in countries:

            # get weather_data df from race session
            race = fastf1.get_session(year, country, 'Race', force_ergast=True)
            race.load(laps=False, telemetry=False, weather=True, messages=False, livedata=None)
            weather_df = race.weather_data
            
            # specify the columns to keep
            columns_to_keep = ['AirTemp', 'Humidity', 'Pressure', 'TrackTemp', 'WindSpeed']

            # calculate the rounded mean for each column
            average_df = weather_df[columns_to_keep].mean().to_frame().transpose()

            # adding 'Pressure; column
            average_df.insert(5, 'Rainfall', weather_df['Rainfall'])  

            # adding 'Country' column 
            average_df.insert(0, 'Country', country)      

            # append new weather values to all_weather_df
            this_yr_weather_df = pd.concat([this_yr_weather_df, average_df], ignore_index=True)

            # print(result)

        # Add the DataFrame to the dictionary with the year as the key
        key = f'{year}'
        weather_data_dict[key] = this_yr_weather_df

    # record end_time
    end_time = time.time()

    # calculate elapsed time
    elapsed_time = end_time - start_time

    print(f"Runtime: {elapsed_time} seconds")

    # concatenate DataFrames into a single DataFrame
    combined_df = pd.concat(weather_data_dict.values(), keys=weather_data_dict.keys())

    #print(combined_df)

    # write the combined DataFrame to a CSV file
    combined_df.to_csv('weather_data.csv')

    return weather_data_dict

####################################################################################################################################################

def fix_columns(file_path):
    """
    Reads CSV data from the specified file path into a Pandas DataFrame,
    adjusts column names, and drops unnecessary columns.

    Parameters:
    - file_path (str): The path to the CSV file to be read.

    Returns:
    - df (pandas.DataFrame): The resulting DataFrame after column adjustments.

    The function reads CSV data from the provided file path into a Pandas DataFrame.
    It then adjusts the column names by renaming the first two columns to 'Year' and 'Index'
    and drops the 'Index' column because it is not needed.
    """

    assert isinstance(file_path, str), "input must be a file path string"

    # Read CSV data into a Pandas DataFrame
    df = pd.read_csv(file_path)

    # Get the current column names
    current_columns = df.columns.tolist()

    # Specify the new names for the first two columns
    new_column_names = ['year', 'Index'] + current_columns[2:]

    # Rename columns based on position
    df.columns = new_column_names

    # Drop Index column because it is not needed
    df = df.drop('Index', axis=1)

    # # Display the DataFrame
    # print(df)

    # Write the modified DataFrame to a new CSV file
    df.to_csv("modified_weather_data.csv", index=False)

    return df

####################################################################################################################################################

def merge_data(schedules_file_path, weather_data_file_path, output_file_path='f1_merged_data.csv'):
    """
    Merge two CSV files containing F1 schedules and weather data into a single DataFrame based on shared column names.
    Save the merged DataFrame to a new CSV file.

    Parameters:
    - schedules_file_path (str): The path to the CSV file containing F1 schedules.
    - weather_data_file_path (str): The path to the CSV file containing weather data.
    - output_file_path (str, optional): The path to the output CSV file where the merged data will be saved.
      Defaults to 'f1_merged_data.csv'.

    Returns:
    - pd.DataFrame: The merged DataFrame.
    """
    
    assert isinstance(schedules_file_path, str), "input must be a file path string"
    assert isinstance(weather_data_file_path, str), "input must be a file path string"


    # Load the CSV files into DataFrames
    df1 = pd.read_csv(schedules_file_path)
    df2 = pd.read_csv(weather_data_file_path)

    # # Drop the 'Index' column from the second DataFrame
    # df2.drop(['Index'], axis=1, inplace=True)

    # Merge the DataFrames based on the shared column names ('year' and 'race')
    merged_df = pd.merge(df1, df2, on=['year', 'Country'])

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv('f1_merged_data.csv', index=False)
    
    return merged_df

####################################################################################################################################################

def clean_and_save_data(file_path, output_file_path='cleaned_f1_merged_data.csv'):
    """
    Read a CSV file into a Pandas DataFrame, clean the data, and save the cleaned DataFrame to a new CSV file.

    Parameters:
    - file_path (str): The path to the input CSV file.
    - output_file_path (str, optional): The path to the output CSV file where cleaned data will be saved.
      Defaults to 'cleaned_f1_merged_data.csv'.

    Returns:
    - pd.DataFrame: The cleaned DataFrame.
    """

    assert isinstance(file_path, str), "input must be a file path stirng"

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Check for missing values in the entire DataFrame
    missing_values = df.isnull().sum()

    # Print the count of missing values for each column
    print("Missing Values per Column:")
    print(missing_values)

    # Drop rows with missing values
    df_cleaned = df.dropna()

    # Remove rows where the value in the "points" column is greater than 26
    df_cleaned = df_cleaned[df_cleaned['points'] <= 26]

    # Round the values in the "points" column to the nearest whole number and convert to int
    df_cleaned['points'] = df_cleaned['points'].round().astype(int)

    # Specify the allowed points
    allowed_points = [0, 1, 2, 4, 6, 8, 10, 12, 15, 18, 25, 26]

    # Remove rows where the "points" column value is not in the allowed_points list
    df_cleaned = df_cleaned[df_cleaned['points'].isin(allowed_points)]

    # Round the values in the "AirTemp" column to the tenths place
    df_cleaned['AirTemp'] = df_cleaned['AirTemp'].round(1)

    # Round the values in the "TrackTemp" column to the tenths place
    df_cleaned['TrackTemp'] = df_cleaned['TrackTemp'].round(1)

    # Round the values in the "Humidity" column to the nearest whole number
    df_cleaned['Humidity'] = df_cleaned['Humidity'].round(0).astype(int)

    # Round the values in the "WindSpeed" column to the nearest hundredths place
    df_cleaned['WindSpeed'] = df_cleaned['WindSpeed'].round(2)

    # Round the values in the "Pressure" column to the nearest hundredths place
    df_cleaned['Pressure'] = df_cleaned['Pressure'].round(2)

    # Check if there are any missing values in the cleaned DataFrame
    if df_cleaned.isnull().values.any():
        print("\nThere are still missing values in the cleaned DataFrame.")
    else:
        print("\nNo missing values found in the cleaned DataFrame.")

    # Save the cleaned DataFrame to a new CSV file
    df_cleaned.to_csv(output_file_path, index=False)

    print(df_cleaned)

    return df_cleaned

####################################################################################################################################################

def data_info(file_path):
    """
    Read a CSV file containing weather data into a Pandas DataFrame.
    Select specific columns ('AirTemp', 'WindSpeed', 'Humidity', 'Pressure') 
    and calculate the maximum, minimum, and average values for each column.
    Also gets the # of races analyzed.

    Parameters:
    - file_path (str): The path to the CSV file.

    Returns:
    - pd.DataFrame: The DataFrame containing the selected columns.
    - pd.Series: Maximum values for each selected column.
    - pd.Series: Minimum values for each selected column.
    - pd.Series: Average values for each selected column.
    """

    assert isinstance(file_path, str), "input must be a file path stirng"
    
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(file_path)

    # Selecting specific columns
    selected_columns = ['AirTemp', 'WindSpeed', 'Humidity', 'Pressure']
    selected_df = df[selected_columns]

    # Finding max, min, and average for each column
    max_values = selected_df.max()
    min_values = selected_df.min()
    average_values = selected_df.mean()

    # Get the number of rows using the len() function
    num_rows = len(df)

    # Printing the results
    print("Maximum values:")
    print(max_values)

    print("\nMinimum values:")
    print(min_values)

    print("\nAverage values:")
    print(average_values)

    print("\nNumber of values/Races:")
    print(num_rows)

    return selected_df, max_values, min_values, average_values

####################################################################################################################################################

"""
Running this sequence of code should produce the 5 CSV files used to perform our weather data analysis

NOTE: You must be connected to the internet for this script to function as it requires access to
      FastF1 / Ergast's online datasets.

1. schedules.csv -> race data from Fastf1 API
2. weather_data.csv -> grabbing weather specific data from using the races from schedules.csv
3. modified_weather_data.csv -> fixing the missing column names from weather_data.csv
4. f1_merged_data.csv -> merging weather_data with schedules by country and year
5. cleaned_f1_merged_data.csv -> cleaning up the merged data

NOTE: More info about the cleaned data is printed using the function data_info()

"""

# 1. Produces -> "schedules.csv"
race_schedules = get_schedule_span(2018, 2022)

# 2. Produces -> "weather_data.csv"
weather = get_weather(race_schedules)

# 3. Produces -> "modified_weather_data.csv"
fix_columns("weather_data.csv")

# 4. Produces -> "f1_merged_data.csv"
merged_data = merge_data('schedules.csv', 'modified_weather_data.csv')

# 5. Produces -> "cleaned_f1_merged_data.csv"
clean_and_save_data('f1_merged_data.csv')

# Produces -> more info 
data_info('cleaned_f1_merged_data.csv')



