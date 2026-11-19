from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / 'data' / 'synthetic_travel_expenses.csv'

def main(n=2500, seed=42):
    rng = np.random.default_rng(seed)
    destinations = np.array(['Manali','Jaipur','Goa','Rishikesh','Agra','Udaipur','Shimla','Varanasi'])
    transport = np.array(['Bus','Train','Car','Flight'])
    accommodation = np.array(['Hostel','Budget Hotel','3-Star Hotel','4-Star Hotel'])
    season = np.array(['Off-season','Regular','Peak'])
    activity = np.array(['Sightseeing','Adventure','Culture','Relaxation'])
    meal = np.array(['Budget','Standard','Premium'])
    dest_factor = {'Manali':1.15,'Jaipur':1.0,'Goa':1.25,'Rishikesh':0.95,'Agra':0.9,'Udaipur':1.1,'Shimla':1.15,'Varanasi':0.85}
    trans_daily = {'Bus':550,'Train':700,'Car':1500,'Flight':3500}
    stay_daily = {'Hostel':700,'Budget Hotel':1200,'3-Star Hotel':2200,'4-Star Hotel':3800}
    season_factor = {'Off-season':0.85,'Regular':1.0,'Peak':1.25}
    act_daily = {'Sightseeing':450,'Adventure':1000,'Culture':550,'Relaxation':650}
    meal_daily = {'Budget':500,'Standard':850,'Premium':1500}
    rows=[]
    for _ in range(n):
        d=str(rng.choice(destinations)); t=str(rng.choice(transport)); a=str(rng.choice(accommodation)); s=str(rng.choice(season)); ac=str(rng.choice(activity)); m=str(rng.choice(meal))
        travellers=int(rng.integers(1,6)); days=int(rng.integers(2,11))
        base=(trans_daily[t]*travellers + days*(stay_daily[a] + meal_daily[m]*travellers + act_daily[ac]*travellers*0.65))
        total=base*dest_factor[d]*season_factor[s] + rng.normal(0,900)
        rows.append([d,travellers,days,a,t,s,ac,m,max(2500,round(total,2))])
    cols=['destination','travellers','days','accommodation','transport','season','activity','meal_preference','total_cost']
    pd.DataFrame(rows,columns=cols).to_csv(OUT,index=False)
    print(f'Created {OUT} with {n} rows')

if __name__=='__main__': main()
