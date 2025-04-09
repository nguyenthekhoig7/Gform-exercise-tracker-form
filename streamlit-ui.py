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
# - Deploy the app to streamlit public

# Epic: Users Table
# - FK Constraint: Change username in LiftingSet to user_id, FK to user table

# Epic: Exercises
# - Function: Add new exercise to the database by (username, exercise_name)
# - Validation - add new exercise: selected exercise name must be "[Unknown] Exercise not existed"    
# - Validation - add new exercise: only add to database if `exercise_name` is provided (not None)
# - Validation - select exercise: do not allow the same exercise name to be selected multiple times in the same day
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
# - Convert to using SQModel for better management (this solution = sqlite x pydantic )
# - Time input: custom the range for easier selection, min=14h00, max=21h00 (because I never exercised in the morning)
# ====================================