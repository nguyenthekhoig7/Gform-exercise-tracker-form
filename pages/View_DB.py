# Streamlit file that connects to the database and displays the data in all tables

import streamlit as st

# Add the parent directory to sys.path
import sys
sys.path.append('..')
from utils import load_config_yaml
from db import ExerciseDB


config = load_config_yaml('config.yaml')
db_name = config['db_name']
admin_username = config['admin_username']
exercise_list = config['exercise_list']

st.set_page_config(page_title='View Lifting Data')
st.title('View Lifting Data')

# Input username to view all the data
username = st.text_input('Enter your username')

db = ExerciseDB(db_name, exercise_list=exercise_list, admin_username=admin_username)

if username:
    if username == admin_username:
        all_table_names = db.get_all_table_name()
        st.markdown("**Database data**")
        for table in all_table_names:
            data_with_columns = db.get_data(table_name = table, username=admin_username)

            st.markdown(f"Table: **{table}**")
            _, col = st.columns([1, 19])
            with col:   
                st.dataframe(data_with_columns)


    else:
        # View the data for the specific user
        all_table_names = db.get_all_table_name()
        st.markdown("**Database data**")
        for table in all_table_names:
            data_with_columns = db.get_data(table_name = table, username=username)

            st.markdown(f"Table: **{table}**")
            _, col = st.columns([1, 19])
            with col:   
                st.dataframe(data_with_columns)

# def show_data(username: str):
#     cursor.execute("SELECT * FROM lifting_sets WHERE username = ?", (username,))
#     rows = cursor.fetchall()
#     columns = [description[0] for description in cursor.description]
#     data_with_columns = pd.DataFrame(rows, columns = columns)
#     st.dataframe(data_with_columns)