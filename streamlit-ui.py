"""
Update: Use app.py as the main file to run the Streamlit app
This file will be used for planning only.
"""

# import streamlit as st
# from datetime import datetime

# Add current directory to path
# from utils import filter_exercises_by_group, load_st_config
# from datetime import time
# import streamlit_nested_layout # To use nested layout in exercise details input

# from db import ExerciseDB
# from db import LiftingSetsEachDay

# TODO: 
# ==================

# [Requirements] [high priority]
# - BUG: When adding new sets, only first set of first exercise is added to the database, the rest are not added
# - BUG: values in database are not correct, different from the input
# - Deploy the app to streamlit public

# Epic: Users Table
# - Create table: user: username, tier
# - Change username in LiftingSet to user_id, FK to user table

# Epic: Exercises
# - Function: Add default exercises, when new user is created.
# - Function: Add new exercise to the database by (username, exercise_name)
# - Validation - add new exercise: selected exercise name must be "[Unknown] Exercise not existed"    
# - Validation - add new exercise: only add to database if `exercise_name` is provided (not None)

# ==================

# [Enhancements] [medium priority]
# - Convert weights from number to dropdown, define dropdown values based on Muscle Group
# - Update time slider: add option first (morning, afternoon, evening, night) -> display time range
# - Update Exercise expander: show exercise name
# - Convert form into normal widgets, with confirmation message, and confirmation check-box, then Submit button, only process all data when confirmed by the checkbox
# - After add data view page, add function to remove record
# - Add 'required' tag to required fields: username, primary muscle group, secondary muscle group
# - Update the UI: time input confirmation, to "You trained from A to B, duration {B-A}"
# - Rename the files to more meaningful names: streamlit-ui.py -> Lifting_Submission.py, View_DB.py -> View_Data.py

# ====================================

# config = load_st_config(st)
# prim_muscle_groups = config['primary_muscle_groups']
# sec_muscle_groups = config['secondary_muscle_groups']
# exercise_count = config['exercise_count']
# set_count = config['set_count']
# exercise_list = config['exercise_list']
# db_name = config['db_name']
# admin_username = config['admin_username']


# # Initialize/Connect the existed the database
# db = ExerciseDB(db_name, exercise_list=exercise_list, admin_username=admin_username)

# st.set_page_config(page_title='Lifting Data Submission',
#                page_icon=':man-lifting-weights:')
# st.title('Lifting Data Submission')


# # Username input
# st.markdown('### Username')
# username = st.text_input('Enter your username')

# # Date input
# st.markdown('### Date')

# date_options = ['Today (automatic, default)', 'Another day']
# col1, col2 = st.columns([3, 2])
# with col1:
#     date_option = col1.radio('Select a date', date_options)

# if date_option == date_options[0]:
#     date = datetime.today().strftime('%Y-%m-%d-%a')
#     col2.text("")   
#     col2.markdown(f"""\nSelecting date: **{date}**""")
# else:
#     date = col2.date_input('Select a date', value=None, min_value=None, max_value=None, key=None)
#     if date is not None:
#         date = date.strftime('%Y-%m-%d-%a')

# # Time input
# st.markdown('### Time')

# training_time_range = st.slider("Your training was from:", value=(time(11, 30), time(12, 45)))
# training_time_range = [str(time_i) for time_i in training_time_range]
# st.write("You're input training time for:", training_time_range)

# # Muscle Group
# st.markdown('### Muscle Group')
# col1, col2 = st.columns([1, 1])

# with col1:
#     Primary_Muscle_Group = st.selectbox('Primary Muscle Group', prim_muscle_groups, index=None, placeholder="Select a muscle group", key="prim_muscle_group")
# with col2:
#     Secondary_Muscle_Group = st.selectbox('Secondary Muscle Group', sec_muscle_groups, index=None, placeholder="Select a muscle group", key="sec_muscle_group")

# # Exercises input
# with st.form(key='my_form', clear_on_submit = False):
#     # Exercise list
#     st.markdown('### Exercise List')
#     exercise_records = []
#     for i in range(exercise_count):

#         # Each exercise
        
