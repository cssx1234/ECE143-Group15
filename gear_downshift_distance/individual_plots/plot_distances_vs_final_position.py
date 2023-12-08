import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as cm

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
    'russia',
    'turkey'
]

df = pd.read_csv(f'./saved_csv_files/out_bahrain.csv')
for location in gp_locations[1:]:
    temp_df = pd.read_csv(f'./saved_csv_files/out_{location}.csv')
    temp_df.columns = ['Unnamed: 0'] + [str(int(float(col))) for col in temp_df.columns[1:]]
    df = pd.concat([df, temp_df], ignore_index=True)

for i, column in enumerate(df.columns):
    if column != 'Unnamed: 0':
        values = np.ma.masked_invalid(df[column]).compressed()
        indices = [column] * len(values)
        plt.scatter(indices, values, label=column, marker='o', s=5, color='red')

plt.xlabel('Final Position of the Driver')
plt.ylabel('Downshift distance from corner (cm)')
plt.title('Final Position of the Driver vs Downshift distance from corner')
plt.show()

