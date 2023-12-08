import pandas as pd
import csv
import matplotlib.pyplot as plt

'''
dataset:
        from: kaggle
        https://www.kaggle.com/datasets/selfishgene/historical-hourly-weather-data/data
        https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020/
        main data file: circuits.csv constructor_results.csv constructor_standings.csv constructors.csv
                        driver_standings.csv drivers.csv lap_times.csv pit_stops.csv qualifying.csv
                        races.csv results.csv seasons.csv sprint_results.csv status.csv
                  

this .py file is a backup file for TK's 143_PROJ.ipynb
you should go through the code in .ipynb file to know details.

'''


# load data 
d_results = pd.read_csv("./archive/results.csv")
d_drivers = pd.read_csv("./archive/drivers.csv")
d_driver_standings = pd.read_csv("./archive/driver_standings.csv")
d_races = pd.read_csv("./archive/races.csv")
d_circuits = pd.read_csv("./archive/circuits.csv")

# process data (drop some useless part)
d_results_ = pd.DataFrame(d_results, columns = ['raceId','driverId','rank'])
d_drivers_ = pd.DataFrame(d_drivers, columns = ['driverId','nationality'])
d_driver_standings_ = pd.DataFrame(d_driver_standings, columns=['raceId','driverId','wins'])
d_races_ = pd.DataFrame(d_races, columns = ['raceId','name','circuitId'])
d_circuits_ = pd.DataFrame(d_circuits, columns = ['country','circuitId'])

# merge data
d = pd.merge(d_circuits_, d_races_)
d = pd.merge(d, d_results_)
d = pd.merge(d, d_drivers_)
d = pd.merge(d, d_driver_standings)

# process null data
dn = d[d['rank']!= '\\N']
dn = pd.DataFrame(dn, columns=['country','raceId','name','driverId','nationality','rank','wins'])

# save data (backup)
# dn.to_csv('myproj.csv')


# select data
res = []
s = {}
for i in dn['driverId']:
    if i in s:
        s[i] += 1
    else:
        s[i] = 1
        res.append(dn[dn['driverId']==i])

countries_drivers = {'Argentina':'Argentine',
 'Australia': 'Australian',
 'Austria':'Austrian',
 'Belgium':'Belgian',
 'Brazil':'Brazilian',
 'Canada':'Canadian',
 'China':'Chinese',
 'France':'French',
 'Germany':'German',
 'Hungary':'Hungarian',
 'India':'Indian',
 'Italy':'Italian',
 'Japan':'Japanese',
 'Malaysia':'Malaysian',
 'Mexico':'Mexican',
 'Monaco':'Monegasque',
 'Portugal':'Portuguese',
 'Russia':'Russian',
 'South Africa':'South African',
 'Spain':'Spanish',
 'Sweden':'Swedish',
 'Switzerland':'Swiss',
 'UK':'British',
 'USA':'American',
 'United States':'American'}

drivers_countries = {}
for i,j in zip(countries_drivers.keys(),countries_drivers.values()):
    drivers_countries[j] = i
    
for i in res:
    i.reset_index(drop=True,inplace=True)
    
    
    
newres = []
for i in res:
    if i.iloc[0,5] in drivers_countries:
        newres.append(i)
    else:
        pass
    
for i in newres:
    i.replace('USA','United States',inplace=True)
 
 
# add HomeRace   
for i in newres:
    i['HomeRace'] = i.apply(lambda x: drivers_countries[x['nationality']]==x['country'],axis=1)
    
    
newres1 = sorted(newres, key = lambda x:len(x), reverse = True)

# generate driverId topNumberNonHome topNumberHome MiddleNumberNonHome MiddleNumberHome BottomNumberNonHome BottomNumberHome nonHomeRaceMeanRank HomeRaceMeanRank

rrr = []
# driverId topNumberNonHome topNumberHome MiddleNumberNonHome MiddleNumberHome BottomNumberNonHome BottomNumberHome nonHomeRaceMeanRank HomeRaceMeanRank
for i in range(20):
    a = (newres1[i][((newres1[i]['rank']-newres1[i]['rank'].min()) <= ((newres1[i]['rank'].max()-newres1[i]['rank'].min())*0.3))])
    aAll = len(a)
    aHome = a[a['HomeRace']==1]
    aOut = aAll - len(aHome)
    ab = (newres1[i][((newres1[i]['rank']-newres1[i]['rank'].min()) <= ((newres1[i]['rank'].max()-newres1[i]['rank'].min())*0.6))])
    abAll = len(ab)
    abHome = ab[ab['HomeRace']==1]
    bHome = len(abHome) - len(aHome)
    bOut = abAll - len(abHome) - aOut
    abc = newres1[i]
    abcAll = len(abc)
    abcHome = abc[abc['HomeRace']==1]
    cHome = len(abcHome) - len(abHome)
    cOut = abcAll - len(abcHome) - aOut - bOut
    rrr.append([newres1[i].iloc[0,2], aOut,len(aHome),bOut,bHome,cOut,cHome, newres1[i][newres1[i]["HomeRace"]==False]["rank"].mean(),newres1[i][newres1[i]["HomeRace"]==True]["rank"].mean()])
    
