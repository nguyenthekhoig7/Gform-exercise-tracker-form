import streamlit as st
from datetime import datetime

# Add current directory to path
from utils import load_config_yaml, filter_exercises_by_group
from datetime import time
import streamlit_nested_layout

# TODO: 
# Requirements:
# - Add a button to add not-shown-exercises

# - Convert weights from number to dropdown, define dropdown values based on Muscle Group
# Enhancements:
# - Update time slider: add option first (morning, afternoon, evening, night) -> display time range
# - Update Exercise expander: show exercise name
# - Convert JSON to a DB (sqlite might be simplest)


# Not importance-classified yet
# Update the UI: time input confirmation, to "You trained from A to B, duration {B-A}"
# 


config = load_config_yaml('config.yaml')
prim_muscle_groups = config['primary_muscle_groups']
sec_muscle_groups = config['secondary_muscle_groups']
exercise_count = config['exercise_count']
set_count = config['set_count']
exercise_list = config['exercise_list']

st.set_page_config(page_title='Lifting Data Submission',
               page_icon=':man-lifting-weights:')
st.title('Lifting Data Submission')

# Date input
st.markdown('### Date')

date_options = ['Today (automatic, default)', 'Another day']
col1, col2 = st.columns([3, 2])
with col1:
    date_option = col1.radio('Select a date', date_options)

if date_option == date_options[0]:
    date = datetime.today().strftime('%Y-%m-%d-%a')
    col2.text("")   
    col2.markdown(f"""\nSelecting date: **{date}**""")
else:
    date = col2.date_input('Select a date', value=None, min_value=None, max_value=None, key=None)
    if date is not None:
        date = date.strftime('%Y-%m-%d-%a')

# Time input
st.markdown('### Time')

col1, col2, col3, col4 = st.columns([3, 2, 1, 2])

training_time_range = st.slider("Your training was from:", value=(time(11, 30), time(12, 45)))
training_time_range = [str(time_i) for time_i in training_time_range]
st.write("You're input training time for:", training_time_range)

# Muscle Group
st.markdown('### Muscle Group')
col1, col2 = st.columns([1, 1])

with col1:
    Primary_Muscle_Group = st.selectbox('Primary Muscle Group', prim_muscle_groups, index=None, placeholder="Select a muscle group", key="prim_muscle_group")
with col2:
    Secondary_Muscle_Group = st.selectbox('Secondary Muscle Group', sec_muscle_groups, index=None, placeholder="Select a muscle group", key="sec_muscle_group")

# Exercises input
with st.form(key='my_form', clear_on_submit = False):
    # Exercise list
    st.markdown('### Exercise List')
    exercise_records = []
    for i in range(exercise_count):

        with st.expander(expanded=False, label=f"Exercise {i+1}"):
            st.markdown(f'#### Exercise {i+1} of {exercise_count}')
            col1, col2 = st.columns([7, 3])
            with col1:
                filtered_prim_exercises = filter_exercises_by_group(exercise_list, Primary_Muscle_Group, Secondary_Muscle_Group)
                exercise_name = st.selectbox('Exercise Name', filtered_prim_exercises, key = f"exercise_name_{i}")
            with col2.expander(label="Add new exercise", expanded=False):
                all_muscle_groups = prim_muscle_groups.copy()
                all_muscle_groups.extend(sec_muscle_groups)
                print(f"prim_muscle_groups: {prim_muscle_groups}")
                print(f"sec_muscle_groups: {sec_muscle_groups}")
                print(f"All muscle groups to choose from: {all_muscle_groups}")
                new_exercise_muscle_group = st.selectbox('Muscle Group', all_muscle_groups,
                                                         index=None,
                                                         key = f"new_exercise_muscle_group_{i}")
                new_exercise_name = st.text_input("Exercise name: ", key=f"new_exercise_name_{i}")

                new_exercise_name_complete = f"[{new_exercise_muscle_group}] {new_exercise_name}"
                st.markdown(f"You are adding new exercise: {new_exercise_name_complete}")
                print(f"Adding new exercise: {new_exercise_name_complete}")

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

            exercise_records.append({
                'exercise_name': exercise_name,
                # 'notes': notes,
                'sets': [
                    {
                        'weight': weight,
                        'reps': reps
                    }
                    for weight, reps in zip([weight, weight_dropdown], [reps, reps_dropdown])
                ]
            })

    # Submit button
    submitted = st.form_submit_button('Submit')
# Make sure both Muscle Groups are selected
if submitted and None in (Primary_Muscle_Group, Secondary_Muscle_Group):
    st.error('Please select Primary and Secondary Muscle Groups.')

elif submitted:

    st.write('Submitted!')

    # Save to json file
    import json

    json_file_path = 'lifting-history.json'
    # Load existing data
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    
    # Append new data
    data.append({
        'date': date,
        'training_time_range': training_time_range,
        'Primary_Muscle_Group': Primary_Muscle_Group,
        'Secondary_Muscle_Group': Secondary_Muscle_Group,
        'exercise_records': exercise_records
    })
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent = 4)

    # Display the results
    with st.expander('Results'):
        st.write('Date:', date)
        st.write('Time:', training_time_range)
        st.write('Primary Muscle Group:', Primary_Muscle_Group)
        st.write('Secondary Muscle Group:', Secondary_Muscle_Group)
        st.write('Exercise Records:', exercise_records)