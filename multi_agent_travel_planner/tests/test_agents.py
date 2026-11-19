from agents.core import TripRequest, TransportationAgent, HotelAgent

def trip(): return TripRequest('Delhi','Manali',4,2,15000,'Bus','Budget Hotel','Budget','Adventure','Regular')
def test_transport_positive(): assert TransportationAgent().run(trip())['estimated_cost']>0
def test_hotel_positive(): assert HotelAgent().run(trip())['estimated_cost']>0
