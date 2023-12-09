#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


data=pd.read_csv('my_dataframe.csv')
data[1:50]


# In[3]:


# Create an empty DataFrame to store the filtered results
selected_rows = pd.DataFrame(columns=data.columns)

# Initialize a variable to track the current 'Stint' value and driver
current_stint = None
current_driver = None

# Iterate through the DataFrame row by row, selecting rows where the 'Stint' changes from 1.0 to 2.0, 2.0 to 3.0, and 3.0 to 4.0.
for index, row in data.iterrows():
    if current_stint is None:
        current_stint = row['Stint']
        current_driver = row['Driver']
        selected_rows = selected_rows.append(row, ignore_index=True)
    elif current_driver != row['Driver']:
        selected_rows = selected_rows.append(row, ignore_index=True)
    elif current_stint == 1.0 and row['Stint'] == 2.0:
        selected_rows = selected_rows.append(row, ignore_index=True)
    elif current_stint == 2.0 and row['Stint'] == 3.0:
        selected_rows = selected_rows.append(row, ignore_index=True)
    elif current_stint == 3.0 and row['Stint'] == 4.0:
        selected_rows = selected_rows.append(row, ignore_index=True)
    elif current_stint == 4.0 and row['Stint'] == 5.0:
        selected_rows = selected_rows.append(row, ignore_index=True)
    elif current_stint == 5.0 and row['Stint'] == 6.0:
        selected_rows = selected_rows.append(row, ignore_index=True)
        selected_rows = selected_rows.append(row, ignore_index=True)
    current_stint = row['Stint']
    current_driver = row['Driver']


# In[4]:


column_names = selected_rows.columns
column_names 


# In[5]:


#select columns needed
selected_columns = selected_rows[['LapNumber','Driver', 'Stint', 'Compound', 'Position']]


# In[6]:


selected_columns = selected_rows[['Driver', 'Compound', 'Position']]


# In[7]:


X = []
y = []
x = []
current_driver = None
previous_position = None

for index, row in selected_columns.iterrows():
    driver = row['Driver']
    compound = row['Compound']
    position = row['Position']
    
    if current_driver != driver:
        if x:
            X.append(x)
            y.append(previous_position)  # Add the last position value of the previous driver to the y list
        
        x = []
        current_driver = driver
    
    x.append(compound)
    previous_position = position  # Update the previous position value
    
# Process the data for the last driver
if x:
    X.append(x)
    y.append(previous_position)


# In[8]:


tire_counts = {'SOFT': 0, 'MEDIUM': 0, 'HARD': 0}
for sublist in X:
    for tire in sublist:
        if tire in tire_counts:
            tire_counts[tire] += 1

# Given tire count data
tire_counts = {'SOFT': 559, 'MEDIUM': 839, 'HARD': 548}

# Creating a bar chart
plt.figure(figsize=(8, 6))
plt.bar(tire_counts.keys(), tire_counts.values(), color=['blue', 'green', 'red'])

plt.title('Tire Type Usage Counts')
plt.xlabel('Tire Type')
plt.ylabel('Usage Count')
plt.xticks(list(tire_counts.keys()))

# Display the chart
plt.show()


# In[9]:


len(X),len(y)


# In[10]:


# Create a new list containing subarrays where the length of the subarray is greater than 1
filtered_subarrays = [X for X in X if len(X) > 1]

# Create a new list containing the y values corresponding to the retained subarrays
filtered_y = [y[i] for i in range(len(X)) if len(X[i]) > 1]
X= filtered_subarrays
y= filtered_y


# In[11]:


filtered_subarrays = [X for X in X if 'INTERMEDIATE' not in X]
filtered_y = [y[i] for i in range(len(X)) if 'INTERMEDIATE' not in X[i]]
y= filtered_y
len(filtered_y)


# In[12]:


# Create a DataFrame and apply one-hot encoding
df = pd.DataFrame(filtered_subarrays)
df = pd.get_dummies(df, columns=df.columns)



# In[13]:


def feature(data):
    return data
    


# In[14]:


X=[]
for index, row in df.iterrows():
    X.append(feature(row.values))
len(X),len(y)


# In[15]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# In[16]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


# In[17]:


model = LinearRegression()
model.fit(X_train, y_train)


# In[18]:


y_pred = model.predict(X_test)


# In[19]:


import numpy as np
squared_diff = (y_test - y_pred)**2
squared_diff
# Assuming you have the squared differences array squared_diff
squared_diff = np.array(squared_diff)  # Replace with your values

# Calculate MSE
mse = np.mean(squared_diff)
mse


# In[20]:


categories = ['HARD', 'MEDIUM', 'SOFT']


# In[21]:


def convert_to_original_format(binary_array, categories):
    original_format = []

    for i in range(0, len(binary_array), 3):
        position = binary_array[i:i+3]
        if 1 in position:

            selected_category = categories[np.argmax(position)]
            original_format.append(selected_category)
    return original_format


