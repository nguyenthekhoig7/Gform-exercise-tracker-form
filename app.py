# Run command: `streamlit run app.py`
import streamlit as st
from ui import StreamlitUI, InputValidator
from db import ExerciseDB
from db import LiftingSetsEachDay
import streamlit_nested_layout # To use nested layout in exercise details input
from config import DB_NAME, EXERCISE_LIST, ADMIN_USERNAME, PRIM_MUSCLE_GROUPS, SEC_MUSCLE_GROUPS, NUM_EXERCISES, NUM_SETS

def main():
    st.set_page_config(page_title='Lifting Tracker', page_icon='🏋️')
    st.title('Lifting Data Submission')

    # Just for debugging
    print("Starting the app...")

    ui = StreamlitUI(st)
    validator = InputValidator()
    
    # Create a database instance in the session state if it doesn't exist
    if 'db' not in st.session_state:
        st.session_state.db = ExerciseDB(DB_NAME, exercise_list=EXERCISE_LIST, admin_username=ADMIN_USERNAME)
    
    username = ui.input_username()
    
    if not username:
        # st.error("Enter your username.")
        return
    print(f"Username: {username}")

    if not st.session_state.db.user_exists(username):
        st.session_state.db.add_user(username, tier='user')

    user_exercise_list = st.session_state.db.get_user_exercise_list(username)

    date = ui.input_date()
    time_range = ui.input_time()
    primary_muscle, secondary_muscle = ui.input_muscle_groups()

    if not primary_muscle and not secondary_muscle:
        return

    submit_button, exercise_records = ui.input_exercises(user_exercise_list, primary_muscle, secondary_muscle,
                                                         exercise_count=NUM_EXERCISES, set_count=NUM_SETS)

    if submit_button:
        
        exercise_valid, msg = validator.validate_select_exercise(num_exercise=NUM_EXERCISES)
        if not exercise_valid:
            # st.error(msg)
            return
        
        else:
            st.write('Submitted!')

            # Add the data to the database
            lifting_day = LiftingSetsEachDay(username, date, time_range, exercise_records)
            all_lift_sets = lifting_day.to_lifting_sets()
            st.session_state.db.add_lifting_sets(all_lift_sets)

            # Display the results
            with st.expander('Results'):
                st.write('Username:', username)
                st.write('Date:', date)
                st.write('Time:', time_range)
                st.write('Primary Muscle Group:', primary_muscle)
                st.write('Secondary Muscle Group:', secondary_muscle)
                st.write('Exercise Records:', exercise_records)

if __name__ == '__main__':
    main()
