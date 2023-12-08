import fastf1
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import cm
import numpy as np

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

session = fastf1.get_session(2021, 'austria', 'Q')
session.load()

laps = session.laps.pick_drivers(common_drivers)
circuit_info = session.get_circuit_info()


lap = laps.iloc[3] # picking a specific lap
tel = lap.get_telemetry()

x = np.array(tel['X'].values)
y = np.array(tel['Y'].values)

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
gear = tel['nGear'].to_numpy().astype(float)


cmap = cm.get_cmap('Paired')
lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
lc_comp.set_array(gear)
lc_comp.set_linewidth(4)

plt.gca().add_collection(lc_comp)
plt.axis('equal')
plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

title = plt.suptitle(
    f"Gear usage at every position\nfor a specific lap"
)

cbar = plt.colorbar(mappable=lc_comp, label="Gear Number", boundaries=np.arange(1, 10))
cbar.set_ticks(np.arange(1.5, 9.5))
cbar.set_ticklabels(np.arange(1, 9))
plt.show()