converted_data = [convert_to_original_format(arr, categories) for arr in X_test]


for item in converted_data:
    print(item)


# In[22]:


values=y_pred
categories=converted_data
category_dict = {str(category): set() for category in categories}

# Traverse values and add them to the corresponding category list
for category, value in zip(categories, values):
    category_dict[str(category)].add(value)


for category, value_list in category_dict.items():
    print(f"Category: {category}, Values: {value_list}")


# In[23]:


strategies= [
   ['SOFT', 'MEDIUM'],
   ['SOFT', 'MEDIUM', 'HARD'],
   ['MEDIUM', 'HARD'],
   ['MEDIUM', 'MEDIUM', 'HARD'],
   ['SOFT', 'MEDIUM', 'MEDIUM', 'SOFT'],
   ['MEDIUM', 'MEDIUM', 'HARD', 'HARD'],
   ['MEDIUM', 'HARD', 'HARD'],
   ['MEDIUM', 'MEDIUM'],
   ['SOFT', 'HARD'],
   ['SOFT', 'MEDIUM', 'MEDIUM'],
   ['SOFT', 'HARD', 'HARD'],
   ['MEDIUM', 'MEDIUM', 'HARD', 'MEDIUM'],
   ['SOFT', 'HARD', 'MEDIUM'],
   ['SOFT', 'MEDIUM', 'SOFT'],
   ['MEDIUM', 'HARD', 'SOFT', 'SOFT'],
   ['SOFT', 'SOFT', 'MEDIUM'],
   ['SOFT', 'HARD', 'MEDIUM', 'MEDIUM'],
   ['HARD', 'MEDIUM'],
   ['HARD', 'MEDIUM', 'HARD', 'HARD'],
   ['SOFT', 'HARD', 'SOFT', 'SOFT', 'MEDIUM'],
   ['MEDIUM', 'SOFT'],
   ['MEDIUM', 'HARD', 'SOFT'],
   ['SOFT', 'SOFT', 'MEDIUM', 'SOFT'],
   ['SOFT', 'SOFT', 'MEDIUM', 'HARD'],
   ['MEDIUM', 'SOFT', 'HARD'],
   ['MEDIUM', 'MEDIUM', 'HARD', 'MEDIUM', 'HARD'],
   ['MEDIUM', 'MEDIUM', 'SOFT'],
   ['MEDIUM', 'MEDIUM', 'HARD', 'HARD', 'HARD'],
   ['MEDIUM', 'MEDIUM', 'MEDIUM', 'HARD'],
   ['MEDIUM', 'HARD', 'MEDIUM'],
   ['MEDIUM', 'SOFT', 'HARD', 'SOFT'],
   ['SOFT', 'SOFT', 'MEDIUM', 'MEDIUM'],
   ['SOFT', 'MEDIUM', 'HARD', 'SOFT'],
   ['MEDIUM', 'MEDIUM', 'HARD', 'SOFT'],
   ['SOFT', 'MEDIUM', 'SOFT', 'SOFT'],
   ['MEDIUM', 'HARD', 'MEDIUM', 'SOFT'],
   ['MEDIUM', 'HARD', 'MEDIUM', 'HARD'],
   ['SOFT', 'HARD', 'HARD', 'SOFT'],
   ['MEDIUM', 'SOFT', 'MEDIUM'],
   ['HARD', 'MEDIUM', 'HARD']
]

position = [
   10.421807824763274,
   10.135894813226685,
   12.369066495825235,
   11.283008998736495,
   8.7781382928357,
   10.828605624405517,
   12.083153484288644,
   11.568922010273086,
   11.221952310315423,
   9.423878673401273,
   10.936039298778832,
   9.972600329883551,
   10.224023158953422,
   9.668191639829718,
   10.969709930326106,
   12.255863617943877,
   8.913614490100478,
   12.990894357912628,
   12.25057797204506,
   13.813649859258266,
   14.40090695481569,
   11.615450310891678,
   11.610123237378305,
   11.8014602436129,
   14.1149939432791,
   6.071997352739018,
   10.815305825339529,
   6.928002647260984,
   10.116589484580107,
   11.371137344463234,
   13.469253562713527,
   10.945454949090934,
   9.490154432661111,
   10.637268618170923,
   9.022451259264145,
   10.725396963897662,
   10.916733970132256,
   10.29029891821326,
   13.40297780345369,
   12.704981346376037
]

# Draw a bar chart
plt.figure(figsize=(12, 6))
plt.bar(range(len(strategies)), position, tick_label=[" / ".join(strategy) for strategy in strategies],color='red')
plt.xlabel('Strategy')
plt.ylabel('Final Position')
plt.title('Strategy and Performance')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

