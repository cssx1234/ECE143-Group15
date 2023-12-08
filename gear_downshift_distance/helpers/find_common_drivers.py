import fastf1

gp_locations = [
    'australia',
    'austria',
    'azerbaijan',
    'bahrain',
    'belgium',
    'brazil',
    'canada',
    'france',
    'great britain',
    'hungary',
    'italy',
    'japan',
    'mexico',
    'monaco',
    'netherlands',
    'saudi arabia',
    'singapore',
    'spain',
]

ll, l = [], []

def find_common_drivers():
    """find_common_drivers finds the the 3 letter abbreviation for the drivers who have participated in all grand prixes from the year 2018 to 2022.
    """
    
    for yr in [2018, 2019, 2020, 2021, 2022]:
        for loc in gp_locations:
            session = fastf1.get_session(yr, loc, 'Q')
            session.load(telemetry=False, weather=False)
            
            temp = []
            for driver in session.drivers:
                drv_laps = session.laps.pick_driver(driver)
                abb = drv_laps['Driver'].iloc[0]
                temp.append(abb)
            
            l.append(temp)
            
        res = set(l[0])
        for s in l[1:]:
            res.intersection_update(s)
        print(res)
        ll.append(list(res))


res = set(ll[0])
for s in ll[1:]:
    res.intersection_update(s)
print(res)


with open('common_drivers.txt','w') as f:
    f.write('\n'.join(res))