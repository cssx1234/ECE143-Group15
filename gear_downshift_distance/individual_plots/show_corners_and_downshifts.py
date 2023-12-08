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

distances = defaultdict(list,{k:[] for k in range(1,20)})

global exceptions
exceptions = []

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


def rotate(xy, *, angle):
    """rotate gives the coordinates for a point rotated at a certain angle
    """
    
    rot_mat = np.array([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)


def plot_gear_on_track(lap, circuit_info):
    """plot_track_with_info plots an image of the track with the gear information at each point at the track.

    :param lap: lap under consideration
    :type lap: lap object from fastf1
    :param circuit_info: information about the circuit
    :type circuit_info: object from fastf1
    """

    pos = lap.get_pos_data()
    track = pos.loc[:, ('X', 'Y')].to_numpy()
    track_angle = circuit_info.rotation / 180 * np.pi
    rotated_track = rotate(track, angle=track_angle)
    plt.plot(rotated_track[:, 0], rotated_track[:, 1])

    return track_angle


def plot_corners_and_downshifts(location, year, driver_list):
    global exceptions
    session = fastf1.get_session(year, location, 'Q') # pulling data from fastf1
    session.load()

    laps = session.laps.pick_drivers(driver_list) # getting data for all laps

    circuit_info = session.get_circuit_info()
    offset_vector = [500, 0]

    lap = laps.iloc[2] # choosing random lap
    track_angle = plot_gear_on_track(lap, circuit_info)

    corner_positions = []
    corner_dict = {}

    for _, corner in circuit_info.corners.iterrows(): # iterating over circuit information and saving all corners
        corner_positions.append([corner['X'], corner['Y']])
        corner_x, corner_y = trunc(corner['X'],2), trunc(corner['Y'],2)
        corner_dict[(corner_x, corner_y)] = corner['Number']

        txt = f"{corner['Number']}{corner['Letter']}"
        offset_angle = corner['Angle'] / 180 * np.pi
        offset_x, offset_y = rotate(offset_vector, angle=offset_angle)
        text_x = corner['X'] + offset_x
        text_y = corner['Y'] + offset_y
        text_x, text_y = rotate([text_x, text_y], angle=track_angle)
        track_x, track_y = rotate([corner['X'], corner['Y']], angle=track_angle)
        plt.scatter(text_x, text_y, color='grey', s=140)
        plt.plot([track_x, text_x], [track_y, text_y], color='grey')
        plt.text(text_x, text_y, txt, va='center_baseline', ha='center', size='small', color='white')

    corner_positions = np.asarray(corner_positions, dtype=np.float32)
    tel = lap.get_telemetry() # getting telemetry data 

    x = np.array(tel['X'].values)
    y = np.array(tel['Y'].values)

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    gear = tel['nGear'].to_numpy().astype(float) # getting gear number for all segments of the track

    downshift_positions = []
    for i in range(len(segments)):
        if gear[i] != gear[i+1] and gear[i] > gear[i+1]:
            downshift_positions.append(segments[i][1])
    downshift_positions = np.asarray(downshift_positions, dtype=np.float32) # finding positions where downshifts occured

    downshift_positions = trunc(downshift_positions, 2)
    corner_positions = trunc(corner_positions,2)

    for downshift in downshift_positions:
        plt.scatter(downshift[0], downshift[1], color='#387095') # plotting downshift points
    
    for corner in corner_positions:
        plt.scatter(corner[0], corner[1], color='red') # plotting corner points

    plt.show()



if __name__ == "__main__":
    plot_corners_and_downshifts('austria', 2021, common_drivers)