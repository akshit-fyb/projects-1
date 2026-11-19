from dataclasses import dataclass, asdict
from pathlib import Path
import joblib, pandas as pd

@dataclass
class TripRequest:
    origin:str; destination:str; days:int; travellers:int; budget:float
    transport:str; accommodation:str; meal_preference:str; activity:str; season:str='Regular'

class TransportationAgent:
    def run(self,t):
        per={'Bus':550,'Train':700,'Car':1500,'Flight':3500}[t.transport]
        return {'agent':'Transportation Agent','recommendation':t.transport,'estimated_cost':per*t.travellers,'data_type':'estimate','note':'Planning estimate; not live ticket availability.'}
class HotelAgent:
    def run(self,t):
        per={'Hostel':700,'Budget Hotel':1200,'3-Star Hotel':2200,'4-Star Hotel':3800}[t.accommodation]
        return {'agent':'Hotel Agent','recommendation':t.accommodation,'estimated_cost':per*max(t.days-1,1),'data_type':'estimate','note':'Category estimate; not live room availability.'}
class ActivitiesAgent:
    def run(self,t):
        per={'Sightseeing':450,'Adventure':1000,'Culture':550,'Relaxation':650}[t.activity]
        return {'agent':'Activities Agent','recommendation':t.activity,'estimated_cost':per*t.days*t.travellers*.65,'data_type':'estimate'}
class FoodAgent:
    def run(self,t):
        per={'Budget':500,'Standard':850,'Premium':1500}[t.meal_preference]
        return {'agent':'Food Agent','recommendation':t.meal_preference,'estimated_cost':per*t.days*t.travellers,'data_type':'estimate'}
class BudgetAgent:
    def __init__(self,model_path): self.model=joblib.load(model_path)
    def run(self,t,components):
        X=pd.DataFrame([{'destination':t.destination,'travellers':t.travellers,'days':t.days,'accommodation':t.accommodation,'transport':t.transport,'season':t.season,'activity':t.activity,'meal_preference':t.meal_preference}])
        pred=float(self.model.predict(X)[0]); component=sum(x['estimated_cost'] for x in components)
        chosen=max(pred,component); status='Within budget' if chosen<=t.budget else 'Over budget'
        return {'agent':'Budget Optimization Agent','ml_predicted_cost':round(pred,2),'component_estimate':round(component,2),'working_estimate':round(chosen,2),'budget':t.budget,'status':status,'difference':round(t.budget-chosen,2),'data_type':'ML prediction + estimates'}
class ItineraryAgent:
    def run(self,t,budget):
        labels=['Arrival + local orientation','Main attractions','Interest-focused activities','Local culture + food','Flexible exploration','Scenic day','Shopping + leisure','Extra exploration','Relaxed local day','Departure']
        days=[]
        for i in range(t.days): days.append({'day':i+1,'plan':labels[i if i<len(labels) else -2]})
        return {'agent':'Itinerary Generation Agent','days':days,'budget_status':budget['status']}
