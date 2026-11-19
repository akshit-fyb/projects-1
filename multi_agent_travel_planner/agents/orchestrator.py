from pathlib import Path
from .core import TransportationAgent,HotelAgent,ActivitiesAgent,FoodAgent,BudgetAgent,ItineraryAgent

MODEL=Path(__file__).resolve().parents[1]/'ml'/'models'/'travel_cost_model.joblib'
class TravelPlannerOrchestrator:
    def __init__(self):
        self.transport=TransportationAgent(); self.hotel=HotelAgent(); self.activities=ActivitiesAgent(); self.food=FoodAgent(); self.budget=BudgetAgent(MODEL); self.itinerary=ItineraryAgent()
    def run(self,t):
        components=[self.transport.run(t),self.hotel.run(t),self.activities.run(t),self.food.run(t)]
        budget=self.budget.run(t,components); itinerary=self.itinerary.run(t,budget)
        return {'request':t,'components':components,'budget':budget,'itinerary':itinerary}
