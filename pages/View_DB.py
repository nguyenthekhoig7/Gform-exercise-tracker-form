# Streamlit file that connects to the database and displays the data in all tables

import streamlit as st

# Add the parent directory to sys.path
import sys
sys.path.append('..')
from config import DB_NAME, EXERCISE_LIST, ADMIN_USERNAME
from db import ExerciseDB

st.set_page_config(page_title='View Lifting Data')
st.title('View Lifting Data')

# Add a form wtih 2 buttons, one to view all the data, and one to clear the database
with st.form(key='view_data_form'):
    # Input username to view all the data
    username = st.text_input('Enter your username')

    # Left button to view the data, right button to reset the database, in columns
    _, col1, _,  col2 = st.columns([1, 4, 1, 3])
    view_data_button = col1.form_submit_button('View Data')
    
    with col2:
        # Put the reset database button in a colapsed expander
        with st.expander("Advanced Option", expanded=False):
            clear_db_button = st.form_submit_button('Reset Database')

db = ExerciseDB(DB_NAME, exercise_list=EXERCISE_LIST, admin_username=ADMIN_USERNAME)

if view_data_button and username:
    if username == ADMIN_USERNAME:
        all_table_names = db.get_all_table_name()
        st.markdown("**Database data**")
        for table in all_table_names:
            data_with_columns = db.get_data(table_name = table, username=ADMIN_USERNAME)

            st.markdown(f"Table: **{table}**")
            _, col = st.columns([1, 19])
            with col:   
                st.dataframe(data_with_columns, hide_index=True, use_container_width=True)


    else:
        # View the data for the specific user
        all_table_names = db.get_all_table_name()
        st.markdown("**Database data**")
        for table in all_table_names:
            data_with_columns = db.get_data(table_name = table, username=username)

            st.markdown(f"Table: **{table}**")
            _, col = st.columns([1, 19])
            with col:
                st.dataframe(data_with_columns, hide_index=True)

if clear_db_button and username:
    # Verify if the user is admin
    if username == ADMIN_USERNAME:
        db.reset_db(username, 'all')
        st.write("Database cleared successfully!")
    else:
        st.write("Only admin can clear the database!")