# create dataframe
rId = []
rTopnH = []
rTopH = []
rMiddlenH = []
rMiddleH = []
rBottomnH = []
rBottomH = []
rnonHome = []
rHome = []
for i in range(len(rrr)):
    rId.append(rrr[i][0])
    rTopnH.append(rrr[i][1])
    rTopH.append(rrr[i][2])
    rMiddlenH.append(rrr[i][3])
    rMiddleH.append(rrr[i][4])
    rBottomnH.append(rrr[i][5])
    rBottomH.append(rrr[i][6])
    rnonHome.append(rrr[i][7])
    rHome.append(rrr[i][8])
    
driverName = ['Fernando','Lewis','Sebastian','Sergio','Felipe','Jenson','Daniel','Rosberg','Nico','Romain','Carlos','Mark','Rubens','Jarno','Lance','Esteban','Adrian','Antonio','Charles','Nick']
   
data = {'driverId':rId,
          'driverName':driverName,
          'Top (Out Home Country)':rTopnH,
          'Top (In Home Country)':rTopH,
          'Middle (Out Home Country)':rMiddlenH,
          'Middle (In Home Country)':rMiddleH,
          'Bottom (Out Home Country)':rBottomnH,
          'Bottom (In Home Country)':rBottomH,
          'nonHomeAvgRank':rnonHome,
          'HomeAvgRank':rHome}
data = pd.DataFrame(data)

# Preparing the data for plotting
# Number of categories
n_categories = 3

# Plotting
plt.figure(figsize=(12, 6))

# Creating the bar width
bar_width = 0.35

# Creating index for each driverId
index = np.arange(len(df['driverId']))

# Plotting Out Home Country data
plt.bar(index, df['Top (Out Home Country)'], bar_width, color='b', label='Top (Out Home Country)')
plt.bar(index, df['Middle (Out Home Country)'], bar_width, color='g', label='Middle (Out Home Country)', bottom=df['Top (Out Home Country)'])
plt.bar(index, df['Bottom (Out Home Country)'], bar_width, color='r', label='Bottom (Out Home Country)', bottom=df['Top (Out Home Country)'] + df['Middle (Out Home Country)'])

# Plotting In Home Country data
plt.bar(index + bar_width, df['Top (In Home Country)'], bar_width, color='grey', label='Top (In Home Country)')
plt.bar(index + bar_width, df['Middle (In Home Country)'], bar_width, color='orange', label='Middle (In Home Country)', bottom=df['Top (In Home Country)'])
plt.bar(index + bar_width, df['Bottom (In Home Country)'], bar_width, color='sienna', label='Bottom (In Home Country)', bottom=df['Top (In Home Country)'] + df['Middle (In Home Country)'])

plt.xlabel('Driver ID')
plt.ylabel('Number of Races')
plt.title('Comparison of Race Outcomes for Drivers: Home Country vs. Outside Home Country')
plt.xticks(index + bar_width / 2, df['driverId'])
plt.legend()

plt.tight_layout()
plt.show()

# Plotting
plt.figure(figsize=(15, 8))

# Creating the bar width
bar_width = 0.35

# Creating index for each driverName
index = np.arange(len(df['driverName']))

# Plotting Average Rank in and out of Home Country
plt.bar(index, df['nonHomeAvgRank'], bar_width, color='blue', label='Out Home Country')
plt.bar(index + bar_width, df['HomeAvgRank'], bar_width, color='orange', label='In Home Country')

plt.xlabel('Driver Name')
plt.ylabel('Average Rank')
plt.title('Average Rank Comparison for Drivers: Home Country vs. Outside Home Country')
plt.xticks(index + bar_width / 2, df['driverName'], rotation=45, ha='right')
plt.legend()

plt.tight_layout()
# plt.savefig("Average Rank.jpg")
plt.show()
