import streamlit as st
from datetime import datetime

# Add current directory to path
# import sys
# sys.path.append('.')
from utils import load_config_yaml
from datetime import time

# TODO: 
# - record training time range
# - save result to csv
# - filter exercises based on muscle group
# - Update Exercise expander: show exercise name
# - Convert weights from number to dropdown, define dropdown values based on Muscle Group
# - Update time slider: add option first (morning, afternoon, evening, night) -> display time range
# - Add a button to add not-shown-exercises

config = load_config_yaml('config.yaml')
prim_muscle_groups = config['primary_muscle_groups']
sec_muscle_groups = config['secondary_muscle_groups']
exercise_count = config['exercise_count']
set_count = config['set_count']
exercise_list = config['exercise_list']

st.set_page_config(page_title='Lifting Data Submission',
               page_icon=':man-lifting-weights:')
st.title('Lifting Data Submission')

# Date
st.markdown('### Date')

# 2 options, default is the submission date, other is manual input
date_options = ['Today (automatic, default)', 'Another day']
col1, col2 = st.columns([3, 2])
with col1:
    date_option = col1.radio('Select a date', date_options)

if date_option == date_options[0]:
    date = datetime.today().strftime('%Y-%m-%d')
    col2.text("")   
    col2.markdown(f"""\nSelecting date: **{date}**""")
else:
    date = col2.date_input('Select a date', value=None, min_value=None, max_value=None, key=None)

# Time
st.markdown('### Time')

col1, col2, col3, col4 = st.columns([3, 2, 1, 2])
# with col1:
#     st.markdown('Your training was from:')
# with col2:
#     start_time = st.time_input('Start Time', value=datetime.now().strftime('%H:%M'))
# with col3:
#     st.markdown('to')
# with col4:
#     end_time = st.time_input('End Time', value=datetime.now().strftime('%H:%M'))
training_time_range = st.slider("Your training was from:", value=(time(11, 30), time(12, 45)))
st.write("You're input training time for:", training_time_range)

with st.form(key='my_form'):
    # Muscle Group
    st.markdown('### Muscle Group')
    col1, col2 = st.columns([1, 1])
    
    with col1:
        Primary_Muscle_Group = st.selectbox('Primary Muscle Group', prim_muscle_groups, index=None, placeholder="Select a muscle group")
    with col2:
        Secondary_Muscle_Group = st.selectbox('Secondary Muscle Group', sec_muscle_groups, index=None, placeholder="Select a muscle group")

    # Exercise list
    st.markdown('### Exercise List')
    exercise_records = []
    for i in range(exercise_count):

        with st.expander(expanded=False, label=f"Exercise {i+1}"):
            st.markdown(f'#### Exercise {i+1} of {exercise_count}')
            col1, col2 = st.columns([4, 1])
            with col1:
                exercise_name = st.selectbox('Exercise Name', exercise_list, key = f"exercise_name_{i}")
            with col2:
                notes = st.text_area('Notes', value='', height=None, max_chars=None, key = f"notes_{i}")

            for j in range(set_count):
                col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])
                with col1:
                    st.markdown(f'##### Set {j+1}')
                with col2:
                    weight = st.number_input('Weight (kg)', min_value=0, max_value=500, value=15, step=1, key = f"weight_{i}_{j}")
                with col3:
                    reps = st.number_input('Reps', min_value=0, max_value=100, value=12, step=2, key = f"reps_{i}_{j}")
                with col4:
                    weight_dropdown = st.number_input('Dropdown Weight', min_value=0, max_value=500, value=0, step=1, key = f"weight_{i}_{j}_dropdown")
                with col5:
                    reps_dropdown = st.number_input('Dropdown Reps', min_value=0, max_value=100, value=0, step=1, key = f"reps_{i}_{j}_dropdown")

            # exercise_records.append([exercise_name, weight, sets, reps, notes])


    # Submit button
    submitted = st.form_submit_button('Submit')

if submitted:
    # Save data to a file
    # TODO: Brainstorm the best way to save the data, might ask for consultation from chatbot
    # WITh my requirements above, what would be the best way to save the data?
    # Answer: Save the data to a CSV file, with the columns as specified above
    pass