import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

def pressure_histogram(csv_file_path):
    """
    Read a CSV file containing cleaned F1 merged data into a Pandas DataFrame.
    Calculate the correlation coefficient between Air Pressure and Points earned by each driver.
    Plot the distribution of correlation coefficients as a histogram.

    Parameters:
    - csv_file_path (str): The path to the cleaned CSV file.

    Returns:
    - None
    """

    assert isinstance(csv_file_path, str), "input must be a file path string"

    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Calculate correlation coefficient for each driver
    drivers = df['driverCode'].unique()

    correlation_coefficients = []

    for driver in drivers:
        driver_data = df[df['driverCode'] == driver]

        # Calculate correlation coefficient
        correlation_coefficient, _ = pearsonr(driver_data['Pressure'], driver_data['points'])

        correlation_coefficients.append(correlation_coefficient)

    # Plot correlation coefficients as a histogram
    plt.hist(correlation_coefficients, bins=20, color='red', edgecolor='white')
    plt.xlabel('Correlation Coefficient')
    plt.ylabel('Frequency')
    plt.title('Histogram of Corr. Coeff. Between Air Pressure (mbar) and Points Earned by Drivers')
    plt.show()

csv_file_path = 'cleaned_f1_merged_data.csv'

# Call the function with the cleaned CSV file path
pressure_histogram(csv_file_path)
