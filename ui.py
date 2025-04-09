# ui.py
import streamlit as streamlit_client
from datetime import datetime, time
from config import PRIM_MUSCLE_GROUPS, SEC_MUSCLE_GROUPS, UNKNOWN_EXERCISE, ItemKeys
from utils import filter_exercises_by_group

class StreamlitUI:
    def __init__(self, st: streamlit_client = streamlit_client):
        self.st = st

    def input_username(self):
        self.st.markdown('### Username')
        return self.st.text_input('Enter your username')

    def input_date(self):
        self.st.markdown('### Date')
        date_options = ['Today', 'Another day']
        col1, col2 = self.st.columns([3, 2])
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
        return date
    

    def input_time(self):
        self.st.markdown('### Time')
        return self.st.slider("Training Time:", value=(time(11, 30), time(12, 45)))

    def input_muscle_groups(self):
        col1, col2 = self.st.columns([1, 1])
        with col1:
            primary = self.st.selectbox('Primary Muscle Group', PRIM_MUSCLE_GROUPS, index=None, placeholder="Select a muscle group")
        with col2:
            secondary = self.st.selectbox('Secondary Muscle Group', SEC_MUSCLE_GROUPS, index=None, placeholder="Select a muscle group")
        return primary, secondary

    def input_exercises(self, exercise_list, primary_muscle, secondary_muscle, exercise_count, set_count):

        with self.st.form(key='my_form', clear_on_submit = False):
            # Exercise liself.st
            self.st.markdown('### Exercise List')
            exercise_records = []
            for i in range(exercise_count):

                # Each exercise
                
                expanded = True if i == 0 else False
                with self.st.expander(expanded=expanded, label=f"Exercise {i+1} of {exercise_count}"):

                    # Exercise name
                    self.st.markdown(f'#### Exercise Name')
                    col1, col2 = self.st.columns([2, 1])
                    
                    # Option 1: Select existed exercise
                    with col1:
                        filtered_prim_exercises = filter_exercises_by_group(exercise_list, primary_muscle, secondary_muscle)
                        
                        filtered_prim_exercises.append("[Unknown] Exercise not existed")
                        exercise_name = self.st.selectbox('Exercise Name', filtered_prim_exercises, index=None, key = f"exercise_name_{i}")
                    with col2:
                        if  primary_muscle is None and secondary_muscle is None:
                            self.st.error('Please select a muscle group to enable selection.')
                    
                    # Option 2: Add new exercise
                    with self.st.expander(label="Add new exercise", expanded=False):
                        all_muscle_groups = PRIM_MUSCLE_GROUPS.copy()
                        all_muscle_groups.extend(SEC_MUSCLE_GROUPS)
                        col1, col2 = self.st.columns([1, 3])
                        with col1: 
                            new_exercise_muscle_group = self.st.selectbox('Muscle Group', all_muscle_groups,
                                                                index=None,
                                                                key = f"new_exercise_muscle_group_{i}")
                        with col2:  
                            new_exercise_name = self.st.text_input("Exercise name: ", key=f"new_exercise_name_{i}")

                        new_exercise_name_complete = f"[{new_exercise_muscle_group}] {new_exercise_name}"
                        self.st.markdown(f"You are adding new exercise: {new_exercise_name_complete}")

                    if exercise_name == "[Unknown] Exercise not existed":
                        exercise_name = new_exercise_name_complete

                    # Each set: weight and reps
                    for j in range(set_count):
                        col1, col2, col3, col4, col5 = self.st.columns([3, 2, 2, 1, 1])
                        with col1:
                            self.st.markdown(f'##### Set {j+1}')
                        with col2:
                            weight = self.st.number_input('Weight (kg)', min_value=0, max_value=500, value=15, step=1, key = f"weight_{i}_{j}")
                        with col3:
                            reps = self.st.number_input('Reps', min_value=0, max_value=100, value=12, step=2, key = f"reps_{i}_{j}")
                        with col4:
                            weight_dropdown = self.st.number_input('Dropdown Weight', min_value=0, max_value=500, value=0, step=1, key = f"weight_{i}_{j}_dropdown")
                        with col5:
                            reps_dropdown = self.st.number_input('Dropdown Reps', min_value=0, max_value=100, value=0, step=1, key = f"reps_{i}_{j}_dropdown")
                    
                    if exercise_name is not None:
                        exercise_records.append({
                            ItemKeys.EXERCISE_ORDER_ID: i,
                            ItemKeys.EXERCISE_NAME: exercise_name,
                            ItemKeys.SETS: [
                                {
                                    ItemKeys.WEIGHT_KG: weight,
                                    ItemKeys.REPS_COUNT: reps,
                                    ItemKeys.DROPDOWN_WEIGHT_KG: weight_dropdown,
                                    ItemKeys.DROPDOWN_REPS_COUNT: reps_dropdown
                                }
                                for weight, reps, weight_dropdown, reps_dropdown in zip(
                                    [self.st.session_state.get(f"weight_{i}_{set_j}") for set_j in range(set_count)],
                                    [self.st.session_state.get(f"reps_{i}_{set_j}") for set_j in range(set_count)],
                                    [self.st.session_state.get(f"weight_{i}_{set_j}_dropdown") for set_j in range(set_count)],
                                    [self.st.session_state.get(f"reps_{i}_{set_j}_dropdown") for set_j in range(set_count)]
                                )
                            ]
                        })

            # Submit button
            submitted = self.st.form_submit_button('Submit')

        return submitted, exercise_records
    

class InputValidator:
    def __init__(self, st: streamlit_client = streamlit_client):
        self.st = st

    
    def validate_select_exercise(self, num_exercise):
        """
        Check all "exercise_name_{i}" and "new_exercise_name_{i}" 
        Confict is when exercise_name_{i} does not contains "[Unknown] Exercise not existed" and new_exercise_name_{i} is not empty
        """

        for i in range(num_exercise):
            exercise_name = self.st.session_state[f"exercise_name_{i}"]
            new_exercise_name = self.st.session_state[f"new_exercise_name_{i}"]
            new_exercise_group = self.st.session_state[f"new_exercise_muscle_group_{i}"]

            if new_exercise_name != "":

                if exercise_name != "[Unknown] Exercise not existed":
                    error_msg = f"Conflict at Exercise {i+1}: Please select **{UNKNOWN_EXERCISE}** when adding a new exercise."
                    self.st.error(error_msg)
                    return False, error_msg
            
                elif new_exercise_group is None:
                    error_msg = f"Conflict at Exercise {i+1}: Please select a **muscle group** for the new exercise."
                    self.st.error(error_msg)
                    return False, error_msg
            
        return True, ""