#         expanded = True if i == 0 else False
#         with st.expander(expanded=expanded, label=f"Exercise {i+1} of {exercise_count}"):

#             # Exercise name
#             st.markdown(f'#### Exercise Name')
#             col1, col2 = st.columns([2, 1])
            
#             # Option 1: Select existed exercise
#             with col1:
#                 filtered_prim_exercises = filter_exercises_by_group(exercise_list, Primary_Muscle_Group, Secondary_Muscle_Group)
                
#                 filtered_prim_exercises.append("[Unknown] Exercise not existed")
#                 exercise_name = st.selectbox('Exercise Name', filtered_prim_exercises, index=None, key = f"exercise_name_{i}")
#             with col2:
#                 if  Primary_Muscle_Group is None and Secondary_Muscle_Group is None:
#                     st.error('Please select a muscle group to enable selection.')
            
#             # Option 2: Add new exercise
#             with st.expander(label="Add new exercise", expanded=False):
#                 all_muscle_groups = prim_muscle_groups.copy()
#                 all_muscle_groups.extend(sec_muscle_groups)
#                 col1, col2 = st.columns([1, 3])
#                 with col1: 
#                     new_exercise_muscle_group = st.selectbox('Muscle Group', all_muscle_groups,
#                                                          index=None,
#                                                          key = f"new_exercise_muscle_group_{i}")
#                 with col2:  
#                     new_exercise_name = st.text_input("Exercise name: ", key=f"new_exercise_name_{i}")

#                 new_exercise_name_complete = f"[{new_exercise_muscle_group}] {new_exercise_name}"
#                 st.markdown(f"You are adding new exercise: {new_exercise_name_complete}")

#             # Each set: weight and reps
#             for j in range(set_count):
#                 col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])
#                 with col1:
#                     st.markdown(f'##### Set {j+1}')
#                 with col2:
#                     weight = st.number_input('Weight (kg)', min_value=0, max_value=500, value=15, step=1, key = f"weight_{i}_{j}")
#                 with col3:
#                     reps = st.number_input('Reps', min_value=0, max_value=100, value=12, step=2, key = f"reps_{i}_{j}")
#                 with col4:
#                     weight_dropdown = st.number_input('Dropdown Weight', min_value=0, max_value=500, value=0, step=1, key = f"weight_{i}_{j}_dropdown")
#                 with col5:
#                     reps_dropdown = st.number_input('Dropdown Reps', min_value=0, max_value=100, value=0, step=1, key = f"reps_{i}_{j}_dropdown")
            
#             if exercise_name is not None:
#                 exercise_records.append({
#                     'exercise_order_id': i,
#                     'exercise_name': exercise_name,
#                     'sets': [
#                         {
#                             'weight_kg': weight,
#                             'reps_count': reps,
#                             'dropdown_weight_kg': weight_dropdown,
#                             'dropdown_reps_count': reps_dropdown
#                         }
#                         for weight, reps, weight_dropdown, reps_dropdown in zip(
#                             [weight for _ in range(set_count)],
#                             [reps for _ in range(set_count)],
#                             [weight_dropdown for _ in range(set_count)],
#                             [reps_dropdown for _ in range(set_count)]
#                         )
#                     ]
#                 })

#     # Submit button
#     submitted = st.form_submit_button('Submit')

# # Make sure both Muscle Groups are selected
# if submitted: 

#     if  not username:
#         st.error('Please enter your username.')
    
#     elif submitted and None in (Primary_Muscle_Group, Secondary_Muscle_Group):
#         st.error('Please select both Primary and Secondary Muscle Groups.')

#     else:

#         st.write('Submitted!')

#         # Add the data to the database
#         lifting_day = LiftingSetsEachDay(username, date, training_time_range, exercise_records)
#         all_lift_sets = lifting_day.to_lifting_sets()
#         db.add_lifting_sets(all_lift_sets)

#         # Display the results
#         with st.expander('Results'):
#             st.write('Username:', username)
#             st.write('Date:', date)
#             st.write('Time:', training_time_range)
#             st.write('Primary Muscle Group:', Primary_Muscle_Group)
#             st.write('Secondary Muscle Group:', Secondary_Muscle_Group)
#             st.write('Exercise Records:', exercise_records)