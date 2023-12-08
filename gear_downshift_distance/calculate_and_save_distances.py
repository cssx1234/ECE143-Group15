import fastf1
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist
from collections import defaultdict
import pandas as pd

gp_locations = [
    'bahrain',
    'italy',
    'portugal',
    'spain',
    'monaco',
    'azerbaijan',
    'france',
    'austria',
    'great britain',
    'hungary',
    'belgium',
    'netherlands',
    'russia',
    'turkey',
    'brazil',
    'united states',
    'qatar'
]

common_drivers = [
    'LEC',
    'GAS',
    'STR',
    'PER',
    'RUS',
    'MSC',
    'OCO',
    'NOR',
    'BOT',
    'ALO',
    'HAM',
    'RIC',
    'MAG',
    'SAI',
    'ZHO',
    'TSU',
    'VER',
    'LAT',
    'ALB'
]

global exceptions
exceptions = []
distances = defaultdict(list,{k:[] for k in range(1,20)})

year = 2021

def trunc(values, decs=0):
    """trunc truncates the input numpy array with decimal values to the given number of decimal places.

    :param values: values to be truncated
    :type values: Numpy Array
    :param decs: number of decimal places to retain while truncation, defaults to 0
    :type decs: int, optional
    :return: truncated values
    :rtype: Numpy array
    """

    return np.trunc(values*10**decs)/(10**decs)


def calculate_distances(location, year, driver_list):
    """calculate_distances calculates the distances from the corners to the closest downshift points and plots them on a scatterplot graph.

    :param location: location of the grand prix
    :type location: string
    :param year: year of grand prix
    :type year: int
    :param driver_list: list of drivers to be considered
    :type driver_list: list
    """

    global exceptions
    for round_number in ['Q','1','2','3','4','5']:
        session = fastf1.get_session(year, location, round_number) # pulling data from fastf1
        session.load()

        results = session.results
        results.to_csv('./saved_csv_files/results.csv')
        
        if 'Position' in results.columns[results.isna().any()].tolist():
            continue

        laps = session.laps.pick_drivers(driver_list) # getting data for all laps

        circuit_info = session.get_circuit_info()

        for _, lap in laps.iterrows():
            driver = lap['Driver']
            driver_final_position = results.loc[results['Abbreviation'] == driver, 'Position'].iloc[0] if not results[results['Abbreviation'] == driver].empty else None # get final position of driver

            corner_positions = []
            corner_dict = {}

            for _, corner in circuit_info.corners.iterrows(): # iterating over circuit information and saving all corners
                corner_positions.append([corner['X'], corner['Y']])
                corner_x, corner_y = trunc(corner['X'],2), trunc(corner['Y'],2)
                corner_dict[(corner_x, corner_y)] = corner['Number']

            corner_positions = np.asarray(corner_positions, dtype=np.float32)

            try:
                tel = lap.get_telemetry() # getting telemetry data 
            except Exception as e:
                exceptions.append(e)
                continue
            
            x = np.array(tel['X'].values)
            y = np.array(tel['Y'].values)

            points = np.array([x, y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            gear = tel['nGear'].to_numpy().astype(float) # getting gear number for all segments of the track

            downshift_positions = []
            for i in range(len(segments)):
                if gear[i] != gear[i+1] and gear[i] > gear[i+1]:
                    # print(segments[i])
                    downshift_positions.append(segments[i][1])
            downshift_positions = np.asarray(downshift_positions, dtype=np.float32) # finding segments where downshifts occured

            downshift_positions = trunc(downshift_positions, 2)
            corner_positions = trunc(corner_positions,2)

            distance_matrix = cdist(downshift_positions, corner_positions) # finding distance between all corners and downshift points
            closest_corner_indices = np.argmin(distance_matrix, axis=1)
            downshift_to_corner_mapping = {tuple(downshift): corner_positions[closest_corner_index].tolist() for downshift, closest_corner_index in zip(downshift_positions, closest_corner_indices)} # mapping downshoft points to closest corners
            
            for downshift, closest_corner in downshift_to_corner_mapping.items():
                distance = np.linalg.norm(np.array(downshift) - np.array(closest_corner)) # finding distance between downshift point and closest corner
                distances[driver_final_position].append(trunc(distance,2))


if __name__ == "__main__":
    try:
        for location in gp_locations: # iterating for all locations
            calculate_distances(location, year, common_drivers)
            df = pd.DataFrame.from_dict(distances, orient='index')
            df = df.transpose()
            df.to_csv(f'./saved_csv_files/out_{location}.csv') # saving results to csv file
        
    except Exception as e:
        print(e)

    finally: # if exception occurs, save data calculated until exception occured
        df = pd.DataFrame.from_dict(distances, orient='index')
        df = df.transpose()
        df.to_csv(f'./saved_csv_files/out_{location}.csv')

    print(exceptions)
