import json
from pathlib import Path
import streamlit as st
from agents.core import TripRequest
from agents.orchestrator import TravelPlannerOrchestrator
from integrations.weather import forecast
from database.db import save_trip,recent_trips

st.set_page_config(page_title='Multi-Agent AI Travel Planner',page_icon='🌍',layout='wide')
st.title('🌍 Multi-Agent AI Travel Planner')
st.caption('Academic prototype: coordinated specialist agents + regression ML + live weather. Estimated data is labelled and never presented as live booking availability.')

with st.sidebar:
    st.header('Trip Requirements')
    origin=st.text_input('Starting location','Delhi'); destination=st.text_input('Destination','Manali')
    c1,c2=st.columns(2); days=c1.number_input('Days',2,10,4); travellers=c2.number_input('Travellers',1,10,2)
    budget=st.number_input('Total budget (₹)',2000,500000,15000,step=500)
    transport=st.selectbox('Transport',['Bus','Train','Car','Flight'])
    accommodation=st.selectbox('Accommodation',['Hostel','Budget Hotel','3-Star Hotel','4-Star Hotel'],1)
    meal=st.selectbox('Meals',['Budget','Standard','Premium'])
    activity=st.selectbox('Main interest',['Sightseeing','Adventure','Culture','Relaxation'])
    season=st.selectbox('Season',['Off-season','Regular','Peak'],1)
    generate=st.button('Generate AI Travel Plan',type='primary',use_container_width=True)

if generate:
    model=Path('ml/models/travel_cost_model.joblib')
    if not model.exists(): st.error('ML model is missing. Run: python ml/generate_dataset.py && python ml/train.py'); st.stop()
    trip=TripRequest(origin,destination,int(days),int(travellers),float(budget),transport,accommodation,meal,activity,season)
    result=TravelPlannerOrchestrator().run(trip)
    st.session_state['result']=result
    save_trip(origin,destination,{'components':result['components'],'budget':result['budget'],'itinerary':result['itinerary']})

r=st.session_state.get('result')
if r:
    b=r['budget']; a,bcol,c=st.columns(3); a.metric('Your Budget',f"₹{b['budget']:,.0f}"); bcol.metric('ML Predicted Cost',f"₹{b['ml_predicted_cost']:,.0f}"); c.metric('Budget Status',b['status'],f"₹{b['difference']:,.0f}")
    st.subheader('🤖 Agent Outputs')
    cols=st.columns(4)
    for col,x in zip(cols,r['components']):
        with col: st.markdown(f"**{x['agent']}**"); st.write(x['recommendation']); st.write(f"Estimated ₹{x['estimated_cost']:,.0f}"); st.caption(x['data_type'])
    st.subheader('📅 Day-by-Day Itinerary')
    for d in r['itinerary']['days']: st.markdown(f"**Day {d['day']} — {d['plan']}**")
    st.subheader('🌦 Live Weather')
    try:
        w=forecast(r['request'].destination)
        if w['available']:
            st.caption('Live forecast source: Open-Meteo. Weather is not ML-predicted by this project.')
            st.dataframe(w['days'],use_container_width=True)
        else: st.warning(w['message'])
    except Exception as e: st.warning('Weather API unavailable right now. The rest of the plan still works.')
    st.subheader('💬 Travel Assistant')
    q=st.chat_input('Ask about this trip, e.g. “Why am I over budget?”')
    if q:
        ql=q.lower()
        if 'budget' in ql or 'cost' in ql: ans=f"The working estimate is ₹{b['working_estimate']:,.0f} against your ₹{b['budget']:,.0f} budget. Change transport, accommodation, meals or activities in the sidebar and regenerate."
        elif 'model' in ql or 'regression' in ql: ans='The Budget Agent uses the trained regression pipeline to predict total travel expenditure from trip features. The current training dataset is clearly labelled synthetic supplementary data.'
        else: ans='I can explain the itinerary, budget and regression model. In the next project iteration, this chat router can directly modify trip state and re-run selected agents.'
        with st.chat_message('assistant'): st.write(ans)

with st.expander('💾 Recent saved trips'):
    for x in recent_trips(): st.write(f'{x[0]} — {x[1]} → {x[2]}')

st.divider(); st.caption('Weather data: Open-Meteo (CC BY 4.0). Cost estimates are academic estimates; no hotel/flight availability is claimed.')
