import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import gspread
import plotly.express as px


import os

api_key = os.environ.get('API_KEY')

if api_key:
    print(f"API Key accessed successfully: {api_key[:5]}...") # Print only a part for security
# Use the api_key for your operations
else:
    print("API_KEY environment variable not found.")


gc = gspread.service_account_from_dict(api_key)


#First Extract Data from appropriate google sheet pages:
sh = gc.open("SASI 2025 Course Results")



#take user input here:
email = st.text_input("Your Survey Receiving Email:")
st.write("The current email:", email)

AM_survey_tracker = pd.DataFrame(sh.worksheet("Survey Tracker AM").get_all_values())
PM_survey_tracker = pd.DataFrame(sh.worksheet("Survey Tracker PM").get_all_values())

new_header = AM_survey_tracker.iloc[0]
AM_survey_tracker.columns = new_header
AM_survey_tracker = AM_survey_tracker[1:]

new_header = PM_survey_tracker.iloc[0]
PM_survey_tracker.columns = new_header
PM_survey_tracker = PM_survey_tracker[1:]

THE_survey_tracker = pd.DataFrame()

# Page config
st.set_page_config(page_title='Student SASI Survey Display', layout='wide')

try:

    if email in AM_survey_tracker["Email"].tolist():
        THE_survey_tracker = AM_survey_tracker
        st.subheader(f"You're AM")
    elif email in PM_survey_tracker["Email"].tolist():
        THE_survey_tracker = PM_survey_tracker
        st.subheader(f"You're PM")
    else:
        st.subheader(f"Please input a valid email:")


    THE_student_info = THE_survey_tracker[THE_survey_tracker["Email"] == email].iloc[:,:3]
    THE_student = THE_survey_tracker[THE_survey_tracker["Email"] == email].iloc[:,3:].astype(float).clip(upper = 1)
    #Then convert these to pandas-dataframes:
    #Then plot via plotly and display via individuals: 

    st.subheader(f"Welcome: {THE_student_info.iloc[0,0]} {THE_student_info.iloc[0,1]}")
    col1, col2 = st.columns(2)
    col1.metric("Surveys Completed:", f"{THE_student.iloc[0].tolist().count(1.0)}")
    col2.metric("Total:", f"{len(THE_student.iloc[0].tolist())}")


    #the plotly graph
    red_to_green = [[0, 'red'], [1, 'green']]

    fig_heat = px.imshow(THE_student, x=THE_student.columns, y=THE_student.index, aspect='auto', color_continuous_scale= red_to_green, title = f"Survey's for Student Email: {email}")
    fig_heat.update_traces(xgap=2, ygap=2)  # Increase the gap to see lines
    fig_heat.update_layout(coloraxis_colorbar=dict(
        title=dict(text="Completion Status"),
        tickvals=[0,1],
        ticktext=["Incomplete", "Completed"],
    ))
    st.plotly_chart(fig_heat)

except:
    st.subheader(f"Please input your email above")

